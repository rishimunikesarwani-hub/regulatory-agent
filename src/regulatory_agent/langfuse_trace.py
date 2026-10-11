"""Optional metadata-only tracing. Local audit persistence remains authoritative."""
from functools import lru_cache
import hashlib
import os
from urllib.parse import urlsplit


def configured():
    return os.environ.get('APP_ENV','local') == 'local' and all(os.environ.get(k) for k in
        ('LANGFUSE_PUBLIC_KEY','LANGFUSE_SECRET_KEY','LANGFUSE_BASE_URL'))


@lru_cache(maxsize=1)
def _client():
    from langfuse import Langfuse
    url=urlsplit(os.environ['LANGFUSE_BASE_URL'])
    if url.scheme!='https' or url.username or url.password or url.path not in ('','/') or url.query or url.fragment:
        raise ValueError('langfuse_endpoint_denied')
    return Langfuse(public_key=os.environ['LANGFUSE_PUBLIC_KEY'],secret_key=os.environ['LANGFUSE_SECRET_KEY'],
        base_url=url.geturl(),timeout=3,debug=False,environment='local-fictional-demo',release=os.environ.get('COMMIT_SHA','local'),
        # Only our explicit observations are exported. No automatic HTTP or framework spans.
        should_export_span=lambda span:span.instrumentation_scope.name=='langfuse-sdk')


def start_attempt(record, *, client=None):
    try:
        if client is None:
            if not configured():return None
            client=_client()
        trace_id=hashlib.sha256(record['job_id'].encode()).hexdigest()[:32]
        model=record.get('actual_response_model_id') or record.get('model_id')
        return client.start_observation(name=record['stage_id'],
            as_type='generation' if record['operation']=='model' else 'span',
            trace_context={'trace_id':trace_id}, model=model.removeprefix('openai:') if model else None,
            metadata={'event_id':record['event_id'],'operation':record['operation'],'demo':'fictional'})
    except Exception:
        return None


def export_attempt(record, *, client=None, observation=None):
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
        observation.update(**update); observation.end()
        return True
    except Exception:
        return False


def flush():
    try:
        if configured():_client().flush()
    except Exception:
        pass
