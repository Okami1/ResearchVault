import logging
import smtplib
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from html import escape

from research_vault.config import (
    DIGEST_FROM_EMAIL,
    DIGEST_TO_EMAIL,
    SMTP_HOST,
    SMTP_PASSWORD,
    SMTP_PORT,
    SMTP_USERNAME,
)
from research_vault.scorer import ScoredArticle

logger = logging.getLogger(__name__)


def _render_html(picks: list[ScoredArticle]) -> str:
    items = []
    for pick in picks:
        a = pick.article
        items.append(
            f"""
            <li style="margin-bottom: 18px;">
              <a href="{escape(a.link)}" style="font-size: 16px; font-weight: 600; color: #1a1a1a;">{escape(a.title)}</a>
              <div style="font-size: 13px; color: #666;">{escape(a.source)} &middot; importance {pick.score}/10</div>
              <div style="font-size: 14px; color: #333; margin-top: 4px;">{escape(pick.reason)}</div>
            </li>
            """
        )
    return f"""
    <div style="font-family: sans-serif; max-width: 640px; margin: 0 auto;">
      <h2>AI Digest &mdash; {date.today().isoformat()}</h2>
      <ol style="padding-left: 20px;">
        {''.join(items)}
      </ol>
    </div>
    """


def send_digest(picks: list[ScoredArticle]) -> None:
    if not picks:
        logger.info("No picks to send; skipping email.")
        return

    message = MIMEMultipart("alternative")
    message["Subject"] = f"AI Digest — {date.today().isoformat()} ({len(picks)} articles)"
    message["From"] = DIGEST_FROM_EMAIL
    message["To"] = DIGEST_TO_EMAIL
    message.attach(MIMEText(_render_html(picks), "html"))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(DIGEST_FROM_EMAIL, [DIGEST_TO_EMAIL], message.as_string())

    logger.info("Sent digest with %d articles.", len(picks))
