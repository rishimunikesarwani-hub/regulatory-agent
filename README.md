# The Regulatory Agent

The application connects regulatory requirements to bank controls, evidence, findings, and proposed corrections.

## Start here

Read the [project handbook](docs/guide-start-here.md). It links the five specifications, the decision history, and the test plans.

| Item | Decision |
|---|---|
| Submission | 10 October 2026. |
| Internal readiness target | 9 October |
| First domain | IT controls in Indian commercial banks |
| Hackathon target | F3/D2. |
| Hosting | Cloud-native AWS architecture |
| Private data processing | India only |
| Development | Local automated tests. Separate checks for live AWS services and the actual model. |
| Data |  Demo documents and authorized user uploads |
| Budget | Credits available / flexible. |

## Development procedure

1. Specify the functionality.
2. Write a test that fails for the missing behavior.
3. Implement the behavior.
4. Refactor the code without changing the behavior.
5. Do the applicable verification.

Every functionality needs a requirement, an acceptance criteria, and a verification result.

## Project folders

| Folder | Contents |
|---|---|
| docs/ | Specifications, decisions, and verification plans |
| src/ | Application code after development starts |
| tests/ | Software correctness tests |
| evals/ | AI quality cases and evaluation tools |
| ops/ | Infrastructure configuration and local verification commands |
| data/ | Public source copies and clearly synthetic test data |
| runs/ | Dated verification and evaluation records |

Do not put real bank files in version control.

Keep the [source brief](../hackthon_data/6ab20c4818adf_et_hackathon_detailed_problem_statements_branded.pdf) outside the application folder.
The [PRD](docs/product/01_PRD.md) records its page references and file hash.

Read [AGENTS.md](AGENTS.md) before changes. Read [LOG.md](LOG.md) to continue the work.

## Document language

Use ASD-STE100 Simplified Technical English for all project Markdown.
Read the [language guide](docs/guide-ste100-writing.md).
Full dictionary and approved-meaning compliance remains unverified.
