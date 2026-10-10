$ErrorActionPreference = 'Stop'
Push-Location (Split-Path $PSScriptRoot -Parent)
try {
    uv venv --python 3.12.13 .venv
    if ($LASTEXITCODE -ne 0) { throw 'Python environment creation failed.' }
    uv pip sync --python .venv/Scripts/python.exe ops/requirements.lock
    if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed.' }
    & .venv/Scripts/python.exe -X utf8 ops/check.py
    if ($LASTEXITCODE -ne 0) { throw 'Local checks failed.' }
} finally {
    Pop-Location
}
