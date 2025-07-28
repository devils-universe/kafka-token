from bot import bot
from telebot import types

@bot.message_handler(func=lambda msg: msg.text == "🛒 Shoop")
def handle_shoop(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("🎨 Create Kafka", url="https://devilsuniverse.com/#container04"),
        types.InlineKeyboardButton("🎁 Get Kafka", url="https://t.me/addstickers/your_sticker_pack_here")
    )

    bot.send_message(
        message.chat.id,
        "🛒 *Kafka Store*\n\n"
        "🎨 *Create Kafka* — Design a meme and earn $KAFKA\n"
        "🎁 *Get Kafka* — Download our custom sticker pack",
        parse_mode="Markdown",
        reply_markup=markup
    )
