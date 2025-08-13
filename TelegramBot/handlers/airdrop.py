from telebot import types
from bot import bot
from utils.language import t

BTN_EN = "🎁 Airdrop"   # старое имя кнопки (англ)

def open_airdrop(message):
    uid = message.from_user.id
    bot.send_message(message.chat.id, f"{t(uid,'🎁 Airdrop')"}

# Старый обработчик — оставляем для англоязычного текста кнопки
@bot.message_handler(func=lambda m: m.text == BTN_EN)
def handle_airdrop_en(message):
    open_airdrop(message)
    uid = message.from_user.id
    bot.send_message(message.chat.id, f"{t(uid,'🎁 Лови')")
