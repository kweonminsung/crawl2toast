import sqlite3
from enum import Enum

class SettingKey(Enum):
    START_ONBOOT = "start_onboot"
    ICONIFY_ONCLOSE = "iconify_onclose"
    STRAY = "stray"


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


def get_setting(key: SettingKey) -> str | None:
    global conn

    cursor = conn.cursor()
    cursor.execute(f"SELECT value FROM settings WHERE key = '{key.value}'")
    result = cursor.fetchone()

    if result:
        return result[0]
    else:
        return None


def set_setting(key: SettingKey, value: str) -> None:
    global conn

    cursor = conn.cursor()
    cursor.execute(f"INSERT OR REPLACE INTO settings (key, value) VALUES ('{key.value}', '{value}')")
    conn.commit()


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