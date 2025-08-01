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

@bot.message_handler(func=lambda msg: msg.text == "📋 Tasks")
def handle_tasks(message):
    text = (
        "*📋 Task:*\n"
        "Create a meme story with Kafka, minimum *142 words*, and get *42 $KAFKA* 🐿️\n\n"
        "🔗 Share it in the chat: [Kafka Storage](https://t.me/+LK08slIhqj1iZTMy)\n"
        "✅ Make sure you're subscribed to the channels:\n"
        "• [DevilsUniverse EN](https://t.me/devilsuniversecom)\n"
        "• [DevilsUniverse RU](https://t.me/devilsuniverseru)"
    )

    bot.send_message(
        message.chat.id,
        text,
        parse_mode="Markdown",
        reply_markup=get_main_menu()
    )
