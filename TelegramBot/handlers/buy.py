# handlers/buy.py
from bot import bot
from telebot import types

CONTRACT = "0x0023caf04B4fAc8B894Fc7fA49d38ddc4606a816"
SITE = "https://devilsuniverse.com"

def build_buy_markup() -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=3)
    # Row 1 — Buy
    kb.row(
        types.InlineKeyboardButton("🎲 OKX", url="https://web3.okx.com/ru/token/bsc/0x0023caf04b4fac8b894fc7fa49d38ddc4606a816"),
        types.InlineKeyboardButton("🥞 Pancake", url="https://pancakeswap.finance/swap?outputCurrency=0x0023caf04b4fac8b894fc7fa49d38ddc4606a816&chain=bsc"),
        types.InlineKeyboardButton("🌶 Paprika", url="https://coinpaprika.com/coin/kafka-kafka/")
    )
    # Row 2 — Charts & Explorer
    kb.row(
        types.InlineKeyboardButton("📈 GeckoTerminal", url="https://www.geckoterminal.com/bsc/tokens/0x0023caf04b4fac8b894fc7fa49d38ddc4606a816"),
        types.InlineKeyboardButton("🔎 BscScan", url="https://bscscan.com/token/0x0023caf04B4fAc8B894Fc7fA49d38ddc4606a816"),
        types.InlineKeyboardButton("📢 Support", url="https://t.me/devils_kafka")
    )
    # Row 3 — Utilities
    kb.row(
        types.InlineKeyboardButton("📋 Copy CA", callback_data="buy_copy_ca"),
        types.InlineKeyboardButton("❓ How to buy", callback_data="buy_howto")
    )
    return kb

def buy_main_text() -> str:
    return (
        "🪙 *Buy $KAFKA*\n"
        "_BEP-20 on BNB Smart Chain_\n\n"
        f"• *Contract:* `{CONTRACT}`\n"
        "• Decimals: `18`\n"
        "• Slippage: typically `0.5–1%`\n\n"
        "👉 Choose a platform below. If it's your first time — tap *How to buy*."
    )

@bot.message_handler(func=lambda msg: msg.text == "🪙 Buy $KAFKA")
def handle_buy(message):
    bot.send_message(
        message.chat.id,
        buy_main_text(),
        parse_mode="Markdown",
        disable_web_page_preview=True,
        reply_markup=build_buy_markup()
    )

@bot.callback_query_handler(func=lambda c: c.data == "buy_copy_ca")
def cb_buy_copy_ca(call):
    # Send separately — easy to highlight and copy
    bot.answer_callback_query(call.id, "Contract address sent.")
    bot.send_message(
        call.message.chat.id,
        f"🔗 *$KAFKA Contract (BSC):*\n`{CONTRACT}`",
        parse_mode="Markdown",
        disable_web_page_preview=True
    )

@bot.callback_query_handler(func=lambda c: c.data == "buy_howto")
def cb_buy_howto(call):
    text = (
        "❓ *How to buy $KAFKA*\n\n"
        "1) *Wallet*: MetaMask or OKX Wallet. Network — *BNB Smart Chain (BSC)*.\n"
        "2) *Fund BNB* for gas.\n"
        "3) *Import token*: add the contract:\n"
        f"`{CONTRACT}`\n"
        "4) *Swap on Pancake/OKX*: select $KAFKA by contract address.\n"
        "5) *Slippage*: start with 0.5–1%. If the swap fails — increase a bit.\n\n"
        "💡 *Safety*: verify the contract address and avoid unknown links."
    )
    kb = types.InlineKeyboardMarkup()
    kb.row(
        types.InlineKeyboardButton("🥞 Open Pancake", url="https://pancakeswap.finance/swap?outputCurrency=0x0023caf04b4fac8b894fc7fa49d38ddc4606a816&chain=bsc")
    )
    kb.row(
        types.InlineKeyboardButton("⬅️ Back", callback_data="buy_back"),
        types.InlineKeyboardButton("📋 Copy CA", callback_data="buy_copy_ca")
    )
    # Nicer UX — edit the current message instead of spamming the chat
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=text,
        parse_mode="Markdown",
        disable_web_page_preview=True,
        reply_markup=kb
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda c: c.data == "buy_back")
def cb_buy_back(call):
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=buy_main_text(),
        parse_mode="Markdown",
        disable_web_page_preview=True,
        reply_markup=build_buy_markup()
    )
    bot.answer_callback_query(call.id)
