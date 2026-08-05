# ResearchVault

Scrapes a curated list of AI news sites, lab blogs, and research feeds, uses
Claude to judge which articles are actually important, and emails you a daily
digest via SMTP. Runs automatically once a day via GitHub Actions.

## How it works

1. `research_vault/sources.py` lists the RSS feeds to check (news sites, lab
   blogs, arXiv categories).
2. `main.py` fetches all feeds, keeps only articles published in the last
   `LOOKBACK_HOURS` that haven't been seen before (tracked in
   `data/seen_links.json`).
3. The candidate articles are sent to Claude in one batch, which scores each
   for importance and picks the top ones (`research_vault/scorer.py`).
4. The picks are emailed as an HTML digest over SMTP
   (`research_vault/emailer.py`).

## Local setup

```
pip install -r requirements.txt
cp .env.example .env   # fill in your API keys
python main.py
```

You'll need:

- An [Anthropic API key](https://console.anthropic.com/settings/keys)
- An email account to send from over SMTP. No domain of your own is needed —
  Gmail works fine: enable 2-Step Verification, then create an
  [app password](https://myaccount.google.com/apppasswords) and use that as
  `SMTP_PASSWORD` (not your normal Gmail password). See `.env.example` for
  the Gmail/Outlook SMTP settings.

## Running automatically (GitHub Actions)

The workflow at `.github/workflows/daily-digest.yml` runs the digest every day
at 07:00 UTC. To enable it on your fork/repo, add these as **repository
secrets** (Settings → Secrets and variables → Actions):

- `ANTHROPIC_API_KEY`
- `SMTP_HOST`
- `SMTP_PORT`
- `SMTP_USERNAME`
- `SMTP_PASSWORD`
- `DIGEST_TO_EMAIL`

The workflow commits `data/seen_links.json` back to the repo after each run so
articles aren't repeated across days. You can also trigger it manually from
the Actions tab (`workflow_dispatch`).

## Configuration

See `research_vault/config.py` for all tunable settings (lookback window,
how many articles per digest, minimum importance score, which Claude model to
use).