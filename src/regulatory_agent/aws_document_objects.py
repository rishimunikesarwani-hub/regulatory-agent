"""Case-authorized Mumbai S3 transfers. Cloud upload records and routes bind these operations."""
import base64
import hashlib
import json
import re
from urllib.parse import quote, urlsplit

from .cases import not_found, unavailable
from .contracts import UploadAuthorization
from .documents import upload_request, rejected
from .local import identifier


class S3DocumentObjects:
    def __init__(self, cases, client, bucket, account):
        if client.meta.region_name != 'ap-south-1' or client.meta.endpoint_url != 'https://s3.ap-south-1.amazonaws.com':
            raise ValueError('mumbai_s3_client_required')
        if not isinstance(account, str) or not re.fullmatch(r'\d{12}', account) or not isinstance(bucket, str) or not bucket.strip():
            raise ValueError('invalid_storage_configuration')
        self.cases, self.client, self.bucket, self.account = cases, client, bucket, account

    def _key(self, owner, case, upload):
        self.cases.read(owner, case)
        try:
            identifier(upload)
        except (ValueError, TypeError):
            raise not_found() from None
        return f'owners/{owner}/cases/{case}/uploads/{upload}'

    def _ready(self):
        args = {'Bucket': self.bucket, 'ExpectedBucketOwner': self.account}
        if self.client.get_bucket_location(**args).get('LocationConstraint') != 'ap-south-1':
            raise unavailable()
        if self.client.get_bucket_versioning(**args).get('Status') != 'Enabled':
            raise unavailable()

    def _target(self, url):
        parsed = urlsplit(url)
        if (parsed.scheme != 'https' or parsed.hostname != f'{self.bucket}.s3.ap-south-1.amazonaws.com'
                or parsed.username or parsed.password or parsed.port not in {None,443}):
            raise unavailable()
        return url

    @staticmethod
    def _length(size):
        if type(size) is not int or not 0 < size <= 10_000_000:
            raise rejected(oversized=type(size) is int and size > 10_000_000)
        return size

    def grant(self, owner, case, upload, headers, size):
        key = self._key(owner, case, upload)
        upload_request(headers, size)
        self._ready()
        fields = {'Content-Type': 'application/octet-stream', 'x-amz-server-side-encryption': 'AES256'}
        grant = self.client.generate_presigned_post(Bucket=self.bucket, Key=key, Fields=fields,
            Conditions=[['content-length-range', size, size], *({name: value} for name, value in fields.items())],
            ExpiresIn=300)
        expiration = json.loads(base64.b64decode(grant['fields']['policy']))['expiration']
        authorization = UploadAuthorization(upload_id=upload, destination=self._target(grant['url']), expires_at=expiration)
        return {'authorization': authorization.model_dump(), 'fields': grant['fields']}

    def _bytes(self, key, version, size):
        response = self.client.get_object(Bucket=self.bucket, Key=key, VersionId=version, ExpectedBucketOwner=self.account)
        body = response['Body']
        try:
            if response.get('ContentLength') != size or response.get('VersionId') != version:
                raise unavailable()
            data = body.read(size + 1)
            if len(data) != size:
                raise unavailable()
            return data
        finally:
            body.close()

    def pin(self, owner, case, upload, size):
        key = self._key(owner, case, upload)
        self._length(size)
        self._ready()
        head = self.client.head_object(Bucket=self.bucket, Key=key, ExpectedBucketOwner=self.account)
        version = head.get('VersionId')
        if not version or version == 'null' or head.get('ServerSideEncryption') != 'AES256':
            raise unavailable()
        if head.get('ContentLength') != size:
            raise rejected('uploaded_size_mismatch')
        data = self._bytes(key, version, size)
        return {'upload_id': upload, 'key': key, 'version_id': version, 'size_bytes': size,
                'sha256': hashlib.sha256(data).hexdigest()}, data

    def _reference(self, owner, case, reference, limit):
        self.cases.read(owner, case)
        if not isinstance(reference, dict):
            raise not_found()
        key = self._key(owner, case, reference.get('upload_id'))
        version, digest = reference.get('version_id'), reference.get('sha256')
        if reference.get('key') != key or not isinstance(version, str) or not version or version == 'null' or \
                not isinstance(digest, str) or not re.fullmatch(r'[a-f0-9]{64}', digest):
            raise not_found()
        size = reference.get('size_bytes')
        if type(size) is not int or not 0 < size <= limit:
            raise unavailable()
        return key,version,size

    def _read(self, owner, case, reference, limit):
        key,version,size=self._reference(owner,case,reference,limit)
        self._ready()
        data = self._bytes(key, version, size)
        if hashlib.sha256(data).hexdigest() != reference['sha256']:
            raise unavailable()
        return data

    def read(self, owner, case, reference):
        return self._read(owner, case, reference, 10_000_000)

    def save_extraction(self, owner, case, upload, data):
        key = self._key(owner, case, upload + '-extracted')
        # Parser permits at most 200,000 nonempty passages within 400,000 text bytes.
        # Their location metadata and escaped JSON fit below this internal artifact read bound.
        if not isinstance(data, bytes) or not 0 < len(data) <= 32_000_000:
            raise unavailable()
        self._ready()
        result = self.client.put_object(Bucket=self.bucket, Key=key, Body=data, ContentType='application/json',
                                       ServerSideEncryption='AES256', ExpectedBucketOwner=self.account)
        version = result.get('VersionId')
        if not version or version == 'null' or result.get('ServerSideEncryption') != 'AES256':
            raise unavailable()
        return {'upload_id': upload + '-extracted', 'key': key, 'version_id': version,
                'size_bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

    def read_extraction(self, owner, case, reference):
        self.cases.read(owner, case)
        if not isinstance(reference, dict) or not str(reference.get('upload_id', '')).endswith('-extracted'):
            raise not_found()
        return self._read(owner, case, reference, 32_000_000)

    def download(self, owner, case, reference, filename):
        self.cases.read(owner, case)
        upload_request({'x-filename': quote(filename, safe=''), 'x-document-kind': 'policy', 'x-synthetic': 'true'}, reference.get('size_bytes'))
        self.read(owner, case, reference)
        return self._signed(reference,filename)

    def _signed(self, reference, filename):
        return self._target(self.client.generate_presigned_url('get_object', Params={
            'Bucket': self.bucket, 'Key': reference['key'], 'VersionId': reference['version_id'],
            'ExpectedBucketOwner': self.account, 'ResponseContentType': 'application/octet-stream',
            'ResponseContentDisposition': "attachment; filename*=UTF-8''" + quote(filename, safe='')}, ExpiresIn=300))

    def download_extraction(self, owner, case, reference, filename):
        self.read_extraction(owner,case,reference)
        return self._signed(reference,filename)

    def save_report(self, owner, case, identity, data):
        if not isinstance(identity,str) or not identity.startswith('report-'): raise not_found()
        key=self._key(owner,case,identity+'-report')
        if not isinstance(data,bytes) or not 0<len(data)<=128_000_000: raise unavailable()
        self._ready(); digest=hashlib.sha256(data).digest(); checksum=base64.b64encode(digest).decode()
        result=self.client.put_object(Bucket=self.bucket,Key=key,Body=data,ContentType='application/octet-stream',
            ServerSideEncryption='AES256',ExpectedBucketOwner=self.account,ChecksumSHA256=checksum)
        version=result.get('VersionId')
        if not isinstance(version,str) or not version or version=='null' or result.get('ServerSideEncryption')!='AES256' or \
                result.get('ChecksumSHA256')!=checksum: raise unavailable()
        return {'upload_id':identity+'-report','key':key,'version_id':version,'size_bytes':len(data),'sha256':digest.hex()}

    def download_report(self, owner, case, reference, filename):
        key,version,size=self._reference(owner,case,reference,128_000_000)
        identity=reference['upload_id']
        if not identity.startswith('report-') or not identity.endswith('-report'): raise not_found()
        self._ready()
        head=self.client.head_object(Bucket=self.bucket,Key=key,VersionId=version,ExpectedBucketOwner=self.account,ChecksumMode='ENABLED')
        checksum=base64.b64encode(bytes.fromhex(reference['sha256'])).decode()
        if head.get('VersionId')!=version or head.get('ContentLength')!=size or head.get('ServerSideEncryption')!='AES256' or \
                head.get('ChecksumSHA256')!=checksum or head.get('ChecksumType','FULL_OBJECT')!='FULL_OBJECT': raise unavailable()
        return self._signed(reference,filename)
