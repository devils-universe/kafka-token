from bot import bot
from telebot import types
import logging

CONTRACT = "0x0023caf04B4fAc8B894Fc7fA49d38ddc4606a816"

def buy_main_text_en() -> str:
    return (
        "🪙 *Buy $KAFKA*\n"
        "_BEP-20 on BNB Smart Chain_\n\n"
        f"• *Contract:* `{CONTRACT}`\n"
        "• Decimals: `18`\n"
        "• Slippage: usually `0.5–1%`\n\n"
        "👉 Choose a platform below. If first time — click *How to Buy*."
    )

def build_buy_markup_en() -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=3)
    kb.row(
        types.InlineKeyboardButton("🎲 OKX", url="https://web3.okx.com/token/bsc/0x0023caf04b4fac8b894fc7fa49d38ddc4606a816"),
        types.InlineKeyboardButton("🥞 Pancake", url="https://pancakeswap.finance/swap?outputCurrency=0x0023caf04b4fac8b894fc7fa49d38ddc4606a816&chain=bsc"),
        types.InlineKeyboardButton("🌶 Paprika", url="https://coinpaprika.com/coin/kafka-kafka/")
    )
    kb.row(
        types.InlineKeyboardButton("📈 GeckoTerminal", url="https://www.geckoterminal.com/bsc/tokens/0x0023caf04b4fac8b894fc7fa49d38ddc4606a816"),
        types.InlineKeyboardButton("🔎 BscScan", url="https://bscscan.com/token/0x0023caf04B4fAc8B894Fc7fA49d38ddc4606a816"),
        types.InlineKeyboardButton("📢 Support", url="https://t.me/devils_kafka")
    )
    kb.row(
        types.InlineKeyboardButton("📋 Copy CA", callback_data="buy_copy_ca"),
        types.InlineKeyboardButton("❓ How to Buy", callback_data="buy_howto_en")
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
        logging.warning(f"[buy_en] edit_message_text failed: {e}. Sending new message.")
        bot.send_message(
            call.message.chat.id,
            text,
            parse_mode="Markdown",
            disable_web_page_preview=True,
            reply_markup=reply_markup
        )

@bot.message_handler(func=lambda msg: getattr(msg, "text", "") == "🪙 Buy $KAFKA")
def handle_buy_en_message(message):
    bot.send_message(
        message.chat.id,
        buy_main_text_en(),
        parse_mode="Markdown",
        disable_web_page_preview=True,
        reply_markup=build_buy_markup_en()
    )

@bot.callback_query_handler(func=lambda c: isinstance(getattr(c, "data", None), str)
                                       and (c.data == "open_buy" or c.data.startswith("buy_")))
def cb_buy_en(call):
    from utils.language import t, get_lang
    if get_lang(call.from_user.id) != 'en':
        return
    data = call.data
    if data == "open_buy":
        _safe_edit_or_send(call, buy_main_text_en(), build_buy_markup_en())
    elif data == "buy_copy_ca":
        uid = call.from_user.id
        bot.answer_callback_query(call.id, t(uid, "contract_sent"))
        bot.send_message(
            call.message.chat.id,
            f"🔗 *$KAFKA Contract Address (BSC):*\n`{CONTRACT}`",
            parse_mode="Markdown",
            disable_web_page_preview=True
        )
    elif data == "buy_howto_en":
        text = (
            "❓ *How to buy $KAFKA*\n\n"
            "1) *Wallet*: MetaMask or OKX Wallet. Network — *BNB Smart Chain (BSC)*.\n"
            "2) *Fund BNB* for gas.\n"
            "3) *Import token*: add the contract:\n"
            f"`{CONTRACT}`\n"
            "4) *Swap on Pancake/OKX*: select $KAFKA by contract address.\n"
            "5) *Slippage*: start with 0.5–1%. If swap fails — slightly increase.\n\n"
            "💡 *Security*: double-check contract address and avoid unknown links."
        )
        kb = types.InlineKeyboardMarkup()
        kb.row(
            types.InlineKeyboardButton("🥞 Open Pancake", url="https://pancakeswap.finance/swap?outputCurrency=0x0023caf04b4fac8b894fc7fa49d38ddc4606a816&chain=bsc")
        )
        kb.row(
            types.InlineKeyboardButton("⬅️ Back", callback_data="open_buy"),
            types.InlineKeyboardButton("📋 Copy CA", callback_data="buy_copy_ca")
        )
        _safe_edit_or_send(call, text, kb)
    else:
        _safe_edit_or_send(call, buy_main_text_en(), build_buy_markup_en())
    bot.answer_callback_query(call.id)
    
