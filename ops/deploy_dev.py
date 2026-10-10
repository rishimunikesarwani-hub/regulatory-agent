"""Deploy the reviewed development slice. Called only by the serialized workflow."""
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
import json
import os
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def command(*args, capture=False):
    return subprocess.run(args, cwd=ROOT, check=True, text=True, encoding="utf-8", capture_output=capture).stdout


def configuration(env):
    required = ("AWS_DEV_ACCOUNT_ID", "AWS_DEV_EXECUTION_ROLE_ARN", "AWS_DEV_ARTIFACT_BUCKET",
                "AWS_DEV_MONTHLY_BUDGET_USD", "AWS_DEV_RUNTIME_ROLE_ARN", "GITHUB_SHA", "GITHUB_OUTPUT")
    if any(not env.get(key) for key in required):
        raise ValueError("Development account, roles, artifact bucket, budget, and commit must be configured")
    account, stack = env["AWS_DEV_ACCOUNT_ID"], env.get("AWS_DEV_STACK", "regulatory-agent-dev-s01")
    if env.get("AWS_REGION") != "ap-south-1" or not re.fullmatch(r"\d{12}", account):
        raise ValueError("A Mumbai development account is necessary")
    if stack != "regulatory-agent-dev-s01" or not re.fullmatch(r"[a-f0-9]{40}", env["GITHUB_SHA"]):
        raise ValueError("Only the specified development stack and exact commit are permitted")
    if not re.fullmatch(rf"arn:aws:iam::{account}:role/[A-Za-z0-9+=,.@_/-]+", env["AWS_DEV_EXECUTION_ROLE_ARN"]):
        raise ValueError("The execution role must belong to the development account")
    if env["AWS_DEV_RUNTIME_ROLE_ARN"] != f"arn:aws:iam::{account}:role/regulatory-agent-dev-case-runtime":
        raise ValueError("The fixed development case runtime role is necessary")
    if not re.fullmatch(r"[a-z0-9][a-z0-9.-]{1,61}[a-z0-9]", env["AWS_DEV_ARTIFACT_BUCKET"]):
        raise ValueError("Invalid artifact bucket")
    try:
        budget = Decimal(env["AWS_DEV_MONTHLY_BUDGET_USD"])
        if not budget.is_finite() or budget <= 0:
            raise ValueError("A positive development budget is necessary")
    except InvalidOperation:
        raise ValueError("Invalid development budget") from None
    return account, stack


def main():
    os.chdir(ROOT)
    account, stack = configuration(os.environ)
    commit = os.environ["GITHUB_SHA"]
    if command("git", "rev-parse", "HEAD", capture=True).strip() != commit:
        raise ValueError("Checkout does not match the tested commit")
    dirty = command("git", "status", "--porcelain", "--untracked-files=all", "--", "src", "ops", ".github", "data/contracts", "pyproject.toml", capture=True)
    if dirty.strip():
        raise ValueError("Release source differs from its commit")
    identity = json.loads(command("aws", "sts", "get-caller-identity", "--output", "json", capture=True))
    if identity["Account"] != account:
        raise ValueError("AWS account mismatch")
    package = ROOT / "runs/private/sam-package"
    package.mkdir(parents=True, exist_ok=True)
    shutil.copytree(ROOT / "src/regulatory_agent", package / "regulatory_agent", dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    shutil.copyfile(ROOT / "ops/requirements.lock", package / "requirements.txt")
    command("sam", "validate", "--lint", "--template-file", "ops/sam-dev.yaml", "--region", "ap-south-1")
    command("sam", "build", "--template-file", "ops/sam-dev.yaml", "--build-dir", "runs/private/sam-build")
    command("sam", "deploy", "--template-file", "runs/private/sam-build/template.yaml", "--stack-name", stack,
            "--s3-bucket", os.environ["AWS_DEV_ARTIFACT_BUCKET"], "--s3-prefix", commit,
            "--role-arn", os.environ["AWS_DEV_EXECUTION_ROLE_ARN"], "--region", "ap-south-1",
            "--capabilities", "CAPABILITY_IAM", "--parameter-overrides", f"CommitSha={commit}",
            f"CaseRuntimeRoleArn={os.environ['AWS_DEV_RUNTIME_ROLE_ARN']}",
            "--no-confirm-changeset", "--no-fail-on-empty-changeset")
    result = json.loads(command("aws", "cloudformation", "describe-stacks", "--stack-name", stack,
                                "--region", "ap-south-1", "--output", "json", capture=True))
    outputs = {value["OutputKey"]: value["OutputValue"] for value in result["Stacks"][0]["Outputs"]}
    if outputs["CommitSha"] != commit:
        raise ValueError("Deployed commit output mismatch")
    dist = ROOT / "src/web/dist"
    config = dict(mode="aws", api_url=outputs["ApiUrl"], cognito_domain=outputs["CognitoDomain"],
                  user_pool_client_id=outputs["UserPoolClientId"], redirect_uri=outputs["FrontendUrl"] + "/", commit_sha=commit)
    (dist / "config.json").write_text(json.dumps(config), encoding="utf-8")
    command("aws", "s3", "sync", str(dist), "s3://" + outputs["FrontendBucket"], "--region", "ap-south-1",
            "--cache-control", "no-cache", "--only-show-errors")
    invalidation = json.loads(command("aws", "cloudfront", "create-invalidation", "--distribution-id", outputs["DistributionId"],
                                     "--paths", "/*", "--output", "json", capture=True))
    command("aws", "cloudfront", "wait", "invalidation-completed", "--distribution-id", outputs["DistributionId"],
            "--id", invalidation["Invalidation"]["Id"])
    record = dict(commit=commit, url=outputs["FrontendUrl"], api_url=outputs["ApiUrl"], environment="development",
                  recorded_at=datetime.now(timezone.utc).isoformat(), status="deployed_pending_browser",
                  integration_checks="passed", browser_checks="pending", stack=stack, region="ap-south-1",
                  limitations=["Fictional cases only.", "Private uploads are disabled.",
                               "Regulatory assessment is not in this slice.", "No production deployment."])
    path = ROOT / "runs/releases/development.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record, indent=2), encoding="utf-8")
    with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as stream:
        stream.write(f"frontend_url={outputs['FrontendUrl']}\n")


if __name__ == "__main__":
    main()
