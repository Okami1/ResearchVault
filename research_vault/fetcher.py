import calendar
import logging
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

import feedparser

from research_vault.sources import Source

logger = logging.getLogger(__name__)


@dataclass
class Article:
    title: str
    link: str
    summary: str
    published: datetime
    source: str
    category: str


def _entry_published_at(entry) -> datetime | None:
    for field in ("published_parsed", "updated_parsed"):
        struct_time = entry.get(field)
        if struct_time:
            return datetime.fromtimestamp(calendar.timegm(struct_time), tz=timezone.utc)
    return None


def _clean_summary(entry) -> str:
    summary = entry.get("summary", "") or ""
    # Feed summaries are often raw HTML; keep it short and let the model
    # work from the title primarily.
    return summary[:500]


def fetch_source(source: Source, cutoff: datetime, max_articles: int) -> list[Article]:
    parsed = feedparser.parse(source.url)
    if parsed.bozo and not parsed.entries:
        logger.warning("Failed to parse feed %s (%s): %s", source.name, source.url, parsed.bozo_exception)
        return []
    elif parsed.bozo:
        logger.warning("Feed %s (%s) had parse errors: %s", source.name, source.url, parsed.bozo_exception)
    else:
        logger.info("Fetched %d entries from feed %s (%s)", len(parsed.entries), source.name, source.url)

    articles = []
    for entry in parsed.entries:
        published = _entry_published_at(entry)
        if published is None or published < cutoff:
            continue
        link = entry.get("link")
        title = entry.get("title")
        if not link or not title:
            continue
        articles.append(
            Article(
                title=title,
                link=link,
                summary=_clean_summary(entry),
                published=published,
                source=source.name,
                category=source.category,
            )
        )

    articles.sort(key=lambda a: a.published, reverse=True)
    return articles[:max_articles]


def fetch_all(sources: list[Source], lookback_hours: int, max_articles_per_source: int) -> list[Article]:
    cutoff = datetime.now(tz=timezone.utc) - timedelta(hours=lookback_hours)
    all_articles: list[Article] = []
    for source in sources:
        try:
            all_articles.extend(fetch_source(source, cutoff, max_articles_per_source))
        except Exception:
            logger.exception("Error fetching feed %s (%s)", source.name, source.url)
    return all_articles
