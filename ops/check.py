"""Run default checks in an isolated Python worker with external networking disabled."""
import argparse
import json
import os
from pathlib import Path
import platform
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def environment():
    env = {k: v for k, v in os.environ.items()
           if not k.upper().startswith(("AWS_", "OPENAI_", "ANTHROPIC_", "AZURE_", "BEDROCK_"))}
    env["PYTHONPATH"] = os.pathsep.join(str(ROOT / p) for p in ("ops/offline", "src", "."))
    env["PYTHONNOUSERSITE"] = "1"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return env


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pattern", default="test_*.py")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    if platform.python_version() != "3.12.13":
        print("Use Python 3.12.13 in the project .venv.")
        return 2
    run = subprocess.run([sys.executable, "-X", "utf8", "-m", "unittest", "discover", "-s", "tests", "-p", args.pattern, "-v"],
                         cwd=ROOT, env=environment(), text=True, encoding="utf-8", capture_output=True)
    output = run.stdout + run.stderr
    print(output, end="")
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(output, encoding="utf-8")
    return run.returncode


if __name__ == "__main__":
    raise SystemExit(main())
