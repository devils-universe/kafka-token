from bot import bot
from telebot import types
from handlers.tasks import handle_tasks
from handlers.shoop import handle_shoop

@bot.message_handler(func=lambda msg: msg.text == "🪙 Buy $KAFKA")
def handle_buy(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔗 Buy $KAFKA", url="https://web3.okx.com/ru/token/bsc/0x0023caf04b4fac8b894fc7fa49d38ddc4606a816"))
    markup.add(
        types.InlineKeyboardButton("Earn/Mine 🪙Kafka", callback_data="to_tasks"),
        types.InlineKeyboardButton("Create  🪙Kafka", callback_data="to_shoop")
    )
    bot.send_message(message.chat.id, "Choose:", reply_markup=markup)

@bot.callback_query_handler(func=lambda c: c.data in ["to_tasks", "to_shoop"])
def inline(call):
    if call.data == "to_tasks":
        handle_tasks(call.message)
    else:
        handle_shoop(call.message)
    bot.answer_callback_query(call.id)
