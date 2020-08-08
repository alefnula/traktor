from datetime import datetime, timezone

FORMAT = "%Y-%m-%dT%H:%M:%S"


def utcnow() -> datetime:
    """Return tz aware UTC now."""
    return datetime.utcnow().replace(tzinfo=timezone.utc)


def dt_to_str(dt: datetime) -> str:
    """Format datetime to string."""
    return dt.strftime(FORMAT)


def str_to_dt(s: str) -> datetime:
    """Parse datetime string to tz aware UTC."""
    return datetime.strptime(s, FORMAT).replace(tzinfo=timezone.utc)


def local_time(dt: datetime, tz: timezone):
    return dt.astimezone(tz)
