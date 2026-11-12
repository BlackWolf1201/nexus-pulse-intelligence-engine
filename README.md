# NEXUS PULSE Intelligence Engine

Cloud-based editorial intelligence engine for gaming and technology news, rumors, leaks, and verification.

## Project status

**Phase 0 — bootstrap scaffold.** This repository currently contains safe foundations and CI checks only. It does not yet collect real sources, call an AI model, store editorial data, or send notifications.

## Security boundaries

- This repository is public and must contain code only.
- Never commit source registries, collected articles, editorial notes, model feedback, database exports, API tokens, passwords, or Cloudflare credentials.
- Keep production source configuration and editorial records in the private Cloudflare D1 database.
- Keep secrets in GitHub Actions secrets or Cloudflare Worker secrets, never in repository files or workflow logs.
- Workflow logs must contain operational counters only. Do not print article titles, URLs, source lists, article text, API payloads, or credentials.
- Do not connect the NEXUS PULSE public website or change its DNS as part of this project.

## Local development

Requires Python 3.11 or newer.

```bash
python -m venv .venv
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python -m nexus_pulse_intelligence.cli doctor
pytest
ruff check .
```

## GitHub Actions

The workflow in `.github/workflows/ci.yml` runs linting and unit tests on pushes, pull requests, and manual dispatch. It does not run scheduled collection and does not require secrets.

The production cycle will be dispatched by a Cloudflare Cron Worker after the secure dispatch and ingestion interfaces are implemented and tested. No production secrets should be added before that stage.

## Planned architecture

1. Cloudflare Cron Worker — initiates a cycle every 30 minutes.
2. GitHub Actions runner — executes the public Python engine.
3. Private Cloudflare control/ingestion Worker — supplies private source configuration and accepts processed batches.
4. Cloudflare D1 — stores sources, articles, stories, claims, evidence, feedback, and run metadata.
5. Workers AI — performs bounded classification and summarization within the free quota.
6. Private web dashboard and Telegram bot — expose editorial results and alerts.

The 30-minute cadence is a target schedule, not a guarantee of exact start or completion times. Runs must be idempotent and use a persisted cursor so delayed or missed cycles do not lose items.

## Important design rules

- Exact duplicates may be suppressed; related articles must be grouped, not deleted.
- A rumor repeated by several sites is not automatically corroborated: source independence and original evidence must be assessed.
- AI output is an editorial aid, not proof. Official confirmation requires attributable official evidence.
- Every run must be idempotent, bounded by time and item limits, and safe to retry.
- Free-tier quotas must be enforced in code. No billing upgrade or paid fallback is permitted.

## License

No open-source license has been added. Public visibility does not itself grant permission to reuse this code.
