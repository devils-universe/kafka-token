from bot import bot
from telebot import types
from utils.language import t

# Removed get_main_menu (unused static menu for English interface)

# Основной текст "Задания" (переводится через TRANSLATIONS)
def tasks_main_text(uid) -> str:
    return t(uid, 'tasks_main')

def tasks_main_markup(uid):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(t(uid, "follow_us"), callback_data="tasks_follow_us"))
    return kb

# Блок "Follow us" (список каналов)
def follow_us_text(uid):
    return (
        f"📣 *{t(uid, 'follow_us')}:*\n"
        "• [TikTok](https://www.tiktok.com/@devils_kafka)\n"
        "• [X](https://x.com/devils_kafka)\n"
        "• [Facebook](https://www.facebook.com/devilsuniversecom)"
    )

def follow_us_markup(uid):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(t(uid, "back_tasks"), callback_data="tasks_back"))
    return kb

# Обработчики
@bot.message_handler(func=lambda msg: msg.text in {"📋 Tasks", "📋 Задания"})
def handle_tasks(message):
    uid = message.from_user.id
    bot.send_message(
        message.chat.id,
        tasks_main_text(uid),
        parse_mode="Markdown",
        disable_web_page_preview=True,
        reply_markup=tasks_main_markup(uid)
    )

@bot.callback_query_handler(func=lambda c: c.data == "tasks_follow_us")
def cb_tasks_follow_us(call):
    uid = call.from_user.id
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=follow_us_text(uid),
        parse_mode="Markdown",
        disable_web_page_preview=True,
        reply_markup=follow_us_markup(uid)
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda c: c.data == "tasks_back")
def cb_tasks_back(call):
    uid = call.from_user.id
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=tasks_main_text(uid),
        parse_mode="Markdown",
        disable_web_page_preview=True,
        reply_markup=tasks_main_markup(uid)
    )
    bot.answer_callback_query(call.id)
