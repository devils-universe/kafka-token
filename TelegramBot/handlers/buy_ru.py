# handlers/buy_ru.py
from bot import bot
from telebot import types

CONTRACT = "0x0023caf04B4fAc8B894Fc7fA49d38ddc4606a816"
SITE = "https://devilsuniverse.com"

# --- RU strings ---
def buy_main_text_ru() -> str:
    return (
        "🪙 *Купить $KAFKA*\n"
        "_BEP-20 на BNB Smart Chain_\n\n"
        f"• *Контракт:* `{CONTRACT}`\n"
        "• Decimals: `18`\n"
        "• Слиппедж: обычно `0.5–1%`\n\n"
        "👉 Выберите площадку ниже. Если впервые — нажмите *Как купить*."
    )

def build_buy_markup_ru() -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=3)
    # Ряд 1 — Покупка
    kb.row(
        types.InlineKeyboardButton("🎲 OKX", url="https://web3.okx.com/ru/token/bsc/0x0023caf04b4fac8b894fc7fa49d38ddc4606a816"),
        types.InlineKeyboardButton("🥞 Pancake", url="https://pancakeswap.finance/swap?outputCurrency=0x0023caf04b4fac8b894fc7fa49d38ddc4606a816&chain=bsc"),
        types.InlineKeyboardButton("🌶 Paprika", url="https://coinpaprika.com/coin/kafka-kafka/")
    )
    # Ряд 2 — Чарты и эксплорер
    kb.row(
        types.InlineKeyboardButton("📈 GeckoTerminal", url="https://www.geckoterminal.com/bsc/tokens/0x0023caf04b4fac8b894fc7fa49d38ddc4606a816"),
        types.InlineKeyboardButton("🔎 BscScan", url="https://bscscan.com/token/0x0023caf04B4fAc8B894Fc7fA49d38ddc4606a816"),
        types.InlineKeyboardButton("📢 Поддержка", url="https://t.me/devils_kafka")
    )
    # Ряд 3 — Утилиты
    kb.row(
        types.InlineKeyboardButton("📋 Скопировать CA", callback_data="buy_copy_ca"),
        types.InlineKeyboardButton("❓ Как купить", callback_data="buy_howto_ru")
    )
    return kb

# 1) Текстовая кнопка (ReplyKeyboard) — можно оставить, если используешь reply-клавиатуру
@bot.message_handler(func=lambda msg: getattr(msg, "text", "") == "🪙 Купить $KAFKA")
def handle_buy_ru_message(message):
    # Это отправка ОДНОГО сообщения при входе в раздел (нормально для текстовой кнопки)
    bot.send_message(
        message.chat.id,
        buy_main_text_ru(),
        parse_mode="Markdown",
        disable_web_page_preview=True,
        reply_markup=build_buy_markup_ru()
    )

# 2) Колбэк-кнопка — не создаём новых сообщений, а редактируем текущее
@bot.callback_query_handler(func=lambda c: getattr(c, "data", "") == "open_buy")
def cb_open_buy(call):
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=buy_main_text_ru(),
        parse_mode="Markdown",
        disable_web_page_preview=True,
        reply_markup=build_buy_markup_ru()
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda c: getattr(c, "data", "") == "buy_copy_ca")
def cb_buy_copy_ca(call):
    # Тут отдельное сообщение — чтобы удобно копировать адрес
    bot.answer_callback_query(call.id, "Адрес контракта отправлен.")
    bot.send_message(
        call.message.chat.id,
        f"🔗 *Адрес контракта $KAFKA (BSC):*\n`{CONTRACT}`",
        parse_mode="Markdown",
        disable_web_page_preview=True
    )

@bot.callback_query_handler(func=lambda c: getattr(c, "data", "") == "buy_howto_ru")
def cb_buy_howto_ru(call):
    text = (
        "❓ *Как купить $KAFKA*\n\n"
        "1) *Кошелёк*: MetaMask или OKX Wallet. Сеть — *BNB Smart Chain (BSC)*.\n"
        "2) *Пополните BNB* для газа.\n"
        "3) *Импорт токена*: добавьте контракт:\n"
        f"`{CONTRACT}`\n"
        "4) *Своп на Pancake/OKX*: выбирайте $KAFKA по адресу контракта.\n"
        "5) *Слиппедж*: начните с 0.5–1%. Если своп не проходит — слегка увеличьте.\n\n"
        "💡 *Безопасность*: сверяйте адрес контракта и избегайте неизвестных ссылок."
    )
    kb = types.InlineKeyboardMarkup()
    kb.row(
        types.InlineKeyboardButton("🥞 Открыть Pancake", url="https://pancakeswap.finance/swap?outputCurrency=0x0023caf04b4fac8b894fc7fa49d38ddc4606a816&chain=bsc")
    )
    kb.row(
        types.InlineKeyboardButton("⬅️ Назад", callback_data="buy_back_ru"),
        types.InlineKeyboardButton("📋 Скопировать CA", callback_data="buy_copy_ca")
    )
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=text,
        parse_mode="Markdown",
        disable_web_page_preview=True,
        reply_markup=kb
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda c: getattr(c, "data", "") == "buy_back_ru")
def cb_buy_back_ru(call):
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=buy_main_text_ru(),
        parse_mode="Markdown",
        disable_web_page_preview=True,
        reply_markup=build_buy_markup_ru()
    )
    bot.answer_callback_query(call.id)
