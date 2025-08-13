# handlers/base_ru_patch.py
from telebot import types
from bot import bot

# Главное меню (ReplyKeyboard) — если используешь только Inline, это можно не подключать
def main_menu_ru() -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("📋 Задания", "🛒 Магазин", "🪙 Купить $KAFKA")
    return markup

# Инлайн-меню (для колбэков без новых сообщений)
def inline_root_ru() -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup()
    kb.row(
        types.InlineKeyboardButton("🪙 Купить $KAFKA", callback_data="open_buy"),
        types.InlineKeyboardButton("📋 Задания", callback_data="open_tasks"),
    )
    kb.row(
        types.InlineKeyboardButton("🛒 Магазин", callback_data="open_shoop"),
        types.InlineKeyboardButton("🎁 Аирдроп", callback_data="open_airdrop"),
        types.InlineKeyboardButton("🎮 Игра", callback_data="open_game"),
    )
    kb.row(
        types.InlineKeyboardButton("🌐 Веб", callback_data="open_web")
    )
    return kb

# Заглушки разделов — редактируем текущее сообщение, не шлём новое
STUBS_RU = {
    "open_tasks":  "Открываю: Задания",
    "open_shoop":  "Открываю: Магазин",
    "open_airdrop":"Открываю: Аирдроп",
    "open_game":   "Открываю: Игра",
    "open_web":    "Открываю: Веб",
}

@bot.callback_query_handler(func=lambda c: getattr(c, "data", "") in STUBS_RU)
def cb_open_stub_ru(call):
    text = STUBS_RU[call.data]
    # Показываем заглушку + корневое меню, чтобы пользователь мог вернуться
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=text,
        reply_markup=inline_root_ru()
    )
    bot.answer_callback_query(call.id)
