"""Copy the verified T1 handoff without changing Session A."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parents[2]
source = root.parent / "regulatory-agent-session-a"
manifest_path = "data/fixtures/freeze-manifest.json"
manifest_bytes = (source / manifest_path).read_bytes()
manifest = json.loads(manifest_bytes)
files = {}
for name, expected in manifest["sha256"].items():
    content = (source / name).read_bytes()
    assert hashlib.sha256(content).hexdigest() == expected, name
    files[name] = content
assert (source / manifest_path).read_bytes() == manifest_bytes
files[manifest_path] = manifest_bytes
for name in ("ops/session_a_fixtures.py", "tests/test_session_a_fixtures.py",
             "docs/delivery/spec-session-a-foundation.md"):
    files[name] = (source / name).read_bytes()
for name, content in files.items():
    target = root / name
    if target.exists():
        assert target.read_bytes() == content, f"Existing content differs: {name}"
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
receipt = {"source_worktree": str(source), "scope": "T1 handoff copy; no source edits",
           "sha256": {n: hashlib.sha256(b).hexdigest() for n, b in files.items()}}
(Path(__file__).parent / "t1-import.json").write_text(json.dumps(receipt, indent=2), encoding="utf-8")
print(f"Verified and copied {len(files)} T1 files. Held-out answers were not used for implementation.")
