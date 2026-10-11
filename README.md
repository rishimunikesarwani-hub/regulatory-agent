# The Regulatory Agent

The application connects regulatory requirements to bank controls, evidence, findings, and proposed corrections.

## Run the local demo

The local application supports fictional document uploads, historical assessments, source citations, saved reviews, and report downloads.
Live assessments need your own OpenAI API key with available API credit.
Langfuse Cloud keys are optional. AWS credentials are not necessary for this local mode.

Use Windows PowerShell with `uv` and Node.js `24.18.0` installed.
Run these commands from the downloaded repository folder:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ops/setup.ps1
Push-Location src/web
npm ci
Pop-Location
New-Item -ItemType Directory -Force runs/private | Out-Null
if (-not (Test-Path -LiteralPath runs/private/local-demo.env)) { Copy-Item .env.example runs/private/local-demo.env }
notepad runs/private/local-demo.env
```

Set `OPENAI_API_KEY` in the private file.
Keep `MODEL_PROVIDER=openai`.
The template contains no credentials. Git excludes the private file and local database.

```powershell
.venv/Scripts/python.exe ops/run_local_demo.py --check
.venv/Scripts/python.exe ops/run_local_demo.py
```

Open [the local application](http://127.0.0.1:5185/).
Configuration checks do not verify API credit or dispatch model requests.
Use fictional bank documents only in this local OpenAI mode.

The [local guide](docs/delivery/guide-local-demo.md) gives optional tracing settings and separate port and database settings.
AWS deployment, current regulatory-source coverage, and independent model quality remain unverified.

## Start here

Read the [project handbook](docs/guide-start-here.md). It gives links to the five specifications, the decision history, and the test plans.

The private repository is on [GitHub](https://github.com/rishimunikesarwani-hub/regulatory-agent/tree/main).
Session A and Session B foundations are integrated.
The first slice has a browser interface, a case API, and persistent local storage.
The local user can sign in, make a fictional case, save it, and reopen it.
The [verification records](runs/2026-10-10-autonomous-build/) contain the test results.

AWS templates and the development release pipeline are prepared.
AWS deployment and application acceptance remain unverified. The user deferred AWS work while local development continues.
The eight assessment features and their quality requirements remain in scope.

Use the [first-slice guide](docs/delivery/guide-slice-01-development.md) for local setup and AWS preparation.
Read the [worktree guide](docs/delivery/guide-next-worktrees.md) for ownership and delivery order.

| Item | Decision |
|---|---|
| Submission | 10 October 2026. |
| Internal readiness target | 9 October |
| First domain | IT controls in Indian commercial banks |
| Hackathon target | F3/D2. |
| Hosting | Cloud-native AWS architecture |
| Private data processing | India only |
| Development | Local automated tests. Do checks of live AWS services and the model independently. |
| Data | Demo documents and authorized user uploads |
| Budget | Credits available / flexible. |

## Development procedure

1. Write the function specification.
2. Write a test that fails for the missing behavior.
3. Write the code for that behavior.
4. Refactor the code without a change to the behavior.
5. Do the applicable verification.

Each function must have a requirement, an acceptance criterion, and a verification result.

## Project folders

| Folder | Contents |
|---|---|
| docs/ | Specifications, decisions, and verification plans |
| src/ | Shared contracts, application services, AWS adapters, and the browser interface |
| tests/ | Tests for correct software behavior |
| evals/ | AI quality cases and evaluation tools |
| ops/ | Infrastructure configuration and local verification commands |
| data/ | Public source copies and clearly synthetic test data |
| runs/ | Dated verification and evaluation records |

Do not put bank files in version control unless they are synthetic.

Keep the [source brief](../hackthon_data/6ab20c4818adf_et_hackathon_detailed_problem_statements_branded.pdf) outside the application folder.
The [PRD](docs/product/01_PRD.md) records its page references and file hash.

Read [AGENTS.md](AGENTS.md) before changes. Read [LOG.md](LOG.md) to continue the work.

## Document language

Use ASD-STE100 Simplified Technical English for all project Markdown.
Read the [language guide](docs/guide-ste100-writing.md).
The language review includes selected dictionary entries and their approved meanings.
It is not a full compliance assessment.
