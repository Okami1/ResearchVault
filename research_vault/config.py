import os

from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
ANTHROPIC_MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-opus-5")

# SMTP settings for sending the digest through an existing email account
# (e.g. Gmail with an app password) rather than a domain-verified sender.
SMTP_HOST = os.environ.get("SMTP_HOST")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USERNAME = os.environ.get("SMTP_USERNAME")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")

DIGEST_FROM_EMAIL = os.environ.get("DIGEST_FROM_EMAIL", SMTP_USERNAME)
DIGEST_TO_EMAIL = os.environ.get("DIGEST_TO_EMAIL")

# How far back to look for new articles on each run. Generous window to
# tolerate cron jitter and feeds with stale/delayed publish dates.
LOOKBACK_HOURS = int(os.environ.get("LOOKBACK_HOURS", "30"))

# Max number of articles to include in the digest email.
TOP_N_ARTICLES = int(os.environ.get("TOP_N_ARTICLES", "10"))

# Max number of candidate articles to pull from any single source per run.
# High-volume feeds (e.g. arXiv listing feeds) publish far more than anyone
# can triage; keep the most recent N and let scoring pick from there.
MAX_ARTICLES_PER_SOURCE = int(os.environ.get("MAX_ARTICLES_PER_SOURCE", "25"))

# Minimum importance score (1-10) for an article to be eligible for the digest.
MIN_IMPORTANCE_SCORE = int(os.environ.get("MIN_IMPORTANCE_SCORE", "5"))

SEEN_STORE_PATH = os.environ.get("SEEN_STORE_PATH", "data/seen_links.json")

# How long to remember a link as "seen" before it's pruned from the store.
SEEN_RETENTION_DAYS = int(os.environ.get("SEEN_RETENTION_DAYS", "14"))
