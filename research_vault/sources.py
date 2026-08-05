"""RSS feed sources to monitor for AI news.

Edit this list to add/remove sources. `category` is only used to give the
model a bit of context when scoring importance.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Source:
    name: str
    url: str
    category: str


SOURCES = [
    # News sites
    Source("TechCrunch AI", "https://techcrunch.com/category/artificial-intelligence/feed/", "news"),
    Source("The Verge AI", "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml", "news"),
    Source("Ars Technica AI", "https://arstechnica.com/ai/feed/", "news"),
    Source("VentureBeat AI", "https://venturebeat.com/category/ai/feed/", "news"),
    Source("MIT Technology Review", "https://www.technologyreview.com/feed/", "news"),
    Source("Wired AI", "https://www.wired.com/feed/tag/ai/latest/rss", "news"),
    Source("MarkTechPost", "https://www.marktechpost.com/feed/", "news"),
    # Lab / company blogs
    Source("OpenAI", "https://openai.com/news/rss.xml", "lab_blog"),
    Source("Google DeepMind", "https://deepmind.google/blog/rss.xml", "lab_blog"),
    Source("Google AI", "https://blog.google/technology/ai/rss/", "lab_blog"),
    Source("Microsoft Research", "https://www.microsoft.com/en-us/research/feed/", "lab_blog"),
    Source("Hugging Face", "https://huggingface.co/blog/feed.xml", "lab_blog"),
    # Anthropic and Meta AI do not currently publish a public RSS feed for
    # their blogs — add them here if that changes.
    # Research feeds
    Source("arXiv cs.AI", "http://export.arxiv.org/rss/cs.AI", "research"),
    Source("arXiv cs.CL", "http://export.arxiv.org/rss/cs.CL", "research"),
    Source("arXiv cs.LG", "http://export.arxiv.org/rss/cs.LG", "research"),
]
