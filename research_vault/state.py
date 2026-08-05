import json
import os
from datetime import datetime, timedelta, timezone


def load_seen(path: str) -> dict[str, str]:
    """Load the seen-links store: {link: iso_timestamp_first_seen}."""
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_seen(path: str, seen: dict[str, str], retention_days: int) -> None:
    cutoff = datetime.now(tz=timezone.utc) - timedelta(days=retention_days)
    pruned = {
        link: ts
        for link, ts in seen.items()
        if datetime.fromisoformat(ts) >= cutoff
    }
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(pruned, f, indent=2, sort_keys=True)
        f.write("\n")


def mark_seen(seen: dict[str, str], links: list[str]) -> None:
    now = datetime.now(tz=timezone.utc).isoformat()
    for link in links:
        seen.setdefault(link, now)
