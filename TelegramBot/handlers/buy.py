from telebot import types
from bot import bot
from handlers.tasks import handle_tasks
from handlers.shoop import handle_shoop


@bot.message_handler(func=lambda msg: msg.text == "🪙 Buy $KAFKA")
def handle_buy(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔗 Buy $KAFKA", url="https://web3.okx.com/ul/1KaUamm"))
    markup.add(
        types.InlineKeyboardButton("🪙 Earn / Mine", callback_data="to_tasks"),
        types.InlineKeyboardButton("🎨 Spend / Create", callback_data="to_shoop")
    )
    bot.send_message(
        message.chat.id,
        "What would you like to do with $KAFKA?",
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: call.data in ["to_tasks", "to_shoop"])
def handle_inline_buttons(call):
    if call.data == "to_tasks":
        handle_tasks(call.message)
    elif call.data == "to_shoop":
        handle_shoop(call.message)

    bot.answer_callback_query(call.id)