from bot import bot
from telebot import types
from utils.language import get_lang
from handlers.shop_common import (
    PAYMENT_ADDRESS, STICKER_IDS,
    safe_edit_or_send, send_relic_photos_group, build_share_button
)

# ===== RU TEXTS =====
SHOP_MAIN_RU = (
    "🛒 *Магазин*\n"
    "Выберите категорию ниже."
)
RELIC_CAPTION_RU = (
    "*Relic #R001 — The Smoked Core*\n"
    "Ручная работа, гравировка Kafka.\n\n"
    "💳 *Оплата*: `{address}`\n"
    "После оплаты — напишите мастеру, приложите TX-хеш."
)
RELIC_ORDER_RU = (
    "Чтобы оформить заказ:\n"
    "1) Отправьте оплату на адрес:\n`{address}`\n"
    "2) Нажмите «Написать мастеру» и отправьте TX-хеш.\n"
    "3) Мы подтвердим и согласуем доставку."
)
BTN_MSG_ARTISAN_RU = "✍️ Написать мастеру"
BTN_SHARE_PAYMENT_RU = "📤 Поделиться адресом оплаты"
BTN_BACK_SHOP_RU = "⬅️ Назад в магазин"

STICKER_INFO_RU = (
    "Полный пак стикеров от создателя.\n"
    "Если хотите полный набор — напишите мне.\n\n"
    "💳 Оплата: `{address}`"
)
BTN_TEXT_ME_RU = "✍️ Написать"

# ===== MENUS (RU) =====
def _menu_ru() -> types.InlineKeyboardMarkup:
    m = types.InlineKeyboardMarkup()
    m.add(
        types.InlineKeyboardButton("🪈 KafkaFilters", callback_data="shop_kafkafilters"),
        types.InlineKeyboardButton("🎭 KafkaStickers", callback_data="shop_kafkastickers")
    )
    return m

def _relic_keyboard_ru() -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(BTN_MSG_ARTISAN_RU, url="https://t.me/devils_kafka"))
    kb.add(build_share_button(BTN_SHARE_PAYMENT_RU, "Адрес оплаты для артефакта"))
    kb.add(types.InlineKeyboardButton(BTN_BACK_SHOP_RU, callback_data="back_to_shop"))
    return kb

# ===== ENTRY (reply-кнопки) =====
@bot.message_handler(func=lambda msg: msg.text == "🛒 Магазин")
def handle_shoop_ru(message):
    uid = message.from_user.id
    if get_lang(uid) != "ru":
        return
    bot.send_message(
        message.chat.id, SHOP_MAIN_RU, parse_mode="Markdown", reply_markup=_menu_ru()
    )

# ===== OPEN FROM INLINE (callback) =====
def open(call):
    uid = call.from_user.id
    if get_lang(uid) != "ru":
        return
    safe_edit_or_send(call, SHOP_MAIN_RU, _menu_ru())

# ===== RELIC: KafkaFilters =====
@bot.callback_query_handler(func=lambda call: call.data == "shop_kafkafilters"
                                         and get_lang(call.from_user.id) == "ru")
def handle_shop_kafkafilters_ru(call):
    chat_id = call.message.chat.id
    send_relic_photos_group(chat_id, RELIC_CAPTION_RU.format(address=PAYMENT_ADDRESS))
    bot.send_message(
        chat_id,
        RELIC_ORDER_RU.format(address=PAYMENT_ADDRESS),
        parse_mode="Markdown",
        reply_markup=_relic_keyboard_ru()
    )
    bot.answer_callback_query(call.id)

# ===== STICKERS =====
@bot.callback_query_handler(func=lambda call: call.data == "shop_kafkastickers"
                                         and get_lang(call.from_user.id) == "ru")
def handle_shop_kafkastickers_ru(call):
    for sid in STICKER_IDS:
        bot.send_sticker(call.message.chat.id, sid)

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(BTN_TEXT_ME_RU, url="https://t.me/devils_kafka"))
    markup.add(types.InlineKeyboardButton(BTN_BACK_SHOP_RU, callback_data="back_to_shop"))
    bot.send_message(
        call.message.chat.id,
        STICKER_INFO_RU.format(address=PAYMENT_ADDRESS),
        parse_mode="Markdown",
        reply_markup=markup
    )
    bot.answer_callback_query(call.id)

# ===== BACK =====
@bot.callback_query_handler(func=lambda call: call.data == "back_to_shop"
                                         and get_lang(call.from_user.id) == "ru")
def back_to_shop_ru(call):
    safe_edit_or_send(call, SHOP_MAIN_RU, _menu_ru())
    bot.answer_callback_query(call.id)
