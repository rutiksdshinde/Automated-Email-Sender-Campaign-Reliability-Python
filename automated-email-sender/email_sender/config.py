from __future__ import annotations

import os
from dataclasses import dataclass


def _get_bool(name: str, default: bool = False) -> bool:
    v = os.getenv(name)
    if v is None:
        return default
    return v.strip().lower() in {"1", "true", "yes", "y", "on"}


@dataclass(frozen=True)
class Settings:
    DATABASE_URL: str

    SEND_DELAY_SECONDS: int
    SEND_BATCH_SIZE: int
    SMTP_RETRY_COUNT: int
    SMTP_RETRY_BACKOFF_SECONDS: int

    BASE_URL: str
    TRACKING_ENABLED: bool

    # A tiny transparent PNG (1x1)
    TRACKING_PIXEL_PNG_BYTES: bytes

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    EMAIL_FROM: str


def _transparent_png_1x1() -> bytes:
    # Precomputed minimal transparent PNG bytes.
    return (
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89"
        b"\x00\x00\x00\x0bIDATx\x9cc``\x00\x00\x00\x02\x00\x01\xe2!\xbc3\x00\x00\x00\x00IEND\xaeB`\x82"
    )


def load_settings() -> Settings:
    return Settings(
        DATABASE_URL=os.getenv("DATABASE_URL", "sqlite:///email_sender.db"),
        SEND_DELAY_SECONDS=int(os.getenv("SEND_DELAY_SECONDS", "3")),
        SEND_BATCH_SIZE=int(os.getenv("SEND_BATCH_SIZE", "10")),
        SMTP_RETRY_COUNT=int(os.getenv("SMTP_RETRY_COUNT", "3")),
        SMTP_RETRY_BACKOFF_SECONDS=int(os.getenv("SMTP_RETRY_BACKOFF_SECONDS", "5")),
        BASE_URL=os.getenv("BASE_URL", "http://127.0.0.1:8003"),
        TRACKING_ENABLED=_get_bool("TRACKING_ENABLED", True),
        TRACKING_PIXEL_PNG_BYTES=_transparent_png_1x1(),
        SMTP_HOST=os.getenv("SMTP_HOST", "smtp.gmail.com"),
        SMTP_PORT=int(os.getenv("SMTP_PORT", "587")),
        SMTP_USERNAME=os.getenv("SMTP_USERNAME", ""),
        SMTP_PASSWORD=os.getenv("SMTP_PASSWORD", ""),
        EMAIL_FROM=os.getenv("EMAIL_FROM", ""),
    )


settings = load_settings()

