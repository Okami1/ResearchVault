import logging

from research_vault.config import LOOKBACK_HOURS, MAX_ARTICLES_PER_SOURCE, SEEN_RETENTION_DAYS, SEEN_STORE_PATH
from research_vault.emailer import send_digest
from research_vault.fetcher import fetch_all
from research_vault.scorer import score_articles
from research_vault.sources import SOURCES
from research_vault.state import load_seen, mark_seen, save_seen

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def main() -> None:
    seen = load_seen(SEEN_STORE_PATH)

    articles = fetch_all(SOURCES, LOOKBACK_HOURS, MAX_ARTICLES_PER_SOURCE)
    logger.info("Fetched %d articles from %d sources.", len(articles), len(SOURCES))

    new_articles = [a for a in articles if a.link not in seen]
    logger.info("%d articles are new since last run.", len(new_articles))

    picks = score_articles(new_articles)
    logger.info("Selected %d articles for the digest.", len(picks))

    send_digest(picks)

    # Mark every candidate we considered as seen, not just the picks, so
    # low-scoring articles don't get re-evaluated (and re-skipped) forever.
    mark_seen(seen, [a.link for a in new_articles])
    save_seen(SEEN_STORE_PATH, seen, SEEN_RETENTION_DAYS)


if __name__ == "__main__":
    main()
