def timestamp_to_datetime(timestamp: str):
    from datetime import datetime
    
    # print(f"timestamp: {timestamp}")
    # return datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").strftime('%Y-%m-%d %H:%M:%S')
    return datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").strftime('%Y-%m-%d')

