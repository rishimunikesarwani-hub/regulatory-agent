"""Local process supervision for admitted jobs. No queue transport or public admission."""
from contextlib import redirect_stderr, redirect_stdout
from datetime import datetime, timezone
import multiprocessing
import os
import pickle
import time

from .contracts import ContractError
from .telemetry import StageAttempt


def _execute(target, args):
    # Uploaded text is never a callable. Targets come from trusted application code.
    with open(os.devnull, 'w') as sink, redirect_stdout(sink), redirect_stderr(sink):
        try:
            target(*args)
        except BaseException:
            raise SystemExit(1) from None


def _stop(store, owner, case, job_id, token, reason):
    job = store.read_job(owner, case, job_id)
    if job['state'] != 'running' or job['token'] != token:
        return job
    snapshot = store.get(owner, case, 'snapshot', job['snapshot_id'])
    with store.transaction() as db:
        job = store._job(db, owner, case, job_id)
        store._claimed(job, token, time.time(), permit_expired=True)
        rows = db.execute("SELECT id,body FROM records WHERE case_id=? AND kind='stage_attempt'", (case,)).fetchall()
        for identity, body in rows:
            attempt = StageAttempt.model_validate_json(body)
            if attempt.job_id != job_id or attempt.state != 'unknown':
                continue
            event = StageAttempt.model_validate(attempt.model_dump() | {
                'state':'interrupted', 'finished_at':datetime.now(timezone.utc),
                'errors':('timeout' if reason == 'worker_timeout' else 'interrupted',),
                'dispatched':job['model_calls'] > 24 - attempt.unused_allowance
                    if attempt.operation == 'model' and attempt.unused_allowance is not None else attempt.dispatched})
            db.execute("UPDATE records SET body=? WHERE case_id=? AND kind='stage_attempt' AND id=?",
                (event.model_dump_json(), case, identity))
        accounted = {o for stage in job['stages'].values() for o in stage.get('accounted_obligations', [])}
        unchecked = [o for o in snapshot['selected_obligations'] if o not in accounted]
        job.update(state='partial' if accounted else 'failed', unchecked_obligations=unchecked,
                   stop_reason=reason, finished_at=time.time())
        store._save_job(db, job)
    return job


def supervise(store, owner, case, job_id, target, *, args=()):
    """One child per saved claim. The parent owns the remaining deadline and lease."""
    token = store.claim(owner, case, job_id)
    job = store.read_job(owner, case, job_id)
    if token is None:
        return job
    remaining = job['deadline'] - time.time()
    if remaining <= 0:
        return _stop(store, owner, case, job_id, token, 'worker_timeout')
    end = time.monotonic() + remaining
    process = multiprocessing.get_context('spawn').Process(name=f'assessment-{job_id}',
        target=_execute, args=(target, (*args, owner, case, job_id, token)), daemon=True)
    reason = 'worker_crashed'
    try:
        # Windows launches the child before serializing arguments. Validate first.
        pickle.dumps((target, (*args, owner, case, job_id, token)))
        process.start()
        while process.is_alive():
            remaining = end - time.monotonic()
            if remaining <= 0:
                reason = 'worker_timeout'
                break
            process.join(min(5, remaining))
            if process.is_alive() and time.monotonic() < end:
                store.renew(owner, case, job_id, token)
    except ContractError:
        # A newer claim owns finalization. Cleanup still stops this parent's child.
        reason = 'worker_claim_lost'
    except Exception:
        reason = 'worker_start_failed' if process.pid is None else 'worker_supervisor_failed'
    finally:
        if process.pid is not None:
            if process.is_alive():
                process.terminate()
                process.join(1)
            if process.is_alive():
                process.kill()
                process.join(1)
            if process.is_alive():
                raise ContractError('worker_stop_failed')
        process.close()
    return _stop(store, owner, case, job_id, token, reason)


def bedrock_child(database_path, profile, owner, case, job_id, token):
    """Construct SDK clients only in the child, using trusted server configuration."""
    from .assessment_pipeline import AssessmentPipeline
    from .assessments import Assessments
    from .bedrock_model import BedrockModel
    from .cases import CaseService, SQLiteCases
    from .documents import Documents
    cases = CaseService(SQLiteCases(database_path))
    service = Assessments(cases, Documents(cases))
    run, snapshot = service._run(owner, case, job_id)
    service.store._claimed(service.store.read_job(owner, case, job_id), token, time.time())
    if run['data_mode'] != 'synthetic_live' or not snapshot['synthetic']:
        raise ContractError('private_model_processing_unverified')
    AssessmentPipeline(service, BedrockModel.configured(profile=profile)).run(owner, case, job_id, execution_token=token)
