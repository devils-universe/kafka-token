import os
import telebot
from telebot import types
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
LOG_CHAT_ID = os.getenv("LOG_CHAT_ID")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")

bot = telebot.TeleBot(BOT_TOKEN)


def build_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(
        types.KeyboardButton("🪙 Buy $KAFKA"),
        types.KeyboardButton("🎭 Create Meme")
    )
    markup.row(types.KeyboardButton("📦 Buy sticker pack"))
    return markup


def send_menu(chat_id, text="Please choose an option:"):
    bot.send_message(chat_id, text, reply_markup=build_main_menu())


@bot.message_handler(commands=['start'])
def start_command(message):
    welcome = "Welcome to Kafka Life Bot! 🐿️ Buy $KAFKA, create memes, or order sticker packs."
    send_menu(message.chat.id, welcome)


@bot.message_handler(func=lambda msg: msg.text == "🪙 Buy $KAFKA")
def buy_kafka(message):
    bot.send_message(message.chat.id,
                     "You can buy $KAFKA here (Web3 OKX): https://web3.okx.com/ul/1KaUamm")
    send_menu(message.chat.id)


@bot.message_handler(func=lambda msg: msg.text == "🎭 Create Meme")
def create_meme(message):
    bot.send_message(message.chat.id,
                     "Send 42 $KAFKA to 0xef43a15a02345553702c2ef7daa1883e86792f6c and share your idea in our group: https://t.me/+LK08slIhqj1iZTMy")
    send_menu(message.chat.id)


@bot.message_handler(func=lambda msg: msg.text == "📦 Buy sticker pack")
def buy_sticker(message):
    sent = bot.send_message(message.chat.id, "Please provide the transaction hash (TX-hash) of your payment:")
    bot.register_next_step_handler(sent, receive_tx_hash)


def receive_tx_hash(message):
    tx_hash = message.text.strip()
    sent = bot.send_message(message.chat.id, "Thank you! Now, please enter your Telegram username (include @):")
    bot.register_next_step_handler(sent, receive_username, tx_hash)


def receive_username(message, tx_hash):
    username = message.text.strip()
    sent = bot.send_message(message.chat.id, "Got it. What did you pay for?")
    bot.register_next_step_handler(sent, receive_payment_info, tx_hash, username)


def receive_payment_info(message, tx_hash, username):
    purpose = message.text.strip()
    log_message = (
        f"Sticker Pack Order:\n"
        f"TX-hash: {tx_hash}\n"
        f"Telegram user: {username}\n"
        f"Payment for: {purpose}"
    )
    if LOG_CHAT_ID:
        bot.send_message(LOG_CHAT_ID, log_message)
    bot.send_message(message.chat.id, "Thanks! Kafka received your request. Stickers are coming 🐿️")
    send_menu(message.chat.id)


if __name__ == "__main__":
    bot.infinity_polling()