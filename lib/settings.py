import json
from datetime import datetime
from lib.constants import SOURCES_FILE

settings: dict | None = None
sources: dict | None = None

def initialize():
    from lib.db import Database, get_all_settings

    global settings
    
    # Load settings from db
    settings = get_all_settings(Database().get_connection())
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
    

def get_settings() -> dict[str, str | bool | datetime]:
    global settings

    return settings


def get_sources() -> dict[str, dict[str, str | None]]:
    global sources

    return sources