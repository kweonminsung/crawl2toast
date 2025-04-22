from datetime import datetime, time
import os
import sys


def timestamp_to_datetime(timestamp: str) -> datetime:
    return datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")


def datetime_to_timestamp(_datetime: datetime) -> str:
    return _datetime.strftime("%Y-%m-%d %H:%M:%S")


def time_to_int(_time: time) -> int:
    return _time.hour * 3600 + _time.minute * 60 + _time.second


def str_to_bool(value: str) -> bool:
        return value.lower() == 'true'

# Import from the bundled directory
def get_path(path: str, bundle_path: str | None = None) -> str:
    if getattr(sys, 'frozen', False): 
        if bundle_path is None:
            bundle_path = path
        return os.path.join(sys._MEIPASS, bundle_path)
    else:
        return path
    


def restart():
    import os
    import sys
    
    os.execl(sys.executable, *sys.orig_argv)
