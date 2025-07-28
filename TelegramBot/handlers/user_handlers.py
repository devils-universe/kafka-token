from telebot import types
from bot import bot

main_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(
    types.KeyboardButton("🪙 Buy $KAFKA"),
    types.KeyboardButton("📋 Tasks"),
    types.KeyboardButton("🛒 Shoop")
)
main_menu.add(
    types.KeyboardButton("🎁 Airdrop"),
    types.KeyboardButton("🎖 Leaderboard"),
    types.KeyboardButton("🎨 Custom Sticker")
)

@bot.message_handler(commands=["start"])
def send_start(message):
    start_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_markup.add(types.KeyboardButton("Start"))
    bot.send_message(message.chat.id, "👋 Press Start!", reply_markup=start_markup)

@bot.message_handler(func=lambda msg: msg.text == "Start")
def show_menu(message):
    bot.send_message(message.chat.id, "Select action:", reply_markup=main_menu())
