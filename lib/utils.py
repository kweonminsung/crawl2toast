def timestamp_to_datetime(timestamp: str):
    from datetime import datetime

    # return datetime.fromtimestamp(float(timestamp / 1000)).strftime('%Y-%m-%d %H:%M:%S')
    return datetime.fromtimestamp(float(timestamp / 1000)).strftime('%Y-%m-%d')