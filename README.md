# Zero-Day Intelligence — GitHub Edition

GitHub-first automated zero-day intelligence pipeline.

## What it does

Every 30 minutes GitHub Actions:
1. Reads configured RSS/API/web discovery sources.
2. Extracts article/advisory URLs and main text.
3. Deduplicates URLs/content.
4. Applies deterministic security relevance rules.
5. Sends only relevant/uncertain items to the configured AI analyzer.
6. Converts the AI result into a validated structured record.
7. Correlates repeated reporting into one internal vulnerability record.
8. Detects lifecycle changes.
9. Generates/updates an Excel register.
10. Sends an alert only when an alert-worthy state transition occurs.
11. Produces a daily digest.

The AI is an analysis component, not the source of truth. Final lifecycle decisions are made by deterministic rules and evidence.

## Important deployment note

This project is designed for GitHub Actions. The repository is the persistent project/data store for the initial version. For larger scale, PostgreSQL/object storage can be added later without changing the intelligence model.

GitHub-hosted runners are ephemeral, so the workflow commits state/report changes back to the repository. Keep the repository private if the intelligence data or configuration is sensitive.

## Setup

1. Extract this ZIP.
2. Create a GitHub repository.
3. Upload the extracted contents while preserving the folder structure.
4. Enable GitHub Actions.
5. Add the required repository secrets/variables described in `docs/GITHUB_SETUP.md`.
6. Run `Zero-Day Monitor` manually once.
7. Check `reports/zero_day_intelligence.xlsx` and `data/*.json`.
8. The scheduled workflow runs every 30 minutes.

## AI provider

The application supports a generic OpenAI-compatible endpoint. Set:
- `AI_ENABLED=true`
- `AI_BASE_URL`
- `AI_API_KEY`
- `AI_MODEL`

If AI is not configured, deterministic triage still runs and records items as `NEEDS_AI` rather than pretending they are zero-days.

Do not put API keys in the repository.

## Current scope

This is a working foundation for the autonomous pipeline. Source definitions are deliberately configurable in `config/sources.yaml`. Add/remove sources without changing the core engine.

It is not a guarantee of complete global zero-day coverage: sources can be delayed, unavailable, paywalled, private, or silent.
