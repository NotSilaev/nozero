from datetime import datetime
from zoneinfo import ZoneInfo


def get_current_datetime(timezone_code: str | None = "UTC") -> datetime:
    timezone = None
    if timezone_code:
        timezone = ZoneInfo(timezone_code)
    current_datetime = datetime.now(tz=timezone)
    return current_datetime


def convert_datetime(dt: datetime | str, to: str) -> str | datetime:
    """Converts datetime to string and back."""

    if to not in ("str", "datetime"):
        raise ValueError("Param \"to\" can only be \"str\" or \"datetime\"")

    match to:
        case "str":
            return datetime.strftime(dt, "%Y-%m-%d %H:%M:%S.%f")
        case "datetime":
            return datetime.strptime(dt, "%Y-%m-%d %H:%M:%S.%f")
