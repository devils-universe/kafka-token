from bot import bot
from telebot import types
from handlers.shoop import handle_shoop

@bot.message_handler(func=lambda msg: msg.text == "🪙 Buy $KAFKA")
def handle_buy(message):
    markup = types.InlineKeyboardMarkup(row_width=3)
    markup.row(
        types.InlineKeyboardButton("🎲 OKX", url="https://web3.okx.com/ru/token/bsc/0x0023caf04b4fac8b894fc7fa49d38ddc4606a816"),
        types.InlineKeyboardButton("🥞 Pancake", url="https://pancakeswap.finance/swap?outputCurrency=0x0023caf04b4fac8b894fc7fa49d38ddc4606a816&chain=bsc"),
        types.InlineKeyboardButton("🌶 Paprika", url="https://coinpaprika.com/coin/kafka-kafka/")
    )
    bot.send_message(message.chat.id, "Choose:", reply_markup=markup)
