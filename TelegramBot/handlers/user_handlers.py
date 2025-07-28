from telebot import types
from bot import bot

# Главное меню
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

# Команда /start
@bot.message_handler(commands=["start"])
def send_start(message):
    start_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_markup.add(types.KeyboardButton("Start"))
    bot.send_message(message.chat.id, "👋 Press Start!", reply_markup=start_markup)

# Показ главного меню
@bot.message_handler(func=lambda msg: msg.text == "Start")
def show_menu(message):
    bot.send_message(message.chat.id, "Select action:", reply_markup=main_menu)

# Обработчики кнопок главного меню
@bot.message_handler(func=lambda msg: msg.text == "🪙 Buy $KAFKA")
def handle_buy(message):
    bot.send_message(message.chat.id, "💰 Let's buy $KAFKA!")

@bot.message_handler(func=lambda msg: msg.text == "📋 Tasks")
def handle_tasks(message):
    bot.send_message(message.chat.id, "📋 Here are your tasks.")

@bot.message_handler(func=lambda msg: msg.text == "🛒 Shoop")
def handle_shop(message):
    bot.send_message(message.chat.id, "🛒 Welcome to the shop!")

@bot.message_handler(func=lambda msg: msg.text == "🎁 Airdrop")
def handle_airdrop(message):
    bot.send_message(message.chat.id, "🎁 Join the airdrop now!")

@bot.message_handler(func=lambda msg: msg.text == "🎖 Leaderboard")
def handle_leaderboard(message):
    bot.send_message(message.chat.id, "🎖 Check the leaderboard!")

@bot.message_handler(func=lambda msg: msg.text == "🎨 Custom Sticker")
def handle_sticker(message):
    bot.send_message(message.chat.id, "🎨 Send your idea for a custom sticker.")
