from bot import bot
from telebot import types
import logging

CONTRACT = "0x0023caf04B4fAc8B894Fc7fA49d38ddc4606a816"

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
    kb.row(
        types.InlineKeyboardButton("🎲 OKX", url="https://web3.okx.com/ru/token/bsc/0x0023caf04b4fac8b894fc7fa49d38ddc4606a816"),
        types.InlineKeyboardButton("🥞 Pancake", url="https://pancakeswap.finance/swap?outputCurrency=0x0023caf04b4fac8b894fc7fa49d38ddc4606a816&chain=bsc"),
        types.InlineKeyboardButton("🌶 Paprika", url="https://coinpaprika.com/coin/kafka-kafka/")
    )
    kb.row(
        types.InlineKeyboardButton("📈 GeckoTerminal", url="https://www.geckoterminal.com/bsc/tokens/0x0023caf04b4fac8b894fc7fa49d38ddc4606a816"),
        types.InlineKeyboardButton("🔎 BscScan", url="https://bscscan.com/token/0x0023caf04B4fAc8B894Fc7fA49d38ddc4606a816"),
        types.InlineKeyboardButton("📢 Поддержка", url="https://t.me/devils_kafka")
    )
    kb.row(
        types.InlineKeyboardButton("📋 Скопировать CA", callback_data="buy_copy_ca"),
        types.InlineKeyboardButton("❓ Как купить", callback_data="buy_howto_ru")
    )
    return kb

def _safe_edit_or_send(call, text, reply_markup=None):
    try:
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=text,
            parse_mode="Markdown",
            disable_web_page_preview=True,
            reply_markup=reply_markup
        )
    except Exception as e:
        logging.warning(f"[buy_ru] edit_message_text failed: {e}. Sending new message.")
        bot.send_message(
            call.message.chat.id,
            text,
            parse_mode="Markdown",
            disable_web_page_preview=True,
            reply_markup=reply_markup
        )

@bot.message_handler(func=lambda msg: getattr(msg, "text", "") == "🪙 Купить $KAFKA")
def handle_buy_ru_message(message):
    bot.send_message(
        message.chat.id,
        buy_main_text_ru(),
        parse_mode="Markdown",
        disable_web_page_preview=True,
        reply_markup=build_buy_markup_ru()
    )

@bot.callback_query_handler(func=lambda c: isinstance(getattr(c, "data", None), str)
                                       and (c.data == "open_buy" or c.data.startswith("buy_")))
def cb_buy_ru(call):
    from utils.language import t, get_lang
    if get_lang(call.from_user.id) != 'ru':
        return
    data = call.data
    if data == "open_buy":
        _safe_edit_or_send(call, buy_main_text_ru(), build_buy_markup_ru())
    elif data == "buy_copy_ca":
        uid = call.from_user.id
        bot.answer_callback_query(call.id, t(uid, "contract_sent"))
        bot.send_message(
            call.message.chat.id,
            f"🔗 *Адрес контракта $KAFKA (BSC):*\n`{CONTRACT}`",
            parse_mode="Markdown",
            disable_web_page_preview=True
        )
    elif data == "buy_howto_ru":
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
            types.InlineKeyboardButton("⬅️ Назад", callback_data="open_buy"),
            types.InlineKeyboardButton("📋 Скопировать CA", callback_data="buy_copy_ca")
        )
        _safe_edit_or_send(call, text, kb)
    else:
        _safe_edit_or_send(call, buy_main_text_ru(), build_buy_markup_ru())
    bot.answer_callback_query(call.id)
