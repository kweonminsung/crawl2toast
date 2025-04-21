from datetime import datetime, time

def timestamp_to_datetime(timestamp: str):
    # return datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").strftime('%Y-%m-%d %H:%M:%S')
    return datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").strftime('%Y-%m-%d')


def time_to_int(_time: time) -> int:
    return _time.hour * 3600 + _time.minute * 60 + _time.second