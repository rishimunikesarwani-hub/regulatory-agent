"""Record safe development release evidence, including failed browser checks."""
from datetime import datetime, timezone
import json
import os
from pathlib import Path

path = Path("runs/releases/development.json")
has_deployment_record = path.exists()
record = json.loads(path.read_text()) if has_deployment_record else {
    "commit": os.environ.get("GITHUB_SHA"), "url": None, "environment": "development",
    "limitations": ["AWS deployment did not finish.", "No production deployment."]}
record.update(recorded_at=datetime.now(timezone.utc).isoformat(),
              integration_checks="passed", deployment_result=os.environ.get("DEPLOYMENT_RESULT", "unknown"),
              browser_checks=os.environ.get("BROWSER_RESULT", "unknown"))
verified = (has_deployment_record and record.get("commit") == os.environ.get("GITHUB_SHA")
            and record.get("environment") == "development" and bool(record.get("url"))
            and record["deployment_result"] == record["browser_checks"] == "success")
record["status"] = "verified_development_slice" if verified else "unverified"
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text(json.dumps(record, indent=2), encoding="utf-8")
