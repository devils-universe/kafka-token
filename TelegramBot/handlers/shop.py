from bot import bot
from telebot import types
import requests

import os
BSC_SCAN_API_KEY = os.getenv("BSC_SCAN_API_KEY")
EXPECTED_RECEIVER = "0xaa0de276f5e87730431a032ad335d21efd133fa9"
EXPECTED_AMOUNT = 42 * 10**18  # 42 KAFKA (в wei)
EXPECTED_COMMENT_HEX = "0x737469636b657273"  # "stickers" в hex

@bot.message_handler(func=lambda msg: msg.text == "🛒 Shoop")
def handle_shoop(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🎨 Create a Meme", url="https://devilsuniverse.com/#container04"))
    markup.add(types.InlineKeyboardButton("🛍 Open Sticker Store", callback_data="open_sticker_store"))
    bot.send_message(message.chat.id, "🎨 Want to create or receive Kafka-themed fun?\n\nChoose an option:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "open_sticker_store")
def handle_sticker_store(call):
    sticker_ids = [
        "CAACAgIAAxkBAAIBuWiHKOetWo-SdCruW2yorH8Wi15nAAI8ewACL4IoSIc0a3D7YkOpNgQ",
        "CAACAgIAAxkBAAIBuGiHKNz3c9yTLXQ7lLYcBm7IkvZdAAILfQACTjAgSKxOMQABd531PTYE",
        "CAACAgIAAxkBAAIBxmiHKqMAAYDeYfoAARz-6wGbE74EQL4AAut6AAKcrClIURryc3I7N242BA"
    ]
    for sid in sticker_ids:
        bot.send_sticker(call.message.chat.id, sid)
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
    sent = bot.send_message(message.chat.id, "🔍 Please enter your transaction hash:")
    bot.register_next_step_handler(sent, check_transaction)

def check_transaction(message):
    tx_hash = message.text.strip()
    bot.send_message(message.chat.id, f"ℹ️ Checking TX: `{tx_hash}`", parse_mode="Markdown")
    url = f"https://api.bscscan.com/api?module=proxy&action=eth_getTransactionByHash&txhash={tx_hash}&apikey={BSC_SCAN_API_KEY}"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        bot.send_message(message.chat.id, "❌ Error contacting BscScan:\n" + str(e))
        return

    result = resp.json().get("result")
    if not result:
        bot.send_message(message.chat.id, "❌ Transaction not found or still pending.")
        return

    to_addr = result.get("to","").lower()
    value = int(result.get("value","0x0"), 16)
    input_data = result.get("input","").lower()

    debug = (
        f"**DEBUG INFO**\n"
        f"- to: `{to_addr}`\n"
        f"- value: `{value}`\n"
        f"- input begins with: `{input_data[:20]}`…"
    )
    bot.send_message(message.chat.id, debug, parse_mode="Markdown")

    if to_addr == EXPECTED_RECEIVER and value == EXPECTED_AMOUNT and EXPECTED_COMMENT_HEX in input_data:
        bot.send_message(message.chat.id,
            "✅ Transaction confirmed!\nHere's your sticker pack:\nhttps://t.me/addstickers/KafkaLife2"
        )
    else:
        bot.send_message(message.chat.id,
            "⚠️ Invalid transaction:\n"
            "- must send exactly 42 $KAFKA\n"
            "- to correct wallet\n"
            "- include `stickers` in comment"
        )
