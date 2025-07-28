from bot import bot
from telebot import types
from handlers.tasks import handle_tasks
from handlers.shoop import handle_shoop


@bot.message_handler(func=lambda msg: msg.text == "🪙 Buy $KAFKA")
def handle_buy(message):
    markup = types.InlineKeyboardMarkup(row_width=3)

    # Первая строка — ссылки на биржи
    markup.row(
        types.InlineKeyboardButton("🎲 OKX", url="https://web3.okx.com/ru/token/bsc/0x0023caf04b4fac8b894fc7fa49d38ddc4606a816"),
        types.InlineKeyboardButton("🥞 Pancake", url="https://pancakeswap.finance/swap?outputCurrency=0x0023caf04b4fac8b894fc7fa49d38ddc4606a816&chain=bsc"),
        types.InlineKeyboardButton("🌶 Paprika", url="https://coinpaprika.com/coin/kafka-kafka/")
    )

    # Вторая строка — действия
    markup.row(
        types.InlineKeyboardButton("⚒️ Mine $Kafka", callback_data="to_tasks"),
        types.InlineKeyboardButton("🛠️ Create $Kafka", callback_data="to_shoop")
    )

    bot.send_message(message.chat.id, "Choose:", reply_markup=markup)


@bot.callback_query_handler(func=lambda c: c.data in ["to_tasks", "to_shoop"])
def inline(call):
    if call.data == "to_tasks":
        handle_tasks(call.message)
    elif call.data == "to_shoop":
        handle_shoop(call.message)
    bot.answer_callback_query(call.id)
