"""VS2 behavior and ownership contracts through the actual local HTTP application."""
import asyncio
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import tempfile
import unittest
from unittest.mock import patch
from urllib.parse import quote
import zipfile

import httpx
from pypdf import PdfWriter
from pypdf.generic import DecodedStreamObject, DictionaryObject, NameObject

from regulatory_agent.api import create_app


def pdf(text="Fictional bank policy", encrypted=False):
    output = BytesIO()
    writer = PdfWriter()
    page = writer.add_blank_page(612, 792)
    if text:
        page[NameObject("/Resources")] = DictionaryObject({NameObject("/Font"): DictionaryObject({
            NameObject("/F1"): DictionaryObject({NameObject("/Type"): NameObject("/Font"),
                NameObject("/Subtype"): NameObject("/Type1"), NameObject("/BaseFont"): NameObject("/Helvetica")})})})
        stream = DecodedStreamObject()
        stream.set_data(f"BT /F1 12 Tf 30 740 Td ({text}) Tj ET".encode())
        page[NameObject("/Contents")] = writer._add_object(stream)
    if encrypted:
        writer.encrypt("test-fixture-password")
    writer.write(output)
    return output.getvalue()


def docx():
    output = BytesIO()
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/></Types>')
        archive.writestr("word/document.xml", '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body><w:p><w:r><w:t>Fictional policy.</w:t></w:r></w:p><w:p/><w:p><w:r><w:t>Owner is unknown.</w:t></w:r></w:p></w:body></w:document>')
    return output.getvalue()


class DocumentSliceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / "documents.sqlite"
        self.app = self.application("operator-a")
        self.case = self.call("POST", "/api/cases", json={"bank_profile": {"name": "Fictional upload bank"}}).json()["case_id"]
        self.url = f"/api/cases/{self.case}/documents"

    def tearDown(self):
        self.temp.cleanup()

    def application(self, owner):
        return create_app(store=self.path, environment="local", development_user=owner)

    def call(self, method, path, *, app=None, **kwargs):
        async def send():
            async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app or self.app,
                    client=("127.0.0.1", 10000)), base_url="http://127.0.0.1") as client:
                return await client.request(method, path, **kwargs)
        return asyncio.run(send())

    def upload(self, content=b"Fictional policy.\nOwner is unknown.\n", filename="policy.txt", *, source=None, **kwargs):
        headers = {"Content-Type": "application/octet-stream", "X-Filename": quote(filename),
                   "X-Document-Kind": "policy", "X-Synthetic": "true"}
        if source:
            headers["X-Source-Id"] = source
        headers.update(kwargs.pop("headers", {}))
        return self.call("POST", self.url, content=content, headers=headers, **kwargs)

    def test_ct01_supported_files_keep_original_bytes_and_exact_locations(self):
        for name, data, location, text in (
            ("policy.txt", b"Fictional policy.\n\nOwner is unknown.\n", "Line 3", "Owner is unknown."),
            ("controls.csv", b'control,evidence\nreview,"Fictional\nrecord"\n', "Row 2 (lines 2-3)", 'review,"Fictional\nrecord"'),
            ("policy.docx", docx(), "Paragraph 3", "Owner is unknown."),
            ("policy.pdf", pdf(), "Page 1", "Fictional bank policy"),
        ):
            with self.subTest(name=name):
                response = self.upload(data, name)
                self.assertEqual(response.status_code, 201, response.text)
                saved = response.json()
                self.assertTrue(any(p["location"] == location and text in p["text"] for p in saved["passages"]))
                identity = saved["document"]["document_version_id"]
                original = self.call("GET", f"{self.url}/{identity}/original")
                self.assertEqual(original.content, data)
                self.assertEqual(original.headers["cache-control"], "no-store")
                self.assertIn("attachment", original.headers["content-disposition"])

    def test_ct02_documents_reopen_with_a_new_application_instance(self):
        response = self.upload()
        self.assertEqual(response.status_code, 201)
        saved = response.json()
        app = self.application("operator-a")
        listed = self.call("GET", self.url, app=app)
        self.assertEqual(len(listed.json()["sources"]), 1)
        reopened = self.call("GET", self.url + "/" + saved["document"]["document_version_id"], app=app)
        self.assertEqual(reopened.json(), saved)

    def test_ct03_other_owners_and_cases_cannot_read_or_replace_sources(self):
        response = self.upload()
        self.assertEqual(response.status_code, 201)
        saved = response.json()["document"]
        other = self.application("operator-b")
        for path in (self.url, self.url + "/" + saved["document_version_id"],
                     self.url + "/" + saved["document_version_id"] + "/original"):
            self.assertEqual(self.call("GET", path, app=other).status_code, 404)
        self.assertEqual(self.upload(app=other).status_code, 404)
        another = self.call("POST", "/api/cases", json={"bank_profile": {"name": "Another fictional bank"}}).json()["case_id"]
        self.assertEqual(self.call("GET", f"/api/cases/{another}/documents/{saved['document_version_id']}").status_code, 404)
        previous = self.url
        self.url = f"/api/cases/{another}/documents"
        self.assertEqual(self.upload(source=saved["source_id"]).status_code, 404)
        self.url = previous

    def test_ct04_invalid_or_nonfictional_uploads_do_not_create_sources(self):
        for content, filename, headers in ((b"Fictional", "../policy.txt", {}),
                (b"Fictional", "policy.exe", {}), (b"not a pdf", "policy.pdf", {}),
                (b"Fictional", "policy.txt", {"X-Synthetic": "false"}),
                (b"Fictional", "policy.txt", {"X-Document-Kind": "regulation"}),
                (b"\x00\x01", "policy.txt", {})):
            with self.subTest(filename=filename, headers=headers):
                self.assertEqual(self.upload(content, filename, headers=headers).status_code, 422)
        self.assertEqual(self.call("GET", self.url).json()["sources"], [])

    def test_ct05_encrypted_scanned_empty_and_malformed_documents_are_safe_errors(self):
        for content, name in ((pdf(encrypted=True), "encrypted.pdf"), (pdf(text=""), "scan.pdf"),
                (b"", "empty.txt"), (b"PK corrupt data", "invalid.docx"),
                (b'field\n"unterminated', "invalid.csv")):
            with self.subTest(name=name):
                response = self.upload(content, name)
                self.assertEqual(response.status_code, 422)
                self.assertEqual(set(response.json()), {"code", "message", "next_action", "correlation_id"})
                self.assertNotIn(content[:30].decode(errors="replace"), response.text) if content else None

    def test_ct06_file_and_aggregate_limits_reject_without_partial_persistence(self):
        self.assertEqual(self.upload(b"x" * 10_000_001).status_code, 413)
        self.assertEqual(self.upload(b"x" * 400_001).status_code, 422)
        self.assertEqual(self.call("GET", self.url).json()["sources"], [])
        self.assertEqual(self.upload(b"x" * 396_000).status_code, 201)
        self.assertEqual(self.upload(b"y" * 4001).status_code, 422)
        self.assertEqual(len(self.call("GET", self.url).json()["sources"]), 1)

    def test_ct06_document_count_and_replacement_versions_share_the_allowance(self):
        for _ in range(10):
            self.assertEqual(self.upload().status_code, 201)
        self.assertEqual(self.upload().status_code, 422)
        self.assertEqual(len(self.call("GET", self.url).json()["sources"]), 10)

    def test_ct07_replacement_preserves_the_old_version_and_rejected_replacements(self):
        old = self.upload().json()
        newer = self.upload(b"Revised fictional policy.\n", source=old["document"]["source_id"])
        self.assertEqual(newer.status_code, 201)
        self.assertEqual(newer.json()["document"]["source_id"], old["document"]["source_id"])
        self.assertNotEqual(newer.json()["document"]["document_version_id"], old["document"]["document_version_id"])
        self.assertEqual(self.upload(b"\x00", source=old["document"]["source_id"]).status_code, 422)
        self.assertEqual(self.call("GET", self.url + "/" + old["document"]["document_version_id"]).json(), old)

    def test_ct08_concurrent_uploads_cannot_exceed_the_case_count(self):
        for _ in range(9):
            self.assertEqual(self.upload().status_code, 201)
        with ThreadPoolExecutor(max_workers=2) as workers:
            responses = list(workers.map(lambda _: self.upload(), range(2)))
        self.assertEqual(sorted(r.status_code for r in responses), [201, 422])
        self.assertEqual(len(self.call("GET", self.url).json()["sources"]), 10)

    def test_ct09_altered_original_content_is_rejected(self):
        response = self.upload()
        self.assertEqual(response.status_code, 201)
        identity = response.json()["document"]["document_version_id"]
        db = sqlite3.connect(self.path)
        try:
            with db:
                db.execute("UPDATE documents SET original=? WHERE id=?", (b"Altered fictional content", identity))
        finally:
            db.close()
        self.assertEqual(self.call("GET", f"{self.url}/{identity}/original").status_code, 503)

    def test_ct05_timeout_is_a_safe_rejection_without_a_saved_version(self):
        with patch("regulatory_agent.documents.subprocess.run", side_effect=subprocess.TimeoutExpired("extract", 10)):
            response = self.upload()
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()["code"], "extraction_timeout")
        self.assertEqual(self.call("GET", self.url).json()["sources"], [])

    def test_workspace_port_and_upload_headers_have_explicit_loopback_cors(self):
        with patch.dict(os.environ, {"LOCAL_WEB_PORT": "5182"}):
            app = self.application("operator-a")
        response = self.call("OPTIONS", self.url, app=app, headers={"Origin": "http://127.0.0.1:5182",
            "Access-Control-Request-Method": "POST", "Access-Control-Request-Headers": "x-filename,x-document-kind,x-synthetic,x-source-id"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["access-control-allow-origin"], "http://127.0.0.1:5182")
        self.assertEqual(self.call("OPTIONS", self.url, app=app, headers={"Origin": "https://example.com",
            "Access-Control-Request-Method": "POST"}).status_code, 400)


if __name__ == "__main__":
    unittest.main()
