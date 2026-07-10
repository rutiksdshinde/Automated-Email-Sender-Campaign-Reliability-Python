"""Campaign Reliability — Flask dashboard + tracking pixel."""

from __future__ import annotations

import os
from datetime import datetime

from flask import Flask, render_template, request, Response, abort, redirect, url_for

from .config import settings
from .db.session import get_session
from .db.models import Campaign, Recipient, RecipientOpen
from .services.email_status import build_dashboard_stats


def create_app() -> Flask:
    app = Flask(__name__, template_folder="templates")

    @app.get("/")
    def index():
        with get_session() as session:
            stats = build_dashboard_stats(session)
        return render_template("dashboard/index.html", stats=stats)

    @app.get("/track/<public_id>.png")
    def track(public_id: str):
        # Mark open if not already opened.
        with get_session() as session:
            recipient = session.query(Recipient).filter(Recipient.public_id == public_id).first()
            if not recipient:
                abort(404)

            # idempotent: insert open only once
            opened = (
                session.query(RecipientOpen)
                .filter(RecipientOpen.recipient_id == recipient.id)
                .first()
            )
            if not opened:
                open_row = RecipientOpen(recipient_id=recipient.id, opened_at=datetime.utcnow())
                session.add(open_row)
                recipient.status = recipient.status  # no-op; keep existing
                session.commit()

        # 1x1 transparent PNG
        png_bytes = settings.TRACKING_PIXEL_PNG_BYTES
        return Response(png_bytes, mimetype="image/png")

    return app


app = create_app()

# Ensure Uvicorn gets an ASGI callable.
# This project uses Flask, so we expose app_wsgi (WSGI callable) for compatibility.
# If you want native ASGI, replace Flask with FastAPI/Starlette.
app_wsgi = app


