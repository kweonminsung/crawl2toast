import sqlite3
from datetime import datetime
from lib.enums import SettingKey

conn = None

def initialize():
    global conn
    
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY,
            key TEXT NOT NULL UNIQUE,
            value TEXT NOT NULL
        )
    ''')
    cursor.executemany('''
        INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)
    ''', [
        (SettingKey.RECENT_STATUS.value, 'False'),
        (SettingKey.START_ONBOOT.value, 'False'),
        (SettingKey.ICONIFY_ONCLOSE.value, 'True'),
        (SettingKey.STRAY.value, 'True'),
        (SettingKey.INTERVAL.value, '12:00:00'),
        (SettingKey.RECENT_CRAWL.value, '2023-10-01 00:00:00')
    ])

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS histories (
            id INTEGER PRIMARY KEY,
            url TEXT NOT NULL,
            title TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS error_logs (
            id INTEGER PRIMARY KEY,
            url TEXT NOT NULL,
            message TEXT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()


def terminate():
    global conn

    if conn:
        conn.close()
        conn = None


def get_all_settings() -> dict[str, str | bool | datetime]:
    global conn

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM settings")
    rows = cursor.fetchall()

    result = {}
    for row in rows:
        result[row[1]] = row[2]

    return result


def set_setting(key: SettingKey, value: str) -> None:
    global conn

    cursor = conn.cursor()
    cursor.execute(f"INSERT OR REPLACE INTO settings (key, value) VALUES ('{key.value}', '{value}')")
    conn.commit()


def get_histories(url: str, limit: int, offset: int) -> list[dict[str, str | None]]:
    global conn

    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM histories WHERE url = '{url}' ORDER BY timestamp DESC LIMIT {limit} OFFSET {offset}")
    rows = cursor.fetchall()

    result = []
    for row in rows:
        result.append({
            "id": row[0],
            "url": row[1],
            "title": row[2],
            "timestamp": row[3]
        })

    return result


def get_error_logs(limit: int, offset: int) -> list[dict[str, str | None]]:
    global conn

    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM error_logs ORDER BY timestamp DESC LIMIT {limit} OFFSET {offset}")
    rows = cursor.fetchall()

    result = []
    for row in rows:
        result.append({
            "id": row[0],
            "url": row[1],
            "message": row[2],
            "timestamp": row[3]
        })

    return result


def create_error_log(url: str, message: str) -> None:
    global conn

    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO error_logs (url, message) VALUES ('{url}', '{message}')")
    conn.commit()