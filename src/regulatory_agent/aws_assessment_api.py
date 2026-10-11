"""Authenticated native assessment routes. Cognito and case authorization precede this module."""
import base64
import binascii
from datetime import datetime, timezone
import json
import uuid

from pydantic import ValidationError

from .aws_execution import CloudSelection
from .cases import CaseError, invalid_request, not_found, unavailable
from .contracts import ContractError, ExportRequest, ReviewRequest, StartAssessment
from .reviews import instant


def _body(event, contract):
    raw=event.get('body') or ''
    try:
        if not isinstance(raw,str) or len(raw.encode())>64_000: raise ValueError()
        data=base64.b64decode(raw,validate=True) if event.get('isBase64Encoded') is True else raw.encode()
        if len(data)>32_000: raise ValueError()
        return contract.model_validate_json(data)
    except (ValueError,TypeError,UnicodeError,binascii.Error,ValidationError): raise invalid_request() from None


def response(service, queue, owner, case, method, route, event, *, source_root=None):
    """Return public response data. Never return a raw execution record from the queue."""
    try:
        query=event.get('queryStringParameters') or {}
        if not isinstance(query,dict): raise invalid_request()
        cutoff=query.get('cutoff')
        if cutoff is not None:
            try:
                if not isinstance(cutoff,str) or len(cutoff)>64: raise ValueError()
                stamp=instant(cutoff)
                if stamp.utcoffset() is None or stamp>datetime.now(timezone.utc): raise ValueError()
            except (ValueError,TypeError): raise invalid_request() from None
        if method=='GET' and route==['assessment-selection']:
            return 200,CloudSelection(service,root=source_root).catalog(owner,case)
        if route[0]!='assessments': raise not_found()
        if method=='GET' and route==['assessments']: return 200,service.list(owner,case)
        if method=='POST' and route==['assessments','selected']:
            request=_body(event,StartAssessment)
            if queue is None: raise unavailable()
            delivery=queue() if callable(queue) else queue
            run=CloudSelection(service,root=source_root).admit(owner,case,request)
            delivery.send(owner,case,run['job_id'])
            return 202,run
        if len(route)<2: raise not_found()
        job=route[1]
        if method=='GET' and len(route)==2: return 200,service.read(owner,case,job,cutoff)
        if method=='POST' and route[2:]==['resume']:
            if queue is None: raise unavailable()
            delivery=queue() if callable(queue) else queue
            delivery.send(owner,case,job)
            return 202,service.read(owner,case,job)['job']
        if method=='POST' and route[2:]==['export']:
            request=_body(event,ExportRequest)
            data=service.export(owner,case,job,request.format,cutoff)
            extension='json' if request.format=='json' else 'md'
            filename=f'assessment-{job}.{extension}'
            reference=service.store.objects.save_report(owner,case,'report-'+uuid.uuid4().hex,data)
            return 200,{'url':service.store.objects.download_report(owner,case,reference,filename),'filename':filename}
        if method=='GET' and len(route) in {4,5} and route[2]=='sources':
            if len(route)==5:
                if route[4]!='original': raise not_found()
                # Source scope and bytes are checked before a download is signed.
                source=service.source(owner,case,job,route[3])
                stored=service.store.get(owner,case,'document',route[3])
                if source['document']['kind']=='regulation':
                    service._public_original(owner,case,source)
                    url=service.store.objects.download_extraction(owner,case,stored['original_ref'],'historical-regulation.html')
                    return 200,{'url':url,'filename':'historical-regulation.html'}
                service.source_original(owner,case,job,route[3])
                stored=service._bank_record(owner,case,route[3])
                return 200,{'url':service.store.objects.download(owner,case,stored['original'],stored['filename']),
                            'filename':stored['filename']}
            try:
                value=query.get('offset','0')
                if not isinstance(value,str) or not value.isascii() or not value.isdecimal(): raise ValueError()
                offset=int(value)
            except (ValueError,TypeError): raise invalid_request() from None
            return 200,service.source_page(owner,case,job,route[3],offset=offset)
        if method=='POST' and len(route)==5 and route[2]=='findings' and route[4]=='reviews':
            request=_body(event,ReviewRequest)
            return 201,service.review(owner,case,job,route[3],request).model_dump(mode='json')
        raise not_found()
    except ContractError as error:
        if str(error) in {'record_not_found','job_not_found'}: raise not_found() from None
        if str(error) in {'revision_conflict','idempotency_conflict','immutable_record','record_write_conflict'}:
            raise CaseError(409,'assessment_conflict','The saved assessment or review changed.',
                            'Refresh the saved record before another request.') from None
        raise unavailable() from None
