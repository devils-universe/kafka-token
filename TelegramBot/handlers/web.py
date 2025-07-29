from bot import bot

@bot.message_handler(func=lambda msg: msg.text == "🌀 Web")
def handle_sticker(message):
    bot.send_message(message.chat.id, "https://devilsuniverse.com/.")
