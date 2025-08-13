from bot import bot
from utils.language import t

@bot.message_handler(func=lambda m: m.text in {"🥭 Game"})
def handle_airdrop(message):
    uid = message.from_user.id
    bot.send_message(message.chat.id, f"🥭 {t(uid, 'Coming soon, powerd by Mango')}")
