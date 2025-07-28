from bot import bot
from telebot import types


@bot.message_handler(func=lambda msg: msg.text == "🛒 Shoop")
def handle_shoop(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✨ Create a Meme", url="https://devilsuniverse.com/#container04"))

    bot.send_message(
        message.chat.id,
        "🐻 Custom meme or cute photo — *42 $KAFKA*\n"
        "📦 Sticker pack (coming soon)\n\n"
        "💸 Send 42 $KAFKA to:\n"
        "`0xef43a15a02345553702c2ef7daa1883e86792f6c`\n"
        "and provide the TX hash\n\n"
        "👇 Or go to the site to submit your meme idea:",
        parse_mode="Markdown",
        reply_markup=markup
    )