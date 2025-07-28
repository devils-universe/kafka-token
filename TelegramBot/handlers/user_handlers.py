from telebot import types
from bot import bot

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton("🪙 Buy $KAFKA"))
    markup.row(types.KeyboardButton("📋 Tasks"), types.KeyboardButton("🛒 Shoop"))
    return markup

@bot.message_handler(commands=["start"])
def send_start(message):
    start_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_markup.add(types.KeyboardButton("Start"))
    bot.send_message(message.chat.id, "👋 Press Start!", reply_markup=start_markup)

@bot.message_handler(func=lambda msg: msg.text == "Start")
def show_menu(message):
    bot.send_message(message.chat.id, "Select action:", reply_markup=main_menu())
