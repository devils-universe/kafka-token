from bot import bot
from telebot import types
from utils.language import get_lang
from handlers.shop_common import (
    PAYMENT_ADDRESS, STICKER_IDS,
    safe_edit_or_send, send_relic_photos_group, build_share_button
)

# ===== EN TEXTS =====
SHOP_MAIN_EN = (
    "🛒 *Shop*\n"
    "Choose a category below."
)
RELIC_CAPTION_EN = (
    "*Relic #R001 — The Smoked Core*\n"
    "Handcrafted, Kafka engraving.\n\n"
    "💳 *Payment*: `{address}`\n"
    "After payment — DM the artisan with your TX hash."
)
RELIC_ORDER_EN = (
    "To place an order:\n"
    "1) Send payment to:\n`{address}`\n"
    "2) Tap “Message artisan” and send your TX hash.\n"
    "3) We’ll confirm and arrange shipping."
)
BTN_MSG_ARTISAN_EN = "✍️ Message artisan"
BTN_SHARE_PAYMENT_EN = "📤 Share payment address"
BTN_BACK_SHOP_EN = "⬅️ Back to shop"

STICKER_INFO_EN = (
    "Full sticker pack from creator.\n"
    "For full pack — DM me.\n\n"
    "💳 Payment: `{address}`"
)
BTN_TEXT_ME_EN = "✍️ Text me"

# ===== MENUS (EN) =====
def _menu_en() -> types.InlineKeyboardMarkup:
    m = types.InlineKeyboardMarkup()
    m.add(
        types.InlineKeyboardButton("🪈 KafkaFilters", callback_data="shop_kafkafilters"),
        types.InlineKeyboardButton("🎭 KafkaStickers", callback_data="shop_kafkastickers")
    )
    return m

def _relic_keyboard_en() -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(BTN_MSG_ARTISAN_EN, url="https://t.me/devils_kafka"))
    kb.add(build_share_button(BTN_SHARE_PAYMENT_EN, "Payment address for the artifact"))
    kb.add(types.InlineKeyboardButton(BTN_BACK_SHOP_EN, callback_data="back_to_shop"))
    return kb

# ===== ENTRY (reply buttons) =====
@bot.message_handler(func=lambda msg: msg.text == "🛒 Shoop")
def handle_shoop_en(message):
    uid = message.from_user.id
    if get_lang(uid) != "en":
        return
    bot.send_message(
        message.chat.id, SHOP_MAIN_EN, parse_mode="Markdown", reply_markup=_menu_en()
    )

# ===== OPEN FROM INLINE (callback) =====
def open(call):
    uid = call.from_user.id
    if get_lang(uid) != "en":
        return
    safe_edit_or_send(call, SHOP_MAIN_EN, _menu_en())

# ===== RELIC: KafkaFilters =====
@bot.callback_query_handler(func=lambda call: call.data == "shop_kafkafilters"
                                         and get_lang(call.from_user.id) == "en")
def handle_shop_kafkafilters_en(call):
    chat_id = call.message.chat.id
    send_relic_photos_group(chat_id, RELIC_CAPTION_EN.format(address=PAYMENT_ADDRESS))
    bot.send_message(
        chat_id,
        RELIC_ORDER_EN.format(address=PAYMENT_ADDRESS),
        parse_mode="Markdown",
        reply_markup=_relic_keyboard_en()
    )
    bot.answer_callback_query(call.id)

# ===== STICKERS =====
@bot.callback_query_handler(func=lambda call: call.data == "shop_kafkastickers"
                                         and get_lang(call.from_user.id) == "en")
def handle_shop_kafkastickers_en(call):
    for sid in STICKER_IDS:
        bot.send_sticker(call.message.chat.id, sid)

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(BTN_TEXT_ME_EN, url="https://t.me/devils_kafka"))
    markup.add(types.InlineKeyboardButton(BTN_BACK_SHOP_EN, callback_data="back_to_shop"))
    bot.send_message(
        call.message.chat.id,
        STICKER_INFO_EN.format(address=PAYMENT_ADDRESS),
        parse_mode="Markdown",
        reply_markup=markup
    )
    bot.answer_callback_query(call.id)

# ===== BACK =====
@bot.callback_query_handler(func=lambda call: call.data == "back_to_shop"
                                         and get_lang(call.from_user.id) == "en")
def back_to_shop_en(call):
    safe_edit_or_send(call, SHOP_MAIN_EN, _menu_en())
    bot.answer_callback_query(call.id)
