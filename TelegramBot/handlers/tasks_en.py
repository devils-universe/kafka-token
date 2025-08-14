from bot import bot
from telebot import types
from utils.language import get_lang
from handlers.tasks_common import safe_edit_or_send

# ---- Texts (EN) ----
def tasks_main_text_en() -> str:
    return (
        "📋 *Tasks*\n"
        "Do simple actions to support the project. Choose below."
    )

def follow_us_text_en() -> str:
    return (
        "📣 *Follow us:*\n"
        "• [TikTok](https://www.tiktok.com/@devils_kafka)\n"
        "• [X](https://x.com/devils_kafka)\n"
        "• [Facebook](https://www.facebook.com/devilsuniversecom)"
    )

def tasks_main_markup_en() -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("📣 Follow us", callback_data="tasks_follow_us"))
    return kb

def follow_us_markup_en() -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("⬅️ Back", callback_data="tasks_back"))
    return kb

# ---- Entry via reply button ----
@bot.message_handler(func=lambda msg: msg.text == "📋 Tasks")
def handle_tasks_en(message):
    uid = message.from_user.id
    if get_lang(uid) != "en":
        return
    bot.send_message(
        message.chat.id,
        tasks_main_text_en(),
        parse_mode="Markdown",
        disable_web_page_preview=True,
        reply_markup=tasks_main_markup_en()
    )

# ---- Callbacks (filter by lang in decorator to avoid clashes) ----
@bot.callback_query_handler(func=lambda c: c.data == "tasks_follow_us" and get_lang(c.from_user.id) == "en")
def cb_tasks_follow_us_en(call):
    safe_edit_or_send(call, follow_us_text_en(), follow_us_markup_en())
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda c: c.data == "tasks_back" and get_lang(c.from_user.id) == "en")
def cb_tasks_back_en(call):
    safe_edit_or_send(call, tasks_main_text_en(), tasks_main_markup_en())
    bot.answer_callback_query(call.id)
