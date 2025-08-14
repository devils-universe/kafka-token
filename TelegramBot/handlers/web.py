from bot import bot

@bot.message_handler(func=lambda msg: msg.text in {"🌀 Web", "🌀 Веб"})
def handle_web(message):
    bot.send_message(message.chat.id, "https://devilsuniverse.com/", disable_web_page_preview=True)
