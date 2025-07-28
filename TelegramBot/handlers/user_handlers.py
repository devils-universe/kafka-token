from telebot import types
from bot import bot


def main_menu():
    """Создаёт главное меню из трёх кнопок."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton("🪙 Buy $KAFKA"))
    markup.row(
        types.KeyboardButton("📋 Tasks"),
        types.KeyboardButton("🛒 Shoop")
    )
    return markup


@bot.message_handler(commands=["start"])
def send_start(message):
    """Обрабатывает команду /start — предлагает нажать Start."""
    start_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_markup.add(types.KeyboardButton("Start"))
    bot.send_message(
        message.chat.id,
        "👋 Hi there! Press *Start* to begin your Kafka journey 🐿️",
        parse_mode="Markdown",
        reply_markup=start_markup
    )


@bot.message_handler(func=lambda msg: msg.text == "Start")
def show_menu(message):
    """Отображает главное меню после нажатия Start."""
    bot.send_message(
        message.chat.id,
        "What would you like to do?",
        reply_markup=main_menu()
    )
