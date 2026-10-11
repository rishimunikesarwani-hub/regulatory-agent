"""Shared comparison HTTP behavior. Transport adapters validate bodies and authenticate first."""
from .cases import CaseError, not_found, unavailable
from .contracts import ContractError
from .comparison_jobs import Comparisons


def response(service, delivery, owner, case, method, route, request=None, snapshot_id=None):
    comparisons=Comparisons(service)
    try:
        if method=='GET' and route==['regulatory-comparisons','selection']:
            if not isinstance(snapshot_id,str):
                raise CaseError(422,'comparison_selection_required','Select the previous assessment.',
                    'Open a completed historical assessment before comparison.')
            return 200,comparisons.selection(owner,case,snapshot_id)
        if method=='GET' and route==['regulatory-comparisons']:return 200,comparisons.list(owner,case)
        if method=='GET' and len(route)==2:return 200,comparisons.read(owner,case,route[1])
        if method!='POST':raise not_found()
        if route!=['regulatory-comparisons'] and (len(route)!=3 or route[2] not in {'resume','reassess'}):raise not_found()
        if delivery is None:raise unavailable()
        queue=delivery() if callable(delivery) else delivery
        if route==['regulatory-comparisons']:
            record=comparisons.admit(owner,case,request)
            queue.send(owner,case,record['job_id'])
            return 202,comparisons.read(owner,case,record['comparison_id'])
        if route[2]=='resume':
            record,_,_=comparisons._record(owner,case,route[1])
            queue.send(owner,case,record['job_id'])
            return 202,comparisons.read(owner,case,route[1])
        # The typed transport request requires a strict true selection acknowledgment.
        if request is None or request.selection_reviewed is not True:
            raise CaseError(422,'selection_review_required','Review the changed selection before assessment.',
                'Confirm the saved regulatory version and unchanged bank inputs.')
        run=comparisons.reassess(owner,case,route[1])
        queue.send(owner,case,run['job_id'])
        return 202,run
    except ContractError as error:
        code=str(error)
        if code in {'record_not_found','job_not_found','comparison_baseline_missing'}:raise not_found() from None
        if code in {'idempotency_conflict','immutable_record','record_write_conflict'}:
            raise CaseError(409,'comparison_conflict','The saved comparison request changed.',
                'Refresh the saved comparison before another request.') from None
        if code in {'comparison_baseline_unfinished','comparison_reassessment_unavailable'}:
            raise CaseError(409,'comparison_unavailable','This comparison cannot start the requested processing.',
                'Complete the comparison and resolve its selection before a new assessment.') from None
        if code in {'invalid_identifier','comparison_processing_unverified','comparison_pair_invalid',
                'comparison_regulatory_scope_invalid','comparison_obligation_scope','comparison_context_limit',
                'mandatory_regulatory_context_limit','comparison_control_support_missing','comparison_baseline_findings_missing'}:
            raise CaseError(422,'comparison_selection_invalid','The selected comparison context is unavailable.',
                'Select saved RBI versions and a completed historical assessment with fictional bank data.') from None
        raise unavailable() from None
