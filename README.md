# The Regulatory Agent

The application connects regulatory requirements to bank controls, evidence, findings, and proposed corrections.

## Start here

Read the [project handbook](docs/guide-start-here.md). It gives links to the five specifications, the decision history, and the test plans.

The private repository is on [GitHub](https://github.com/rishimunikesarwani-hub/regulatory-agent/tree/main).
The local integration folder is `ET-Hackathon\MVP` on branch `main`.
Session A and Session B foundations are integrated.
The combined offline checks passed 60 tests.
The application interface and compliance assessment are not implemented.

Read the [remaining worktree guide](docs/delivery/guide-next-worktrees.md) for task assignments and dependencies.
Use the [local testing guide](docs/delivery/guide-session-b-testing.md) for setup and the terminal demonstration.

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
| src/ | Local contracts and adapters. Application features are pending. |
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
