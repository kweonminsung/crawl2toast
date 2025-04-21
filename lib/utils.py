from datetime import datetime, time

def timestamp_to_datetime(timestamp: str) -> datetime:
    return datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    # return datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")


def datetime_to_timestamp(_datetime: datetime) -> str:
    return _datetime.strftime("%Y-%m-%d %H:%M:%S")


def time_to_int(_time: time) -> int:
    return _time.hour * 3600 + _time.minute * 60 + _time.second


def str_to_bool(value: str) -> bool:
        return value.lower() == 'true'