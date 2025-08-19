from datetime import datetime, timezone

def format_datetime(dt: datetime) -> datetime:
    """Formats a datetime object to a string in ISO 8601 format."""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt

def get_now_utc() -> datetime:
    """Returns the current time in UTC."""
    return datetime.now(timezone.utc)
