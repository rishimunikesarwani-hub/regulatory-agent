"""VS1-CT01 through VS1-CT04: local case API and persistent storage."""
import asyncio
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from regulatory_agent.api import create_app
from regulatory_agent.cases import CaseError, CaseService, SQLiteCases
from regulatory_agent.contracts import CaseList, CaseRecord, SafeError
from regulatory_agent.local import Store


async def request(app, method="GET", path="/api/cases", body=None, peer="127.0.0.1", headers=()):
    payload = body if isinstance(body, bytes) else json.dumps(body).encode() if body is not None else b""
    messages = []
    sent = False

    async def receive():
        nonlocal sent
        if not sent:
            sent = True
            return {"type": "http.request", "body": payload, "more_body": False}
        await asyncio.Event().wait()

    async def send(message):
        messages.append(message)

    await app({"type": "http", "asgi": {"version": "3.0"}, "http_version": "1.1",
               "method": method, "scheme": "http", "path": path, "raw_path": path.encode(),
               "query_string": b"", "root_path": "", "client": (peer, 10000),
               "server": ("127.0.0.1", 8110),
               "headers": [(b"content-type", b"application/json"), *headers]}, receive, send)
    start = next(m for m in messages if m["type"] == "http.response.start")
    content = b"".join(m.get("body", b"") for m in messages if m["type"] == "http.response.body")
    return start["status"], dict(start["headers"]), json.loads(content)


class CaseSliceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / "cases.db"
        self.store = Store(self.path)
        self.service = CaseService(SQLiteCases(self.store))
        self.app = create_app(self.service, environment="local", development_user="operator-a", commit_sha="test-sha")

    def tearDown(self):
        self.temp.cleanup()

    def call(self, **kwargs):
        return asyncio.run(request(self.app, **kwargs))

    def test_vs1_ct01_create_list_and_reopen_through_shared_schemas(self):
        status, headers, data = self.call(method="POST", body={"bank_profile": {"name": " Fictional Bank ", "active": True}})
        self.assertEqual(status, 201)
        record = CaseRecord.model_validate(data)
        self.assertEqual(record.bank_profile["name"], "Fictional Bank")
        self.assertEqual(record.owner_id, "operator-a")
        self.assertTrue(record.synthetic)
        self.assertTrue(record.created_at.endswith("Z"))
        self.assertEqual(headers[b"cache-control"], b"no-store")
        listed = self.call()[2]
        self.assertEqual(CaseList.model_validate(listed).cases, [record])
        self.assertEqual(self.call(path=f"/api/cases/{record.case_id}")[2], data)

    def test_vs1_ct02_fresh_service_reopens_committed_case(self):
        created = self.service.create("operator-a", {"bank_profile": {"name": "Synthetic Bank"}})
        restarted = CaseService(SQLiteCases(Store(self.path)))
        self.assertEqual(restarted.read("operator-a", created.case_id), created)
        self.assertEqual(restarted.list("operator-a").cases, [created])

    def test_vs1_ct02_new_python_process_reopens_case(self):
        created = self.service.create("operator-a", {"bank_profile": {"name": "Persistent fixture"}})
        code = ("from regulatory_agent.cases import CaseService, SQLiteCases; import sys; "
                "print(CaseService(SQLiteCases(sys.argv[1])).read('operator-a', sys.argv[2]).model_dump_json())")
        completed = subprocess.run([sys.executable, "-c", code, str(self.path), created.case_id],
                                   capture_output=True, text=True, encoding="utf-8", env=os.environ.copy(), check=True)
        self.assertEqual(CaseRecord.model_validate_json(completed.stdout), created)

    def test_vs1_ct03_owner_scope_and_missing_case_have_same_404_shape(self):
        case = self.service.create("operator-b", {"bank_profile": {"name": "Other Fictional Bank"}})
        self.assertEqual(self.call()[2], {"cases": []})
        for identity in (case.case_id, "absent-case"):
            status, headers, body = self.call(path=f"/api/cases/{identity}")
            self.assertEqual(status, 404)
            self.assertEqual(SafeError.model_validate(body).code, "case_not_found")
            self.assertEqual(headers[b"cache-control"], b"no-store")

    def test_vs1_ct03_development_identity_requires_loopback_and_explicit_user(self):
        for peer in ("192.0.2.1", "10.0.0.2"):
            status, _, body = self.call(peer=peer, headers=((b"x-forwarded-for", b"127.0.0.1"),))
            self.assertEqual(status, 401)
            self.assertEqual(body["code"], "authentication_required")
        no_identity = create_app(self.service, environment="local", development_user="")
        self.assertEqual(asyncio.run(request(no_identity))[0], 401)
        self.assertEqual(self.call(peer="::1")[0], 200)
        with self.assertRaises(ValueError):
            create_app(self.service, environment="aws", development_user="operator-a")

    def test_vs1_ct04_invalid_profiles_forged_fields_and_real_data_are_rejected(self):
        invalid = [{}, {"bank_profile": {}}, {"bank_profile": {"name": "  "}},
                   {"bank_profile": {"name": True}}, {"bank_profile": {"name": "a" * 201}},
                   {"bank_profile": {"name": "Bank", "count": 7}},
                   {"bank_profile": {"name": "Bank"}, "owner_id": "operator-b"},
                   {"bank_profile": {"name": "Bank"}, "synthetic": False}]
        for body in invalid:
            with self.subTest(body=body):
                status, headers, error = self.call(method="POST", body=body)
                self.assertEqual(status, 422)
                SafeError.model_validate(error)
                self.assertEqual(headers[b"cache-control"], b"no-store")
        self.assertEqual(self.call()[2], {"cases": []})

    def test_vs1_ct04_storage_failure_returns_safe_503_and_no_success(self):
        class FailingRepository:
            def save(self, record):
                raise RuntimeError("private-bank-secret storage credential")

        self.app = create_app(CaseService(FailingRepository()), environment="local", development_user="operator-a")
        status, headers, body = self.call(method="POST", body={"bank_profile": {"name": "Fictional Bank"}})
        self.assertEqual(status, 503)
        self.assertEqual(body["code"], "storage_unavailable")
        self.assertNotIn("secret", json.dumps(body))
        self.assertEqual(headers[b"cache-control"], b"no-store")

    def test_existing_store_callers_and_profile_shape_remain_unchanged(self):
        self.store.create_case("operator-a", "legacy", {"name": "Existing fixture"})
        record = self.service.create("operator-a", {"bank_profile": {"name": "API fixture"}})
        self.store.authorize("operator-a", record.case_id)
        with self.store.transaction() as db:
            profile = json.loads(db.execute("SELECT profile FROM cases WHERE id=?", (record.case_id,)).fetchone()[0])
        self.assertEqual(profile, {"name": "API fixture"})
        self.assertEqual([c.case_id for c in self.service.list("operator-a").cases], [record.case_id])

    def test_health_is_public_and_contains_no_identity_or_profile(self):
        status, _, body = self.call(path="/api/health", peer="192.0.2.1")
        self.assertEqual(status, 200)
        self.assertEqual(body, {"status": "ok", "commit_sha": "test-sha"})

    def test_local_cors_allows_only_the_configured_frontend_origin(self):
        for origin, permitted in ((b"http://127.0.0.1:5173", True), (b"https://untrusted.example", False)):
            _, headers, _ = self.call(headers=((b"origin", origin),))
            self.assertEqual(headers.get(b"access-control-allow-origin"), origin if permitted else None)
            self.assertNotIn(b"access-control-allow-credentials", headers)

    def test_authentication_precedes_invalid_request_validation(self):
        for payload in ({}, b"{"):
            status, _, body = self.call(method="POST", body=payload, peer="192.0.2.1")
            self.assertEqual(status, 401)
            self.assertEqual(body["code"], "authentication_required")

    def test_unknown_routes_use_safe_error_and_service_rejects_forged_repository_record(self):
        status, headers, body = self.call(path="/api/no-such-route")
        self.assertEqual(status, 404)
        SafeError.model_validate(body)
        self.assertEqual(headers[b"cache-control"], b"no-store")
        record = self.service.create("operator-b", {"bank_profile": {"name": "Other Fictional Bank"}})

        class ForgedRepository:
            def read(self, owner, identity):
                return record

        with self.assertRaises(CaseError) as error:
            CaseService(ForgedRepository()).read("operator-a", record.case_id)
        self.assertEqual(error.exception.status_code, 404)


if __name__ == "__main__":
    unittest.main()
