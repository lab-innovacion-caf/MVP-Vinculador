from datetime import datetime
import pytz

def get_epoch_time(timezone:str):
    timezone_tz = pytz.timezone(timezone)
    time = datetime.now(timezone_tz)
    epoch_time = int(time.timestamp())
    return epoch_time

def format_epoch_time(epoch_time: int, timezone: str) -> str:
    timezone_tz = pytz.timezone(timezone)
    time = datetime.fromtimestamp(epoch_time, timezone_tz)
    return time.strftime("%d/%m/%Y %H:%M:%S")