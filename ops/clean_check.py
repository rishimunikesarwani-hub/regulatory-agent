"""Verify a clean source copy with a new environment and an empty package cache."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix="regulatory-agent-clean-") as directory:
    target = Path(directory) / "source"
    target.mkdir()
    for name in ("src", "tests", "ops", "data/fixtures", "data/sources", "evals/fixtures"):
        shutil.copytree(ROOT / name, target / name, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    env = {k: v for k, v in os.environ.items() if not k.upper().startswith(("AWS_", "OPENAI_", "ANTHROPIC_"))}
    env["UV_CACHE_DIR"] = str(Path(directory) / "empty-cache")
    env.pop("PYTHONPATH", None)
    commands = [
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", "ops/setup.ps1"],
        [str(target / ".venv/Scripts/python.exe"), "-X", "utf8", "ops/demo.py"],
    ]
    for command in commands:
        print("COMMAND:", " ".join(command), flush=True)
        subprocess.run(command, cwd=target, env=env, check=True)
print("Clean source, fresh environment, and empty package cache: PASS")
