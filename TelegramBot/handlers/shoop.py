from bot import bot
from telebot import types


@bot.message_handler(func=lambda msg: msg.text == "🛍 Open Sticker Store")
def handle_sticker_store(message):
    sticker_ids = [
        "CAACAgIAAxkBAAIBuWiHKOetWo-SdCruW2yorH8Wi15nAAI8ewACL4IoSIc0a3D7YkOpNgQ",
        "CAACAgIAAxkBAAIBuGiHKNz3c9yTLXQ7lLYcBm7IkvZdAAILfQACTjAgSKxOMQABd531PTYE",
        "CAACAgIAAxkBAAIBxmiHKqMAAYDeYfoAARz-6wGbE74EQL4AAut6AAKcrClIURryc3I7N242BA"
    ]

    for sticker_id in sticker_ids:
        bot.send_sticker(message.chat.id, sticker_id)

    bot.send_message(
        message.chat.id,
        "🎁 To receive the full Kafka sticker pack:\n"
        "1. Send *42 $KAFKA* to the wallet:\n"
        "`0xef43a15a02345553702c2ef7daa1883e86792f6c`\n"
        "2. In the transaction comment, write: *stickers*\n"
        "3. Then DM me the TX hash 🧾",
        parse_mode="Markdown"
    )
