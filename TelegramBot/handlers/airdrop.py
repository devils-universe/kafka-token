from bot import bot
from utils.language import t

@bot.message_handler(func=lambda m: m.text in {"🎁 Airdrop", "🎁 Аирдроп"})
def handle_airdrop(message):
    uid = message.from_user.id
    bot.send_message(message.chat.id, f"🎁 {t(uid, 'coming_soon')}")
