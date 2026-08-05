import json
import logging

import anthropic

from research_vault.config import ANTHROPIC_API_KEY, ANTHROPIC_MODEL, MIN_IMPORTANCE_SCORE, TOP_N_ARTICLES
from research_vault.fetcher import Article

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You help a working AI engineer keep up with the field by picking the \
most important items out of a daily batch of AI-related articles, blog posts, and \
research papers. "Important" means: likely to affect how people build with AI, a \
notable capability jump, a major product/model launch, a widely-relevant research \
result, or significant industry/regulatory news. Routine product marketing, minor \
version bumps, listicles, and opinion pieces without new information are low \
importance. Duplicate stories about the same event should only have the clearer or \
more original source picked."""

OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "picks": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "index": {"type": "integer", "description": "Index of the article in the provided list"},
                    "score": {"type": "integer", "description": "Importance score from 1 (skip) to 10 (must-read)"},
                    "reason": {"type": "string", "description": "One sentence on why this matters"},
                },
                "required": ["index", "score", "reason"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["picks"],
    "additionalProperties": False,
}


def _format_articles(articles: list[Article]) -> str:
    lines = []
    for i, article in enumerate(articles):
        lines.append(
            f"[{i}] ({article.category}/{article.source}) {article.title}\n{article.summary}"
        )
    return "\n\n".join(lines)


class ScoredArticle:
    def __init__(self, article: Article, score: int, reason: str):
        self.article = article
        self.score = score
        self.reason = reason


def score_articles(articles: list[Article]) -> list[ScoredArticle]:
    if not articles:
        return []

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    response = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=8000,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": (
                    "Here are today's candidate articles. Pick the ones worth "
                    f"including in a daily digest, at most {TOP_N_ARTICLES}. Score every "
                    "pick from 1-10 on importance; only include picks scoring "
                    f"{MIN_IMPORTANCE_SCORE} or higher.\n\n" + _format_articles(articles)
                ),
            }
        ],
        output_config={"format": {"type": "json_schema", "schema": OUTPUT_SCHEMA}},
    )

    if response.stop_reason == "refusal":
        logger.warning("Model declined to score this batch of articles.")
        return []

    text = next((b.text for b in response.content if b.type == "text"), None)
    if not text:
        logger.warning("No text content in scoring response.")
        return []

    data = json.loads(text)
    scored = []
    for pick in data.get("picks", []):
        idx = pick.get("index")
        score = pick.get("score", 0)
        if idx is None or not (0 <= idx < len(articles)) or score < MIN_IMPORTANCE_SCORE:
            continue
        scored.append(ScoredArticle(articles[idx], score, pick.get("reason", "")))

    scored.sort(key=lambda s: s.score, reverse=True)
    return scored[:TOP_N_ARTICLES]
