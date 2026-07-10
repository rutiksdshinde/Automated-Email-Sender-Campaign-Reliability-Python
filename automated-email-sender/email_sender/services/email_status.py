from __future__ import annotations

from sqlalchemy.orm import Session

from ..db.models import Campaign, Recipient, RecipientOpen


def build_dashboard_stats(session: Session) -> dict:
    """Return minimal stats for dashboard rendering."""
    total_campaigns = session.query(Campaign).count()
    total_recipients = session.query(Recipient).count()
    total_opens = session.query(RecipientOpen).count()

    # Basic rate; avoid div by zero.
    open_rate = (total_opens / total_recipients) if total_recipients else 0.0

    return {
        "total_campaigns": total_campaigns,
        "total_recipients": total_recipients,
        "total_opens": total_opens,
        "open_rate": open_rate,
    }

