from datetime import datetime, timezone

FORMAT = "%Y-%m-%dT%H:%M:%S"


def make_aware(dt: datetime) -> datetime:
    """Make UTC time timezone aware."""
    return dt.replace(tzinfo=timezone.utc)


def utcnow() -> datetime:
    """Return tz aware UTC now."""
    return make_aware(datetime.utcnow())


def dt_to_str(dt: datetime) -> str:
    """Format datetime to string."""
    return dt.strftime(FORMAT)


def str_to_dt(s: str) -> datetime:
    """Parse datetime string to tz aware UTC."""
    return make_aware(datetime.strptime(s, FORMAT))


def local_time(dt: datetime, tz: timezone):
    return dt.astimezone(tz)


HOURS = 60 * 60
MINUTES = 60


def humanize(duration: int) -> str:
    hours = duration // HOURS

    result = []
    if hours > 0:
        result.append(f"{hours}h")
        duration = duration - (HOURS * hours)

    minutes = duration // MINUTES
    if minutes > 0 or hours > 0:
        result.append(f"{minutes:02d}m")
        duration = duration - (MINUTES * minutes)

    result.append(f"{duration:02d}s")
    return " ".join(result)
