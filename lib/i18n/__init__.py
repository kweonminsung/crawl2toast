import i18n
import os
from lib.enums import Language, SettingKey
from lib.settings import get_settings, set_setting

def initialize():
    settings = get_settings()
    lang = settings[SettingKey.LANGUAGE]

    i18n.load_path.append(os.path.join(os.path.dirname(__file__), "locales"))

    i18n.set('file_format', 'json')
    i18n.set('filename_format', '{locale}.{format}')
    i18n.set("locale", lang.value)
    i18n.set("fallback", Language.KOREAN.value)


def set_language(language: Language):
    set_setting(SettingKey.LANGUAGE, language)
    i18n.set("locale", language.value)


def t(key: str, **kwargs) -> str:
    return i18n.t(key, **kwargs)