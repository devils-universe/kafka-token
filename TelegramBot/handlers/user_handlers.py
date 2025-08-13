# TelegramBot/handlers/user_handlers.py
from telebot import types
from bot import bot
from utils.language import t, set_lang, get_lang
from utils.translations import TRANSLATIONS  # чтобы получать тексты на обоих языках

# Ключи кнопок главного меню (логические)
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
    # Кнопка выбора языка
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

# === ВАЖНО: перехватываем ТОЛЬКО русские названия разделов, чтобы не бить старые англ. хендлеры ===
RU_MENU_LABELS = {
    "menu_buy":   label("ru", "menu_buy"),
    "menu_tasks": label("ru", "menu_tasks"),
    "menu_shop":  label("ru", "menu_shop"),
    "menu_aird":  label("ru", "menu_aird"),
    "menu_game":  label("ru", "menu_game"),
    "menu_web":   label("ru", "menu_web"),
}
RU_LABEL_SET = set(RU_MENU_LABELS.values())

@bot.message_handler(func=lambda m: m.text in RU_LABEL_SET)
def on_ru_menu_click(message):
    """Когда интерфейс на русском — сюда прилетают клики по русским кнопкам меню.
    На этом шаге даём аккуратные заглушки. На следующем — подвяжем реальные вызовы.
    """
    uid = message.from_user.id
    txt = message.text

    # Определим, какую кнопку нажали
    clicked_key = None
    for k, v in RU_MENU_LABELS.items():
        if v == txt:
            clicked_key = k
            break

    if not clicked_key:
        return

    # Заглушки (переводимые тексты)
    stub_key = {
        "menu_buy":   "stub_buy",
        "menu_tasks": "stub_tasks",
        "menu_shop":  "stub_shop",
        "menu_aird":  "stub_aird",
        "menu_game":  "stub_game",
        "menu_web":   "stub_web",
    }[clicked_key]

    bot.send_message(message.chat.id, t(uid, stub_key))
