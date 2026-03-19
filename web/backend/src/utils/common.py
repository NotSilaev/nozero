import random
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


def generate_random_code(length: int) -> str:
    if (length < 1) or (length > 256):
        raise ValueError("The code can be from 1 to 256 chars long")

    numbers = [f"{random.randint(0, 9)}" for _ in range(0, length)]
    code = "".join(numbers)
    return code
