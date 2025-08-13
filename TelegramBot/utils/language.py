from typing import Dict
from .translations import TRANSLATIONS

# Простое хранение в памяти (на Railway перезапускается вместе с процессом).
_user_lang: Dict[int, str] = {}

DEFAULT_LANG = "en"

def get_lang(user_id: int) -> str:
    return _user_lang.get(user_id, DEFAULT_LANG)

def set_lang(user_id: int, lang: str) -> None:
    if lang in TRANSLATIONS:
        _user_lang[user_id] = lang

def t(user_id: int, key: str) -> str:
    lang = get_lang(user_id)
    # сначала пробуем текущий язык, затем английский, затем сам ключ
    return TRANSLATIONS.get(lang, {}).get(key, TRANSLATIONS["en"].get(key, key))
