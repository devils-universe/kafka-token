from bot import bot

@bot.message_handler(func=lambda msg: msg.text == "🎖 Leaderboard")
def handle_leaderboard(message):
    bot.send_message(message.chat.id, "🎖 Check the leaderboard!")
