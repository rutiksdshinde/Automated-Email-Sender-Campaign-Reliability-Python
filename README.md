# Automated Email Sender (Campaign Reliability) — Python

A lightweight email campaign tool that supports:
- Bulk mail-merge from CSV/Excel (Jinja2 templates)
- Per-recipient attachments (via generator hook)
- Rate-limited SMTP sending with retries/backoff
- SQLite campaign + recipient logging
- Optional open tracking via a 1x1 tracking pixel endpoint
- Scheduling via APScheduler (delayed queue / run later)

> Intended for educational/small-business use. Large-scale outreach should use a transactional email provider.

## Quick start

### 1) Create `.env`
Copy `.env.example` → `.env`.

### 2) Install dependencies
```bat
cd "c:/Users/shind/2026 projects/Rutik Python Projects/automated-email-sender"
python -m pip install -r requirements.txt
```

### 3) Run the web app
```bat
python -m uvicorn email_sender.app:app --reload --port 8003
```

Open:
- http://127.0.0.1:8003/

## Configuration
See `.env.example`.

Important SMTP notes:
- Gmail SMTP typically requires an **App Password**.
- Avoid sending to large unknown lists; keep batches small.

## Mail merge inputs
Prepare a CSV or Excel with at least:
- `email`
- `name` (optional)
- any extra custom columns you reference in templates

## Templates
Edit templates in `email_sender/templates/email_templates/`.

## Attachment generation
Implement `email_sender/services/attachments.py::generate_attachment_for_recipient(recipient)`.
- Current version includes a sample PDF generator.

## Tracking pixel
If enabled, emails include an image URL like:
`{BASE_URL}/track/<recipient_public_id>.png`

When the image is requested, the system logs an `opened_at` timestamp.

## Run modes
- Start server for dashboard + tracking
- Schedule a campaign via the REST endpoints or dashboard (Phase 2+)

## Links
- **Portfolio:** https://rutikshinde.netlify.app/
- **LinkedIn:** https://www.linkedin.com/in/rutik-shinde-09a438237
- **GitHub:** https://github.com/rutiksdshinde
