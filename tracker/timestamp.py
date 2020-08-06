from datetime import datetime, timezone


def utcnow() -> datetime:
    """Return tz aware UTC now."""
    return datetime.utcnow().astimezone(timezone.utc)
