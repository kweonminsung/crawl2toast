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

    def to_native(self) -> str:
        if self == Language.ENGLISH:
            return 'English'
        elif self == Language.KOREAN:
            return '한국어'
        else:
            return '한국어'
    
    @staticmethod
    def from_native(native: str) -> 'Language':
        if native == 'English':
            return Language.ENGLISH
        elif native == '한국어':
            return Language.KOREAN