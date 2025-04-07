import os
import sys
from datetime import datetime, timedelta
from enum import Enum
from zoneinfo import ZoneInfo
from pydantic import BaseModel

# ✅ Fix for Windows + tzdata (IANA timezones like 'Asia/Kolkata')
if sys.platform == "win32":
    os.environ["PYTHONTZPATH"] = os.path.join(sys.prefix, "Lib", "site-packages", "tzdata", "zoneinfo")


class TimeTools(str, Enum):
    GET_CURRENT_TIME = "get_current_time"
    CONVERT_TIME = "convert_time"


class TimeResult(BaseModel):
    timezone: str
    datetime: str
    is_dst: bool


class TimeConversionResult(BaseModel):
    source: TimeResult
    target: TimeResult
    time_difference: str


class TimeServer:
    def get_current_time(self, timezone_name: str) -> TimeResult:
        try:
            timezone = ZoneInfo(timezone_name)
        except Exception:
            raise ValueError(f"No time zone found with key '{timezone_name}'")

        current_time = datetime.now(timezone)

        return TimeResult(
            timezone=timezone_name,
            datetime=current_time.isoformat(timespec="seconds"),
            is_dst=bool(current_time.dst()),
        )

    def convert_time(self, source_tz: str, time_str: str, target_tz: str) -> TimeConversionResult:
        try:
            source_timezone = ZoneInfo(source_tz)
            target_timezone = ZoneInfo(target_tz)
        except Exception:
            raise ValueError(f"Invalid timezone(s): {source_tz}, {target_tz}")

        try:
            parsed_time = datetime.strptime(time_str, "%H:%M").time()
        except ValueError:
            raise ValueError("Invalid time format. Use HH:MM in 24-hour format.")

        now = datetime.now(source_timezone)
        source_time = datetime(
            now.year, now.month, now.day,
            parsed_time.hour, parsed_time.minute,
            tzinfo=source_timezone
        )

        target_time = source_time.astimezone(target_timezone)

        source_offset = source_time.utcoffset() or timedelta()
        target_offset = target_time.utcoffset() or timedelta()
        hours_difference = (target_offset - source_offset).total_seconds() / 3600

        if hours_difference.is_integer():
            time_diff_str = f"{hours_difference:+.1f}h"
        else:
            time_diff_str = f"{hours_difference:+.2f}".rstrip("0").rstrip(".") + "h"

        return TimeConversionResult(
            source=TimeResult(
                timezone=source_tz,
                datetime=source_time.isoformat(timespec="seconds"),
                is_dst=bool(source_time.dst()),
            ),
            target=TimeResult(
                timezone=target_tz,
                datetime=target_time.isoformat(timespec="seconds"),
                is_dst=bool(target_time.dst()),
            ),
            time_difference=time_diff_str,
        )
