# handlers/shoop.py

from bot import bot
from telebot import types
import os

# =========================
# CONFIG
# =========================
PAYMENT_ADDRESS = "0xaa0de276F5E87730431A032aD335D21EFd133Fa9"

# Put your images in the project root's "assets/" (not inside the Telegram bot folder)
RELIC_R001_PHOTOS = [
    "assets/du_shop_final_01_square.jpg",  
    "assets/du_shop_final_02_square.jpg",    
    "assets/du_shop_final_03_square.jpg",  
]
# Tip: leave only 2–3 items above. Non‑existent files will be skipped safely.

RELIC_R001_CAPTION = (
    "*Relic #R001 — The Smoked Core*\n"
    "Handcrafted bamboo bong engraved with Kafka and the $KAFKA symbol.\n\n"
    "— Engraving price: *420 $KAFKA*\n"
    "— Base item (bamboo bong): paid separately (fiat/crypto)\n"
    "— On‑chain proof + optional NFT duplicate\n\n"
    "“A portal for cache input purification. Only the worthy may inhale through the Core.”\n\n"
    "*Payment address:* `"+ PAYMENT_ADDRESS +"`"
)

def _relic_keyboard() -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("💬 Message the artisan", url="https://t.me/devils_kafka"))
    kb.add(
        types.InlineKeyboardButton(
            "📩 Share payment address",
            url=(
                "https://t.me/share/url"
                f"?url={PAYMENT_ADDRESS}"
                "&text=Payment%20for%20Relic%20%23R001%20%E2%80%94%20420%20%24KAFKA"
            ),
        )
    )
    kb.add(types.InlineKeyboardButton("⬅️ Back to Shop", callback_data="back_to_shop"))
    return kb

# =========================
# SHOP ENTRY
# =========================
@bot.message_handler(func=lambda msg: msg.text == "🛒 Shoop")
def handle_shoop(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("🪈 KafkaFilters", callback_data="shop_kafkafilters"),
        types.InlineKeyboardButton("🎭 KafkaStikers", callback_data="shop_kafkastikers")
    )
    bot.send_message(
        message.chat.id,
        "🛒 *Get something:*",
        parse_mode="Markdown",
        reply_markup=markup
    )

# =========================
# RELIC: KafkaFilters
# =========================
@bot.callback_query_handler(func=lambda call: call.data == "shop_kafkafilters")
def handle_shop_kafkafilters(call):
    chat_id = call.message.chat.id

    # 1) Send media group (caption only on the first item)
    media = []
    open_files = []  # keep refs to avoid GC before send
    for i, path in enumerate(RELIC_R001_PHOTOS):
        if not os.path.exists(path):
            continue
        f = open(path, "rb")
        open_files.append(f)
        if i == 0:
            media.append(types.InputMediaPhoto(f, caption=RELIC_R001_CAPTION, parse_mode="Markdown"))
        else:
            media.append(types.InputMediaPhoto(f))

    if media:
        try:
            bot.send_media_group(chat_id, media)
        finally:
            for f in open_files:
                try:
                    f.close()
                except Exception:
                    pass

    # 2) CTA message with buttons
    cta = (
        "🛒 *How to order*\n"
        "1) Message the artisan and describe your wishes\n"
        "2) Send *420 $KAFKA* to the address below\n"
        "3) Reply with the TX hash — you’ll receive tracking and (optional) NFT\n\n"
        "*Payment address:* `"+ PAYMENT_ADDRESS +"`"
    )
    bot.send_message(chat_id, cta, parse_mode="Markdown", reply_markup=_relic_keyboard())
    bot.answer_callback_query(call.id)

# =========================
# STICKERS
# =========================
@bot.callback_query_handler(func=lambda call: call.data == "shop_kafkastikers")
def handle_shop_kafkastikers(call):
    sticker_ids = [
        "CAACAgIAAxkBAAIBuWiHKOetWo-SdCruW2yorH8Wi15nAAI8ewACL4IoSIc0a3D7YkOpNgQ",
        "CAACAgIAAxkBAAIBuGiHKNz3c9yTLXQ7lLYcBm7IkvZdAAILfQACTjAgSKxOMQABd531PTYE",
        "CAACAgIAAxkBAAIBxmiHKqMAAYDeYfoAARz-6wGbE74EQL4AAut6AAKcrClIURryc3I7N242BA"
    ]
    for sid in sticker_ids:
        bot.send_sticker(call.message.chat.id, sid)

    msg = (
        "🎭 *To get the full Kafka sticker pack:*\n"
        "1) Send *42 $KAFKA* to the wallet:\n"
        f"{PAYMENT_ADDRESS}\n"
        "2) Add this comment: `stickers`\n"
        "3) Click below and send the TX hash to the creator"
    )
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("💬 Text me", url="https://t.me/devils_kafka"))
    markup.add(types.InlineKeyboardButton("⬅️ Back to Shop", callback_data="back_to_shop"))
    bot.send_message(call.message.chat.id, msg, parse_mode="Markdown", reply_markup=markup)
    bot.answer_callback_query(call.id)

# =========================
# BACK TO SHOP
# =========================
@bot.callback_query_handler(func=lambda call: call.data == "back_to_shop")
def back_to_shop(call):
    handle_shoop(call.message)
    bot.answer_callback_query(call.id)
