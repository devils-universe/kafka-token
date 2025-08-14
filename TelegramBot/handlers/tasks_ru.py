from bot import bot
from telebot import types
from utils.language import get_lang
from handlers.tasks_common import safe_edit_or_send

# ---- Тексты (RU) ----
def tasks_main_text_ru() -> str:
    return (
        "📋 *Задания*\n"
        "Простые действия, чтобы поддержать проект. Выберите ниже."
    )

def follow_us_text_ru() -> str:
    return (
        "📣 *Подписывайтесь на нас:*\n"
        "• [TikTok](https://www.tiktok.com/@devils_kafka)\n"
        "• [X](https://x.com/devils_kafka)\n"
        "• [Facebook](https://www.facebook.com/devilsuniversecom)"
    )

def tasks_main_markup_ru() -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("📣 Подписаться", callback_data="tasks_follow_us"))
    return kb

def follow_us_markup_ru() -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("⬅️ Назад", callback_data="tasks_back"))
    return kb

# ---- Вход через reply-кнопку ----
@bot.message_handler(func=lambda msg: msg.text == "📋 Задания")
def handle_tasks_ru(message):
    uid = message.from_user.id
    if get_lang(uid) != "ru":
        return
    bot.send_message(
        message.chat.id,
        tasks_main_text_ru(),
        parse_mode="Markdown",
        disable_web_page_preview=True,
        reply_markup=tasks_main_markup_ru()
    )

# ---- Callbacks (с фильтром языка в декораторе) ----
@bot.callback_query_handler(func=lambda c: c.data == "tasks_follow_us" and get_lang(c.from_user.id) == "ru")
def cb_tasks_follow_us_ru(call):
    safe_edit_or_send(call, follow_us_text_ru(), follow_us_markup_ru())
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda c: c.data == "tasks_back" and get_lang(c.from_user.id) == "ru")
def cb_tasks_back_ru(call):
    safe_edit_or_send(call, tasks_main_text_ru(), tasks_main_markup_ru())
    bot.answer_callback_query(call.id)
