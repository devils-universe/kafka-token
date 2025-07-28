import os
from dotenv import load_dotenv
load_dotenv()
from telebot import TeleBot

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")

bot = TeleBot(BOT_TOKEN)