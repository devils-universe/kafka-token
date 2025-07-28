from bot import bot

@bot.message_handler(func=lambda msg: msg.text == "🎨 Custom Sticker")
def handle_sticker(message):
    bot.send_message(message.chat.id, "🎨 Send your idea for a custom sticker.")
