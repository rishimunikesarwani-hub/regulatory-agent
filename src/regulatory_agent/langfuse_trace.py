"""Optional tracing with explicitly enabled fictional local content."""
from contextlib import contextmanager
from contextvars import ContextVar
from functools import lru_cache
import hashlib
import os
from urllib.parse import urlsplit

_model_observation=ContextVar('model_observation',default=None)


def content_capture_enabled():
    return os.environ.get('APP_ENV')=='local' and os.environ.get('LANGFUSE_CAPTURE_CONTENT')=='fictional-local'


@contextmanager
def model_observation(observation):
    token=_model_observation.set(observation)
    try:yield
    finally:_model_observation.reset(token)


def capture_model_content(snapshot, *, input=None, output=None, parameters=None):
    observation=_model_observation.get()
    if observation is None or not content_capture_enabled() or snapshot.get('synthetic') is not True or \
            snapshot.get('mode')!='historical' or not snapshot.get('model_version','').startswith('openai:'):
        return False
    try:
        update={'metadata':{'prompt_version':snapshot['prompt_version'],'content_capture':'fictional-local'}}
        if input is not None:update['input']=input
        if output is not None:update['output']=output
        if parameters is not None:update['model_parameters']=parameters
        observation.update(**update)
        return True
    except Exception:
        return False


def configured():
    return os.environ.get('APP_ENV','local') == 'local' and all(os.environ.get(k) for k in
        ('LANGFUSE_PUBLIC_KEY','LANGFUSE_SECRET_KEY','LANGFUSE_BASE_URL'))


@lru_cache(maxsize=1)
def _client():
    from langfuse import Langfuse
    from opentelemetry.sdk.trace import TracerProvider
    url=urlsplit(os.environ['LANGFUSE_BASE_URL'])
    if url.scheme!='https' or url.username or url.password or url.path not in ('','/') or url.query or url.fragment:
        raise ValueError('langfuse_endpoint_denied')
    return Langfuse(public_key=os.environ['LANGFUSE_PUBLIC_KEY'],secret_key=os.environ['LANGFUSE_SECRET_KEY'],
        base_url=url.geturl(),timeout=3,debug=False,environment='local-fictional-demo',release=os.environ.get('COMMIT_SHA','local'),
        tracer_provider=TracerProvider(),
        # Only our explicit observations are exported. No automatic HTTP or framework spans.
        should_export_span=lambda span:span.instrumentation_scope.name=='langfuse-sdk')


def trace_id(job_id):
    return hashlib.sha256(job_id.encode()).hexdigest()[:32]


def start_job(run, *, client=None, comparison=False):
    try:
        if client is None:
            if not configured():return None
            client=_client()
        return client.start_observation(name='compare-regulatory-requirements' if comparison else 'assess-regulatory-evidence',
            as_type='agent',trace_context={'trace_id':trace_id(run['job_id'])},
            metadata={'demo':'fictional','feature':'comparison' if comparison else 'assessment',
                'content_capture':'fictional-local' if content_capture_enabled() and run.get('model_id','').startswith('openai:') else 'disabled'})
    except Exception:
        return None


def _end(observation):
    try:
        observation.end()
        return True
    except Exception:
        return False


def finish_job(observation, job):
    if observation is None:return False
    updated=False
    try:
        metadata={k:job[k] for k in ('state','model_calls','stop_reason') if k in job}
        observation.update(metadata=metadata,level='DEFAULT' if job.get('state')=='completed' else 'ERROR')
        updated=True
    except Exception:
        pass
    ended=_end(observation)
    return updated and ended


def _name(record):
    if record['operation']=='model':
        key=record['stage_id']
        if key in ('extract-obligations','extract-controls'):return key
        if 'comparison' in str(record.get('versions',{}).get('prompt','')):return 'compare-requirements'
        return 'generate-assessment'
    return {'source_verification':'verify-sources','extraction':'extract-evidence','retrieval':'retrieve-evidence',
        'context_selection':'select-context','validation':'validate-result','persistence':'save-result'}.get(record.get('stage'),'process-stage')


def start_attempt(record, *, client=None, parent=None):
    try:
        if client is None:
            if not configured():return None
            client=_client()
        model=record.get('actual_response_model_id') or record.get('model_id')
        start=parent.start_observation if parent is not None else client.start_observation
        args={} if parent is not None else {'trace_context':{'trace_id':trace_id(record['job_id'])}}
        return start(name=_name(record),
            as_type='generation' if record['operation']=='model' else 'retriever' if record['operation']=='retrieval' else 'span',
            model=model.removeprefix('openai:') if model else None,
            metadata={'event_id':record['event_id'],'stage_id':record['stage_id'],'operation':record['operation'],'demo':'fictional'},**args)
    except Exception:
        return None


def export_attempt(record, *, client=None, observation=None):
    updated=False
    try:
        observation=observation or start_attempt(record,client=client)
        if observation is None:return False
        metadata={k:record[k] for k in ('event_id','operation','state','duration_seconds','dispatched') if k in record}
        update={'metadata':metadata,'level':'DEFAULT' if record.get('state')=='succeeded' else 'ERROR'}
        if record.get('operation')=='model':
            usage=record.get('usage',{})
            update['usage_details']={name:usage[key] for name,key in (('input','input_tokens'),('output','output_tokens'),('cache_read_input_tokens','cache_read_tokens'))
                if type(usage.get(key)) is int and usage[key]>=0}
            model=record.get('actual_response_model_id') or record.get('model_id')
            if model:update['model']=model.removeprefix('openai:')
        observation.update(**update)
        updated=True
    except Exception:
        pass
    ended=_end(observation) if observation is not None else False
    return updated and ended


def flush():
    try:
        if configured():_client().flush()
    except Exception:
        pass
