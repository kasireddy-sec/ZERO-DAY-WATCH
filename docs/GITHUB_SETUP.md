# GitHub setup

## Repository

Create a repository and upload the extracted project contents. Do NOT upload the ZIP as the repository contents.

Recommended: private repository if this will contain internal intelligence.

## Actions permissions

The workflow needs to commit updated state/report files. In repository settings:

Settings → Actions → General → Workflow permissions → Read and write permissions.

The workflow also explicitly requests `contents: write`.

GitHub's built-in `GITHUB_TOKEN` is preferred for repository operations.

## AI configuration

Add repository secrets:

- `AI_API_KEY` — API key for the selected OpenAI-compatible provider.
- `TELEGRAM_BOT_TOKEN` — optional.
- `TELEGRAM_CHAT_ID` — optional.

Add repository variables:

- `AI_ENABLED` = `true`
- `AI_BASE_URL` = provider endpoint
- `AI_MODEL` = model name

The code does not hard-code a provider.

## First run

Actions → Zero-Day Monitor → Run workflow.

Use `dry_run=true` for the first test. It will collect and analyze without sending alerts.

Then run with `dry_run=false`.

## Schedule

The monitor workflow is scheduled for every 30 minutes. GitHub scheduled workflows can be delayed under platform load, so this should be treated as periodic polling rather than a hard real-time SLA.

## Daily digest

The digest workflow runs once per day and reads the repository state.

## Secrets

Never place API keys, Telegram tokens, passwords, or client data in:
- source files
- YAML configuration
- Excel
- commit history

Use GitHub Secrets.
