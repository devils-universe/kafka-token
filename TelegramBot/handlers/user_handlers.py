from telebot import types
from bot import bot
from utils.language import t, set_lang, get_lang
from utils.translations import TRANSLATIONS

MENU_KEYS = ["menu_buy", "menu_tasks", "menu_shop", "menu_aird", "menu_game", "menu_web"]

def label(lang: str, key: str) -> str:
    """Вернёт надпись для кнопки key на языке lang."""
    return TRANSLATIONS[lang].get(key, key)

def build_main_menu(user_id: int) -> types.ReplyKeyboardMarkup:
    lang = get_lang(user_id)
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(
        types.KeyboardButton(label(lang, "menu_buy")),
        types.KeyboardButton(label(lang, "menu_tasks")),
        types.KeyboardButton(label(lang, "menu_shop")),
    )
    kb.add(
        types.KeyboardButton(label(lang, "menu_aird")),
        types.KeyboardButton(label(lang, "menu_game")),
        types.KeyboardButton(label(lang, "menu_web")),
    )
    kb.add(types.KeyboardButton(t(user_id, "language")))
    return kb

def build_lang_menu(user_id: int) -> types.ReplyKeyboardMarkup:
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(types.KeyboardButton(t(user_id, "english")),
           types.KeyboardButton(t(user_id, "russian")))
    kb.add(types.KeyboardButton(t(user_id, "back")))
    return kb

@bot.message_handler(commands=["start"])
def on_start(message):
    uid = message.from_user.id
    start_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_kb.add(types.KeyboardButton(t(uid, "start_btn")))
    start_kb.add(types.KeyboardButton(t(uid, "language")))
    bot.send_message(message.chat.id, t(uid, "start_prompt"), reply_markup=start_kb)

@bot.message_handler(func=lambda m: m.text in {"Start", "Старт"})
def on_press_start(message):
    uid = message.from_user.id
    bot.send_message(message.chat.id, t(uid, "menu_title"), reply_markup=build_main_menu(uid))

@bot.message_handler(func=lambda m: m.text in {"🌐 Language", "🌐 Язык"})
def on_language(message):
    uid = message.from_user.id
    bot.send_message(message.chat.id, t(uid, "choose_language"), reply_markup=build_lang_menu(uid))

@bot.message_handler(func=lambda m: m.text in {"English", "Русский"})
def on_language_choice(message):
    uid = message.from_user.id
    txt = message.text
    if txt == "English":
        set_lang(uid, "en")
        bot.send_message(message.chat.id, t(uid, "lang_set_en"), reply_markup=build_main_menu(uid))
    elif txt == "Русский":
        set_lang(uid, "ru")
        bot.send_message(message.chat.id, t(uid, "lang_set_ru"), reply_markup=build_main_menu(uid))

@bot.message_handler(func=lambda m: m.text in {"⬅️ Back", "⬅️ Назад"})
def on_back(message):
    uid = message.from_user.id
    bot.send_message(message.chat.id, t(uid, "menu_title"), reply_markup=build_main_menu(uid))

# RU menu stub removed – all sections now handled by their own handlers
