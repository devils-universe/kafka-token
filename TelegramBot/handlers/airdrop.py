from bot import bot

@bot.message_handler(func=lambda msg: msg.text == "🎁 Airdrop")
def handle_airdrop(message):
    bot.send_message(message.chat.id, "🎁 Join the airdrop now!")
