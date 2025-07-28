from telebot import TeleBot, types

# Создание экземпляра бота
bot = TeleBot("YOUR_BOT_TOKEN")  # Замените на ваш токен

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

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_start(message):
    start_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_markup.add(types.KeyboardButton("Start"))
    bot.send_message(message.chat.id, "Hi! Start 🐿️", reply_markup=start_markup)

# Обработчик нажатия кнопки "Start"
@bot.message_handler(func=lambda msg: msg.text == "Start")
def show_menu(message):
    bot.send_message(message.chat.id, "Choose one:", reply_markup=main_menu)

# Запуск бота
bot.polling(none_stop=True)
