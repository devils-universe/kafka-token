from bot import bot
from telebot import types

def get_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton("🪙 Buy $KAFKA"),
        types.KeyboardButton("📋 Tasks"),
        types.KeyboardButton("🛒 Shoop")
    )
    markup.add(
        types.KeyboardButton("🎁 Airdrop"),
        types.KeyboardButton("🥭 Game"),
        types.KeyboardButton("🌀 Web")
    )
    return markup

# ----- основной текст задания -----
def tasks_main_text():
    return (
        "*📋 Task:*\n"
        "Create a meme story with Kafka, minimum *142 words*, and get *42 $KAFKA* 🐿️\n"
        "+ minimum 2 NFT illustrations for the plot\n\n"
        "🔗 Share it in the chat: [Kafka Storage](https://t.me/+LK08slIhqj1iZTMy)\n"
        "✅ Make sure you're subscribed to the channels:\n"
        "• [DevilsUniverse EN](https://t.me/devilsuniversecom)\n"
        "• [DevilsUniverse RU](https://t.me/devilsuniverseru)"
    )

def tasks_main_markup():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("📣 Follow us", callback_data="tasks_follow_us"))
    return kb

# ----- блок Follow us -----
def follow_us_text():
    return (
        "📣 *Follow us:*\n"
        "• [TikTok](https://www.tiktok.com/@devils_kafka)\n"
        "• [X](https://x.com/devils_kafka)\n"
        "• [Facebook](https://www.facebook.com/devilsuniversecom)"
    )

def follow_us_markup():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("⬅️ Back to Tasks", callback_data="tasks_back"))
    return kb

# ----- обработчики -----
@bot.message_handler(func=lambda msg: msg.text == "📋 Tasks")
def handle_tasks(message):
    bot.send_message(
        message.chat.id,
        tasks_main_text(),
        parse_mode="Markdown",
        disable_web_page_preview=True,
        reply_markup=tasks_main_markup()
    )

@bot.callback_query_handler(func=lambda c: c.data == "tasks_follow_us")
def cb_tasks_follow_us(call):
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=follow_us_text(),
        parse_mode="Markdown",
        disable_web_page_preview=True,
        reply_markup=follow_us_markup()
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda c: c.data == "tasks_back")
def cb_tasks_back(call):
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=tasks_main_text(),
        parse_mode="Markdown",
        disable_web_page_preview=True,
        reply_markup=tasks_main_markup()
    )
    bot.answer_callback_query(call.id)
