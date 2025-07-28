from bot import bot
from telebot import types
import requests

BSC_SCAN_API_KEY = "H3S5XR457E15E3WFDQBMPQABBRQMMRVXKG"
EXPECTED_RECEIVER = "0xaa0de276f5e87730431a032ad335d21efd133fa9"
EXPECTED_AMOUNT = 42000000000000000000  # 42 KAFKA в wei
EXPECTED_INPUT_HEX = "0x737469636b657273"  # hex-код "stickers"

@bot.message_handler(func=lambda msg: msg.text == "🛒 Shoop")
def handle_shoop(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🎨 Create a Meme", url="https://devilsuniverse.com/#container04"))
    markup.add(types.InlineKeyboardButton("🛍 Open Sticker Store", callback_data="open_sticker_store"))

    bot.send_message(
        message.chat.id,
        "🎨 Want to create or receive Kafka-themed fun?\n\nChoose an option below:",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "open_sticker_store")
def handle_sticker_store(call):
    sticker_ids = [
        "CAACAgIAAxkBAAIBuWiHKOetWo-SdCruW2yorH8Wi15nAAI8ewACL4IoSIc0a3D7YkOpNgQ",
        "CAACAgIAAxkBAAIBuGiHKNz3c9yTLXQ7lLYcBm7IkvZdAAILfQACTjAgSKxOMQABd531PTYE",
        "CAACAgIAAxkBAAIBxmiHKqMAAYDeYfoAARz-6wGbE74EQL4AAut6AAKcrClIURryc3I7N242BA"
    ]
    for sticker_id in sticker_ids:
        bot.send_sticker(call.message.chat.id, sticker_id)

    msg = (
        "🎁 *To receive the full Kafka sticker pack:*\n"
        "1. Send *42 $KAFKA* to wallet:\n"
        "`0xaa0de276f5e87730431a032ad335d21efd133fa9`\n"
        "2. In the transaction comment, write: `stickers`\n"
        "3. Press the button below to send your TX hash 🧾"
    )
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("🧾 Send TX hash"))

    bot.send_message(call.message.chat.id, msg, parse_mode="Markdown", reply_markup=markup)
    bot.answer_callback_query(call.id)

@bot.message_handler(func=lambda msg: msg.text == "🧾 Send TX hash")
def ask_tx_hash(message):
    msg = bot.send_message(message.chat.id, "🔍 Please enter your transaction hash:")
    bot.register_next_step_handler(msg, check_transaction)

def check_transaction(message):
    tx_hash = message.text.strip()
    url = f"https://api.bscscan.com/api?module=proxy&action=eth_getTransactionByHash&txhash={tx_hash}&apikey={BSC_SCAN_API_KEY}"
    response = requests.get(url)

    if response.status_code != 200:
        bot.send_message(message.chat.id, "❌ Error contacting BscScan. Try again later.")
        return

    data = response.json().get("result")
    if not data:
        bot.send_message(message.chat.id, "❌ Transaction not found. Please double-check the hash.")
        return

    to_address = data.get("to", "").lower()
    value = int(data.get("value", "0x0"), 16)
    input_data = data.get("input", "").lower()

    if to_address == EXPECTED_RECEIVER and value == EXPECTED_AMOUNT and EXPECTED_INPUT_HEX in input_data:
        bot.send_message(
            message.chat.id,
            "✅ Transaction confirmed!\nHere is your Kafka sticker pack:\nhttps://t.me/addstickers/KafkaLife2"
        )
    else:
        bot.send_message(
            message.chat.id,
            "⚠️ Transaction doesn't match required parameters:\n"
            "- 42 $KAFKA\n"
            "- Receiver: correct wallet\n"
            "- Comment: `stickers`"
        )
