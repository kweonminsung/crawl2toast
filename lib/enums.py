from enum import Enum

class SettingKey(Enum):
    RECENT_STATUS = "recent_status"
    START_ONBOOT = "start_onboot"
    ICONIFY_ONCLOSE = "iconify_onclose"
    STRAY = "stray"
    INTERVAL = "interval"
    RECENT_CRAWL = "recent_crawl"
    LANGUAGE = "language"


class Language(Enum):
    ENGLISH = "en"
    KOREAN = "ko"