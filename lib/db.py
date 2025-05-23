import sqlite3
from sqlite3 import Connection
from datetime import datetime, time
from lib.enums import SettingKey, Language
from lib.constants import DATABASE_URL
from lib.utils import str_to_bool, timestamp_to_datetime, get_path
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
        
        self.conn = sqlite3.connect(get_path(DATABASE_URL), check_same_thread=False)
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
            (SettingKey.RECENT_CRAWL.value, '2023-10-01 00:00:00'),
            (SettingKey.LANGUAGE.value, Language.KOREAN.value)
        ])

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS histories (
                id INTEGER PRIMARY KEY,
                url TEXT NOT NULL,
                content TEXT NOT NULL,
                link TEXT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY,
                url TEXT NOT NULL,
                ok TEXT NOT NULL,
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


def get_all_settings(conn: Connection) -> dict[SettingKey, str | bool | datetime | time]:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM settings")
    rows = cursor.fetchall()

    result = dict()
    for row in rows:
        if row[1] == SettingKey.RECENT_STATUS.value:
            result[SettingKey.RECENT_STATUS] = str_to_bool(row[2])
        elif row[1] == SettingKey.START_ONBOOT.value:
            result[SettingKey.START_ONBOOT] = str_to_bool(row[2])
        elif row[1] == SettingKey.ICONIFY_ONCLOSE.value:
            result[SettingKey.ICONIFY_ONCLOSE] = str_to_bool(row[2])
        elif row[1] == SettingKey.STRAY.value:
            result[SettingKey.STRAY] = str_to_bool(row[2])
        elif row[1] == SettingKey.INTERVAL.value:
            result[SettingKey.INTERVAL] = datetime.strptime(row[2], "%H:%M:%S").time()
        elif row[1] == SettingKey.RECENT_CRAWL.value:
            result[SettingKey.RECENT_CRAWL] = datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S")
        elif row[1] == SettingKey.LANGUAGE.value:
            result[SettingKey.LANGUAGE] = Language(row[2])

    return result


def set_setting(conn: Connection, key: SettingKey, value: str | bool | Language) -> None:
    cursor = conn.cursor()

    if isinstance(value, bool):
        value = str(value)
    elif isinstance(value, Language):
        value = value.value
        
    cursor.execute(f"INSERT OR REPLACE INTO settings (key, value) VALUES ('{key.value}', '{value}')")
    conn.commit()


def create_history(conn: Connection, url: str, content: str, link: str | None = None) -> None:
    cursor = conn.cursor()

    if link is None:
        cursor.execute(f"INSERT INTO histories (url, content) VALUES ('{url}', '{content}')")
    else:
        cursor.execute(f"INSERT INTO histories (url, content, link) VALUES ('{url}', '{content}', '{link}')")
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
            "link": row[3],
            "timestamp": timestamp_to_datetime(row[4])
        })

    return result


def delete_all_histories(conn: Connection) -> None:
    cursor = conn.cursor()
    cursor.execute("DELETE FROM histories")
    conn.commit()


def get_logs(conn: Connection, limit: int, offset: int) -> list[dict[str, str | None]]:
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM logs ORDER BY timestamp DESC LIMIT {limit} OFFSET {offset}")
    rows = cursor.fetchall()

    result = []
    for row in rows:
        result.append({
            "id": row[0],
            "url": row[1],
            "ok": str_to_bool(row[2]),
            "message": row[3],
            "timestamp": timestamp_to_datetime(row[4])
        })

    return result


def create_log(conn: Connection, url: str, ok: bool, message: str) -> None:
    cursor = conn.cursor()
    cursor.execute("INSERT INTO logs (url, ok, message) VALUES (?, ?, ?)", (url, str(ok), message))
    conn.commit()


def delete_all_logs(conn: Connection) -> None:
    cursor = conn.cursor()
    cursor.execute("DELETE FROM logs")
    conn.commit()