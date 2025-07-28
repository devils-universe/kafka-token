from bot import bot
from telebot import types
from handlers.user_handlers import main_menu


@bot.message_handler(func=lambda msg: msg.text == "🛒 Shoop")
def handle_shoop(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🎨 Create a Meme", url="https://devilsuniverse.com/#container04"))
    markup.add(types.InlineKeyboardButton("🛍 Open Sticker Store", callback_data="open_sticker_store"))

    bot.send_message(
        message.chat.id,
        "🎨 Want to create or receive Kafka-themed fun?\n\nChoose an option below:",
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: call.data == "open_sticker_store")
def handle_sticker_store(call):
    """Показывает стикеры и инструкции по получению."""
    sticker_ids = [
        "CAACAgIAAxkBAAIBuWiHKOetWo-SdCruW2yorH8Wi15nAAI8ewACL4IoSIc0a3D7YkOpNgQ",
        "CAACAgIAAxkBAAIBuGiHKNz3c9yTLXQ7lLYcBm7IkvZdAAILfQACTjAgSKxOMQABd531PTYE",
        "CAACAgIAAxkBAAIBxmiHKqMAAYDeYfoAARz-6wGbE74EQL4AAut6AAKcrClIURryc3I7N242BA"
    ]
    for sticker_id in sticker_ids:
        bot.send_sticker(call.message.chat.id, sticker_id)

    msg = (
        "🎁 *To receive the full Kafka sticker pack:*\n"
        "1. Send *42 $KAFKA* to wallet:\n"
        "`0xef43a15a02345553702c2ef7daa1883e86792f6c`\n"
        "2. In the transaction comment, write: `stickers`\n"
        "3. Press the button below to send your TX hash 🧾"
    )

    button = types.InlineKeyboardMarkup()
    button.add(types.InlineKeyboardButton("🧾 Send TX hash", switch_inline_query=""))

    bot.send_message(call.message.chat.id, msg, parse_mode="Markdown", reply_markup=button)
    bot.answer_callback_query(call.id)
