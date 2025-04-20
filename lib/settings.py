import json
from datetime import datetime
from lib.constants import SOURCES_FILE

settings = None
sources = None

def initialize():
    from lib.db import get_all_settings
    
    global settings
    global sources
    
    # Load settings from db
    settings = get_all_settings()

    print("Settings loaded successfully.")

    # Load sources from JSON file
    try:
        with open(SOURCES_FILE) as f:
            sources = json.load(f)
            print("Sources loaded successfully.")

            need_renderer = False
            for source in sources['source']:
                if source["render_options"]["render"] == True:
                    need_renderer = True
                    break

            if need_renderer:
                from lib.crawler import initialize_selenium_driver
                initialize_selenium_driver()
                
    except FileNotFoundError:
        raise Exception("Sources file not found.")
    except json.JSONDecodeError:
        raise Exception("Error decoding JSON from sources file.")


def get_settings() -> dict[str, str | bool | datetime]:
    global settings

    return settings


def get_sources() -> dict[str, list[dict[str, str | None]]]:
    global sources

    return sources