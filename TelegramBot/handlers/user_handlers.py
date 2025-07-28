from telebot import types
from bot import bot

def main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton("🪙 Buy $KAFKA"),
        types.KeyboardButton("📋 Tasks"),
        types.KeyboardButton("🛒 Shoop")
    )
    markup.add(
        types.KeyboardButton("🎁 Airdrop"),
        types.KeyboardButton("🎖 Leaderboard"),
        types.KeyboardButton("🎨 Custom Sticker")
    )
    bot.send_message(message.chat.id, "Select action:", reply_markup=markup)

@bot.message_handler(commands=["start"])
def send_start(message):
    start_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_markup.add(types.KeyboardButton("Start"))
    bot.send_message(message.chat.id, "👋 Press Start!", reply_markup=start_markup)

@bot.message_handler(func=lambda msg: msg.text == "Start")
def show_menu(message):
    main_menu(message)  

@bot.message_handler(func=lambda msg: msg.text == "⬅️ Back")
def go_back(message):
    main_menu(message)
