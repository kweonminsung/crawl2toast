import json
from datetime import datetime, time
from lib.constants import SOURCES_FILE
from lib.enums import SettingKey, Language
from tkinter import messagebox

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
    from lib.i18n import t
    
    global sources

    sources = dict()
    
    # Load sources from JSON file
    try:
        with open(SOURCES_FILE, encoding="utf-8") as f:
            json_dict = json.load(f)

            if "source" not in json_dict:
                raise AttributeError(f"'source' {t('message.common.attribute_not_found')}")
            if not isinstance(json_dict["source"], list):
                raise AttributeError(f"'source' {t('message.common.attribute_not_list')}")

            raw_source: list[dict] = json_dict["source"]

            for source in raw_source:

                if "name" not in source:
                    source["name"] = None
                if "url" not in source:
                    raise AttributeError(f"'url' {t('message.common.attribute_not_found')}")
                
                if "selector" not in source:
                    raise AttributeError(f"'source[].selector' {t('message.common.attribute_not_found')}")
                if "parent" not in source["selector"]:
                    raise AttributeError(f"'source[].selector.parent' {t('message.common.attribute_not_found')}")
                if "child" not in source["selector"]:
                    raise AttributeError(f"'source[].selector.child' {t('message.common.attribute_not_found')}")
                if "crawl_content" not in source["selector"]:
                    raise AttributeError(f"'source[].selector.crawl_content' {t('message.common.attribute_not_found')}")
                if "crawl_link" not in source["selector"]:
                    source["selector"]["crawl_link"] = None

                if "options" not in source:
                    source["options"] = dict()
                if "disable_toast" not in source["options"]:
                    source["options"]["disable_toast"] = False
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
        messagebox.showerror(t("message.title.error"), f"{SOURCES_FILE} {t('message.common.file_not_found_create')}")
        
        with open(SOURCES_FILE, "w", encoding="utf-8") as f:
            json.dump({"source": []}, f)

    except json.JSONDecodeError:
        messagebox.showerror(t("message.title.error"), f"{SOURCES_FILE} {t('message.common.json_parse_error')}")

    except AttributeError as e:
        messagebox.showerror(t("message.title.error"), f"{SOURCES_FILE} {t('message.common.file_format_error')}\n{e}")
    

def load_settings() -> None:
    from lib.db import Database, get_all_settings

    global settings

    settings = get_all_settings(Database().get_connection())


def get_settings() -> dict[SettingKey, str | bool | datetime | time | Language]:
    global settings

    return settings


def set_setting(key: SettingKey, value: str | bool | datetime | time | Language) -> None:
    from lib.db import Database, set_setting as set_setting_db

    set_setting_db(Database().get_connection(), key, value)
    
    load_settings()


def get_sources() -> dict:
    global sources

    return sources