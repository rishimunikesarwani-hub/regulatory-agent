"""Record the final T2 source hashes and verification metadata."""
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
from pathlib import Path
import platform
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from regulatory_agent.contracts import schema_bundle

folder = Path(__file__).parent
green = (folder / "green.txt").read_text(encoding="utf-8")
assert "Ran 59 tests" in green and "\nOK" in green and "FAILED" not in green
clean = (folder / "clean-copy.txt").read_text(encoding="utf-16")
assert "Ran 59 tests" in clean and "empty package cache: PASS" in clean and "FAILED" not in clean
receipt = json.loads((folder / "t1-import.json").read_text(encoding="utf-8"))
for relative, expected in receipt["sha256"].items():
    assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == expected, relative
(folder / "contracts-v1.json").write_text(json.dumps(schema_bundle(), indent=2), encoding="utf-8")
paths = [p for group in ("src/regulatory_agent", "ops", "tests", "docs/delivery")
         for p in (ROOT / group).rglob("*") if p.is_file() and p.suffix in {".py", ".ps1", ".lock", ".md"}]
hashes = {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
assert subprocess.run(["git", "diff", "--exit-code", "--", "AGENTS.md", "README.md", "LOG.md", "pyproject.toml",
                       "docs/product/01_PRD.md", "docs/architecture/02_TECHNICAL_BLUEPRINT.md",
                       "docs/security/03_SECURITY_ACCESS.md", "docs/frontend/04_FRONTEND_SPEC.md",
                       "docs/delivery/05_FEATURE_TICKETS.md", "docs/decisions/gov-decision-log.md"], cwd=ROOT).returncode == 0
result = {"recorded_at": datetime.now(timezone.utc).isoformat(), "python": platform.python_version(),
          "base_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
          "branch": "work/session-b", "tests": {"passed": 59, "failed": 0, "skipped": 0, "fixture": 29, "t2": 30},
          "clean_copy": "passed", "live_model_evaluations": "not run", "cloud_checks": "not run",
          "pending_tickets": ["T3", "T4", "T5", "T6", "T7", "T8", "T9"],
          "integration": "not merged", "sha256": hashes,
          "packages": {d.metadata["Name"]: d.version for d in importlib.metadata.distributions()}}
(folder / "verification.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
print(f"Recorded {len(hashes)} source hashes and the schema bundle.")
