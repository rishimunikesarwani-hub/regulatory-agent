# Local demo operation

The [D57 contract](spec-local-demo-openai.md) controls OpenAI and Langfuse operation.
This demo uses fictional bank documents and public historical RBI text.
It does not establish current regulatory coverage or production readiness.

## Configuration

1. Open the ignored file `runs/private/local-demo.env`.
2. Put your OpenAI API key in `OPENAI_API_KEY`.
3. Put your Langfuse project public key in `LANGFUSE_PUBLIC_KEY`.
4. Put your Langfuse project secret key in `LANGFUSE_SECRET_KEY`.
5. Set `LANGFUSE_BASE_URL` to your project region URL.
6. Keep `MODEL_PROVIDER=openai`.

Do not send keys in chat or put them in browser configuration.
Langfuse receives measurements without prompts or responses.
The configured OpenAI model is `gpt-4.1-mini-2025-04-14`.
Provider credentials do not prove that the account has available quota.

## Start

Run these commands from the VS5 worktree:

```powershell
cd 'C:\Users\Be Flith Rich\My Project Folder\ET-Hackathon\.worktrees\regulatory-agent-t9-quality'
.venv/Scripts/python.exe ops/run_local_demo.py --check
.venv/Scripts/python.exe ops/run_local_demo.py
```

The second command gives configuration status without key values.
The third command starts the API on port `8150` and the interface on port `5185`.
If either port already has a server, stop the earlier owned server before this command.
The saved database remains `runs/private/slice-05/feedback.sqlite`.

Open [the local app](http://127.0.0.1:5185/) in Chrome.
Select **Continue with local identity**.
Local identity is a development login, not Cognito authentication.

## Demonstration

1. Save a fictional bank case.
2. Upload `data/fixtures/slice-02-policy.txt` as a policy.
3. Confirm that the upload contains fictional data only.
4. Select the saved policy under **Selected historical assessment**.
5. Select **Clause 19(b)**.
6. Set the assessment date to `2024-04-08`.
7. Select **Run selected assessment with live model**.
8. Open the result after the saved job finishes.
9. Open a source citation.
10. Save a human review.
11. Download the JSON or Markdown report.
12. Open the Langfuse project trace list.

The saved run record identifies the OpenAI model and numeric token counts.
Langfuse groups stage measurements by the saved job.
Missing activity records can cause **Needs review** or an evidence gap.
A policy statement does not prove actual control operation.

Use the separate **Run controlled assessment** action for the accepted simulation.
Select **Simulated access rule** to demonstrate fictional version changes and independent review histories.
Do not describe these examples as real RBI amendments.

## Remaining checks

Live OpenAI access and Langfuse delivery need working credentials and a successful demonstration.
An optional trace-export failure does not repeat the assessment.
The mandatory local audit remains available in the saved run record.
AWS deployment, current source verification, and the original model evaluation gates remain pending.
