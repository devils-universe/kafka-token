# handlers/shoop.py

from bot import bot
from telebot import types

# --- SHOP ENTRY POINT ---
@bot.message_handler(func=lambda msg: msg.text == "🛒 Shoop")
def handle_shoop(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("🧱 KafkaFilters", callback_data="shop_kafkafilters"),
        types.InlineKeyboardButton("🎭 KafkaStikers", callback_data="shop_kafkastikers")
    )
    bot.send_message(
        message.chat.id,
        "🛒 *Choose a category:*",
        parse_mode="Markdown",
        reply_markup=markup
    )

# --- RELIC: Filters CATEGORY ---
@bot.callback_query_handler(func=lambda call: call.data == "shop_kafkafilters")
def handle_shop_material(call):
    text = (
        "🔥 *First Relic:*\n"
        "*Relic #R001 — The Smoked Core*\n"
        "A handcrafted bamboo bong engraved with the image of Kafka and the $K symbol.\n\n"
        "🧪 The engraving symbolizes:\n\n"
        "“A portal for cache input purification. Only the worthy may inhale through the Core.”\n\n"
        "💸 Engraving price: *420 $KAFKA*\n"
        "💰 Base item price: paid separately (fiat/crypto)\n\n"
        "❗️This artifact can be purchased *only with $KAFKA*.\n"
        "By purchasing it — you unlock the gateway to the Universe.\n\n"
        "🛒 *How to order:*\n"
        "1. Contact the artisan → 💬 *Message* (/button below)\n"
        "2. Describe what engraving you want and on what item\n"
        "3. Send *420 $KAFKA*\n"
        "4. Receive your tracking number and NFT (optional)"
    )
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("💬 Text me", url="https://t.me/devils_kafka"))
    markup.add(types.InlineKeyboardButton("⬅️ Back to Shop", callback_data="back_to_shop"))
    bot.send_message(call.message.chat.id, text, parse_mode="Markdown", reply_markup=markup)
    bot.answer_callback_query(call.id)

# --- KAFKA STIKERS CATEGORY ---
@bot.callback_query_handler(func=lambda call: call.data == "shop_kafkastikers")
def handle_shop_kafkafilters(call):
    sticker_ids = [
        "CAACAgIAAxkBAAIBuWiHKOetWo-SdCruW2yorH8Wi15nAAI8ewACL4IoSIc0a3D7YkOpNgQ",
        "CAACAgIAAxkBAAIBuGiHKNz3c9yTLXQ7lLYcBm7IkvZdAAILfQACTjAgSKxOMQABd531PTYE",
        "CAACAgIAAxkBAAIBxmiHKqMAAYDeYfoAARz-6wGbE74EQL4AAut6AAKcrClIURryc3I7N242BA"
    ]
    for sid in sticker_ids:
        bot.send_sticker(call.message.chat.id, sid)

    msg = (
        "🏱 *To get the full Kafka sticker pack:*\n"
        "1. Send *42 $KAFKA* to the wallet:\n"
        "[`0xaa0de276F5E87730431A032aD335D21EFd133Fa9`]\n"
        "2. Add this comment: `stickers`\n"
        "3. Click below and send the TX hash to the creator"
    )
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("💬 Text me", url="https://t.me/devils_kafka"))
    markup.add(types.InlineKeyboardButton("⬅️ Back to Shop", callback_data="back_to_shop"))
    bot.send_message(call.message.chat.id, msg, parse_mode="Markdown", reply_markup=markup)
    bot.answer_callback_query(call.id)

# --- BACK TO SHOP ---
@bot.callback_query_handler(func=lambda call: call.data == "back_to_shop")
def back_to_shop(call):
    handle_shoop(call.message)
    bot.answer_callback_query(call.id)
