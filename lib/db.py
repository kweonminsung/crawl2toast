import sqlite3
from sqlite3 import Connection
from datetime import datetime
from lib.enums import SettingKey
from threading import Lock

class Database:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        # Create singleton instance
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(Database, cls).__new__(cls)
                    cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        print("Database initialized successfully.")
        
        self.conn = sqlite3.connect('data.db', check_same_thread=False)
        self._create_tables()

    def _create_tables(self):
        cursor = self.conn.cursor()
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
                content TEXT NOT NULL,
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
        self.conn.commit()

    def get_connection(self) -> Connection:
        return self.conn

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None


def get_all_settings(conn: Connection) -> dict[str, str | bool | datetime]:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM settings")
    rows = cursor.fetchall()

    result = {}
    for row in rows:
        result[row[1]] = row[2]

    return result


def set_setting(conn: Connection, key: SettingKey, value: str) -> None:
    cursor = conn.cursor()
    cursor.execute(f"INSERT OR REPLACE INTO settings (key, value) VALUES ('{key.value}', '{value}')")
    conn.commit()


def create_history(conn: Connection, url: str, content: str) -> None:
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO histories (url, content) VALUES ('{url}', '{content}')")
    conn.commit()


def get_histories(conn: Connection, url: str, limit: int, offset: int) -> list[dict[str, str | None]]:
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM histories WHERE url = '{url}' ORDER BY timestamp DESC LIMIT {limit} OFFSET {offset}")
    rows = cursor.fetchall()

    result = []
    for row in rows:
        result.append({
            "id": row[0],
            "url": row[1],
            "content": row[2],
            "timestamp": row[3]
        })

    return result


def get_error_logs(conn: Connection, limit: int, offset: int) -> list[dict[str, str | None]]:
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


def create_error_log(conn: Connection, url: str, message: str) -> None:
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO error_logs (url, message) VALUES ('{url}', '{message}')")
    conn.commit()