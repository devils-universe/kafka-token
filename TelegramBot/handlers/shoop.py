from bot import bot
from telebot import types
import os
import urllib.parse
from utils.language import t

# CONFIG
PAYMENT_ADDRESS = "0xaa0de276F5E87730431A032aD335D21EFd133Fa9"

RELIC_R001_PHOTOS = [
    "assets/shoop/du_shop_final_01_square.jpg",
    "assets/shoop/du_shop_final_02_square.jpg",
    "assets/shoop/du_shop_final_03_square.jpg",
]

def _relic_keyboard(uid) -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup()
    # Contact artisan and share address buttons
    kb.add(types.InlineKeyboardButton(t(uid, "message_artisan"), url="https://t.me/devils_kafka"))
    share_text = t(uid, "share_text")
    encoded_text = urllib.parse.quote(share_text, safe='')
    kb.add(types.InlineKeyboardButton(t(uid, "share_payment"),
           url=f"https://t.me/share/url?url={PAYMENT_ADDRESS}&text={encoded_text}"))
    # Back to Shop button
    kb.add(types.InlineKeyboardButton(t(uid, "back_shop"), callback_data="back_to_shop"))
    return kb

# SHOP ENTRY
@bot.message_handler(func=lambda msg: msg.text in {"🛒 Shoop", "🛒 Магазин"})
def handle_shoop(message):
    uid = message.from_user.id
    markup = types.InlineKeyboardMarkup()
    # Fixed label typo: 'KafkaStikers' -> 'KafkaStickers'
    markup.add(
        types.InlineKeyboardButton("🪈 KafkaFilters", callback_data="shop_kafkafilters"),
        types.InlineKeyboardButton("🎭 KafkaStickers", callback_data="shop_kafkastickers")
    )
    bot.send_message(
        message.chat.id,
        t(uid, 'shop_main'),
        parse_mode="Markdown",
        reply_markup=markup
    )

# RELIC: KafkaFilters
@bot.callback_query_handler(func=lambda call: call.data == "shop_kafkafilters")
def handle_shop_kafkafilters(call):
    uid = call.from_user.id
    chat_id = call.message.chat.id

    # 1) Send media group (caption only on the first item)
    media = []
    open_files = []
    caption_text = t(uid, 'relic_caption').format(address=PAYMENT_ADDRESS)
    caption_set = False
    for path in RELIC_R001_PHOTOS:
        if not os.path.exists(path):
            continue
        f = open(path, "rb")
        open_files.append(f)
        if not caption_set:
            media.append(types.InputMediaPhoto(f, caption=caption_text, parse_mode="Markdown"))
            caption_set = True
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

    # 2) Send CTA message with buttons
    cta_text = t(uid, 'relic_order').format(address=PAYMENT_ADDRESS)
    bot.send_message(chat_id, cta_text, parse_mode="Markdown", reply_markup=_relic_keyboard(uid))
    bot.answer_callback_query(call.id)

# STICKERS
@bot.callback_query_handler(func=lambda call: call.data == "shop_kafkastickers")
def handle_shop_kafkastickers(call):
    uid = call.from_user.id
    sticker_ids = [
        "CAACAgIAAxkBAAIBuWiHKOetWo-SdCruW2yorH8Wi15nAAI8ewACL4IoSIc0a3D7YkOpNgQ",
        "CAACAgIAAxkBAAIBuGiHKNz3c9yTLXQ7lLYcBm7IkvZdAAILfQACTjAgSKxOMQABd531PTYE",
        "CAACAgIAAxkBAAIBxmiHKqMAAYDeYfoAARz-6wGbE74EQL4AAut6AAKcrClIURryc3I7N242BA"
    ]
    for sid in sticker_ids:
        bot.send_sticker(call.message.chat.id, sid)

    msg_text = t(uid, 'sticker_info').format(address=PAYMENT_ADDRESS)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(t(uid, "text_me"), url="https://t.me/devils_kafka"))
    markup.add(types.InlineKeyboardButton(t(uid, "back_shop"), callback_data="back_to_shop"))
    bot.send_message(call.message.chat.id, msg_text, parse_mode="Markdown", reply_markup=markup)
    bot.answer_callback_query(call.id)

# BACK TO SHOP
@bot.callback_query_handler(func=lambda call: call.data == "back_to_shop")
def back_to_shop(call):
    uid = call.from_user.id
    # Return to shop menu (send a new message with main shop options)
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("🪈 KafkaFilters", callback_data="shop_kafkafilters"),
        types.InlineKeyboardButton("🎭 KafkaStickers", callback_data="shop_kafkastickers")
    )
    bot.send_message(call.message.chat.id, t(uid, 'shop_main'), parse_mode="Markdown", reply_markup=markup)
    bot.answer_callback_query(call.id)
