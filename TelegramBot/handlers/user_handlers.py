from telebot import types
from bot import bot
from utils.language import t, set_lang, get_lang

# ---- Меню (reply keyboard) ----

def build_main_menu(uid: int) -> types.ReplyKeyboardMarkup:
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(
        types.KeyboardButton(t(uid, "menu_buy")),
        types.KeyboardButton(t(uid, "menu_tasks")),
        types.KeyboardButton(t(uid, "menu_shop")),
    )
    kb.add(
        types.KeyboardButton(t(uid, "menu_aird")),
        types.KeyboardButton(t(uid, "menu_game")),
        types.KeyboardButton(t(uid, "menu_web")),
    )
    kb.add(types.KeyboardButton(t(uid, "language")))
    return kb


def build_lang_menu(uid: int) -> types.ReplyKeyboardMarkup:
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(
        types.KeyboardButton(t(uid, "english")),
        types.KeyboardButton(t(uid, "russian")),
    )
    kb.add(types.KeyboardButton(t(uid, "back")))
    return kb


# ---- Хэндлеры ----

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
