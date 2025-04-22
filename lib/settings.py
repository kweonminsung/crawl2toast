import json
from datetime import datetime, time
from lib.constants import SOURCES_FILE
from lib.enums import SettingKey

settings: dict[str, str | bool | datetime | time] | None = None
sources: dict | None = None

def initialize():
    # Load settings from db
    load_settings()
    print("Settings loaded successfully.")

    # Load sources from JSON file
    load_sources()
    print("Sources loaded successfully.")


def load_sources():
    global sources
    
    # Load sources from JSON file
    try:
        with open(SOURCES_FILE, encoding="utf-8") as f:
            raw_source: list[dict] = json.load(f)["source"]

            sources = dict()
            for source in raw_source:
                sources[source["url"]] = source
                
    except FileNotFoundError:
        raise Exception("Sources file not found.")
    except json.JSONDecodeError:
        raise Exception("Error decoding JSON from sources file.")
    

def load_settings() -> None:
    from lib.db import Database, get_all_settings

    global settings

    settings = get_all_settings(Database().get_connection())


def get_settings() -> dict[SettingKey, str | bool | datetime | time]:
    global settings

    return settings


def set_setting(key: SettingKey, value: str | bool | datetime | time) -> None:
    from lib.db import Database, set_setting as set_setting_db

    set_setting_db(Database().get_connection(), key, value)
    
    load_settings()


def get_sources() -> dict:
    global sources

    return sources