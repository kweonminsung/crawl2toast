import json
from datetime import datetime, time
from lib.constants import SOURCES_FILE
from lib.enums import SettingKey
from tkinter import messagebox
import os

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

                if "name" not in source:
                    source["name"] = None
                if "url" not in source:
                    raise AttributeError("'url' 속성이 없습니다.")
                
                if "selector" not in source:
                    raise AttributeError("'selector' 속성이 없습니다.")
                if "parent" not in source["selector"]:
                    raise AttributeError("'selector.parent' 속성이 없습니다.")
                if "child" not in source["selector"]:
                    raise AttributeError("'selector.child' 속성이 없습니다.")
                if "crawl_content" not in source["selector"]:
                    raise AttributeError("'selector.crawl_content' 속성이 없습니다.")
                if "crawl_link" not in source["selector"]:
                    source["selector"]["crawl_link"] = None

                if "options" not in source:
                    source["options"] = dict()
                if "disable_history" not in source["options"]:
                    source["options"]["disable_history"] = False
                if "disable_last_history_check" not in source["options"]:
                    source["options"]["disable_last_history_check"] = False
                if "render" not in source["options"]:
                    source["options"]["render"] = False
                if "render_wait" not in source["options"]:
                    source["options"]["render_wait"] = 1000

                sources[source["url"]] = source
                
    except FileNotFoundError:
        messagebox.showerror("오류", f"{SOURCES_FILE} 파일을 찾을 수 없습니다.\n파일을 생성합니다.")
        
        with open(SOURCES_FILE, "w", encoding="utf-8") as f:
            json.dump({"source": []}, f)

    except json.JSONDecodeError:
        messagebox.showerror("오류", f"{SOURCES_FILE} 파일을 읽는 중 오류가 발생했습니다.")

    except AttributeError as e:
        messagebox.showerror("오류", f"{SOURCES_FILE} 파일의 형식이 잘못되었습니다.\n{e}")
    

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