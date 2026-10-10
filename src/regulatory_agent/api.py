"""Local FastAPI entry point for the case slice. AWS uses aws_cases.handler."""
import os

from fastapi import Depends, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from starlette.concurrency import run_in_threadpool
from urllib.parse import quote
from starlette.exceptions import HTTPException

from .cases import (CaseError, CaseService, SQLiteCases, authenticated_owner, authentication_error,
                    error_body, invalid_request, not_found, unavailable)
from .contracts import CaseCreate, CaseList, CaseRecord, LocalIdentity
from .documents import Documents, rejected


def create_app(service=None, *, store=None, environment=None, development_user=None, commit_sha=None):
    environment = environment if environment is not None else os.environ.get("APP_ENV", "local")
    development_user = development_user if development_user is not None else os.environ.get("DEVELOPMENT_USER", "")
    commit_sha = commit_sha if commit_sha is not None else os.environ.get("COMMIT_SHA", "local")
    if environment != "local" and development_user:
        raise ValueError("development_identity_disabled_outside_local")
    app = FastAPI(title="The Regulatory Agent", docs_url=None, redoc_url=None, openapi_url=None)
    documents = None
    @app.middleware("http")
    async def private_headers(request, call_next):
        try:
            if request.url.path != "/api/health" and request.method != "OPTIONS":
                owner(request)
            response = await call_next(request)
        except CaseError as error:
            response = JSONResponse(error_body(error), status_code=error.status_code)
        except Exception:
            response = JSONResponse(error_body(unavailable()), status_code=503)
        response.headers["Cache-Control"] = "no-store"
        response.headers["X-Content-Type-Options"] = "nosniff"
        return response

    @app.exception_handler(CaseError)
    async def case_error(request, error):
        return JSONResponse(error_body(error), status_code=error.status_code)

    @app.exception_handler(RequestValidationError)
    async def validation_error(request, error):
        return JSONResponse(error_body(invalid_request()), status_code=422)

    @app.exception_handler(HTTPException)
    async def route_error(request, error):
        return JSONResponse(error_body(not_found()), status_code=404)

    def owner(request: Request):
        try:
            peer = request.client.host if request.client else ""
            return authenticated_owner(LocalIdentity.resolve(environment, peer, development_user))
        except ValueError:
            raise authentication_error() from None

    def cases():
        nonlocal service
        if service is None:
            try:
                service = CaseService(SQLiteCases(store if store is not None else os.environ.get("CASES_DB_PATH", "runs/local/cases.db")))
            except Exception:
                raise unavailable() from None
        return service

    @app.get("/api/health")
    def health():
        return {"status": "ok", "commit_sha": commit_sha}

    @app.post("/api/cases", response_model=CaseRecord, status_code=201)
    def create_case(body: CaseCreate, identity=Depends(owner)):
        return cases().create(identity, body)

    @app.get("/api/cases", response_model=CaseList)
    def list_cases(identity=Depends(owner)):
        return cases().list(identity)

    @app.get("/api/cases/{case_id}", response_model=CaseRecord)
    def read_case(case_id: str, identity=Depends(owner)):
        return cases().read(identity, case_id)

    def sources(identity, case_id):
        nonlocal documents
        cases().read(identity, case_id)
        if documents is None:
            documents = Documents(cases())
        return documents

    @app.get("/api/cases/{case_id}/documents")
    def list_documents(case_id: str, identity=Depends(owner)):
        return sources(identity, case_id).list(identity, case_id)

    @app.post("/api/cases/{case_id}/documents", status_code=201)
    async def upload_document(case_id: str, request: Request, identity=Depends(owner)):
        service = sources(identity, case_id)
        data = bytearray()
        async for part in request.stream():
            if len(data) + len(part) > 10_000_000:
                raise rejected(oversized=True)
            data.extend(part)
        return await run_in_threadpool(service.upload, identity, case_id, request.headers, bytes(data))

    @app.get("/api/cases/{case_id}/documents/{version_id}")
    def read_document(case_id: str, version_id: str, identity=Depends(owner)):
        return sources(identity, case_id).read(identity, case_id, version_id)

    @app.get("/api/cases/{case_id}/documents/{version_id}/original")
    def original_document(case_id: str, version_id: str, identity=Depends(owner)):
        data, filename = sources(identity, case_id).read(identity, case_id, version_id, original=True)
        return Response(data, media_type="application/octet-stream",
                        headers={"Content-Disposition": "attachment; filename*=UTF-8''" + quote(filename)})

    if environment == "local":
        web_port = os.environ.get("LOCAL_WEB_PORT", "5173")
        if not web_port.isascii() or not web_port.isdecimal() or not 1 <= int(web_port) <= 65535:
            raise ValueError("invalid_loopback_web_port")
        app.add_middleware(CORSMiddleware, allow_origins=[f"http://127.0.0.1:{web_port}"],
                           allow_methods=["GET", "POST", "OPTIONS"],
                           allow_headers=["Authorization", "Content-Type", "X-Filename", "X-Document-Kind", "X-Synthetic", "X-Source-Id"])
    return app


app = create_app()
