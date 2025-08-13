from bot import bot
from utils.language import t

@bot.message_handler(func=lambda msg: msg.text == "🥭 Game")
def handle_leaderboard(message):
    bot.send_message(message.chat.id, "Coming soon, powerd by Mango")
