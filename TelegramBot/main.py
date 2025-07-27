import os
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

# Load token from .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
LOG_CHAT_ID = os.getenv("LOG_CHAT_ID")

# URLs
OKX_URL = "https://web3.okx.com/ul/5fbVPiy"
PANCAKE_URL = "https://pancakeswap.finance/swap?outputCurrency=0x0023caf04b4fac8b894fc7fa49d38ddc4606a816&chain=bsc"
TWITTER_URL = "https://twitter.com/devils_kafka"
TELEGRAM_URL = "https://t.me/devilsuniversecom"
FACEBOOK_URL = "https://www.facebook.com/devilsuniversecom"
STICKER_URL = "https://devilsuniverse.com/stickers"
MEME_URL = "https://devilsuniverse.com/meme-tool"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("\uD83D\uDCB0 Купить $KAFKA", callback_data="buy")],
        [InlineKeyboardButton("\u2699\uFE0F Услуги", callback_data="services")],
        [InlineKeyboardButton("\uD83D\uDCB8 Задания", callback_data="tasks")],
    ]
    await update.message.reply_text(
        "Выберите действие:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

async def buy_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("Купить на OKX", url=OKX_URL)],
        [InlineKeyboardButton("Купить на PancakeSwap", url=PANCAKE_URL)],
        [InlineKeyboardButton("\u2B05\uFE0F Назад", callback_data="start")],
    ]
    await query.edit_message_text(
        "Где купить $KAFKA:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

async def services_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("Создать мем", url=MEME_URL)],
        [InlineKeyboardButton("Купить стикерпак", url=STICKER_URL)],
        [InlineKeyboardButton("\u2B05\uFE0F Назад", callback_data="start")],
    ]
    await query.edit_message_text(
        "Выберите услугу:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

async def tasks_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("Twitter", url=TWITTER_URL)],
        [InlineKeyboardButton("Telegram", url=TELEGRAM_URL)],
        [InlineKeyboardButton("Facebook", url=FACEBOOK_URL)],
        [InlineKeyboardButton("\u2705 Я выполнил", callback_data="check_tasks")],
        [InlineKeyboardButton("\u2B05\uFE0F Назад", callback_data="start")],
    ]
    await query.edit_message_text(
        "Подпишитесь на наши соцсети и нажмите \"Я выполнил\":",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

async def check_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    try:
        member = await context.bot.get_chat_member(chat_id="@devilsuniversecom", user_id=user_id)
        telegram_ok = member.status in ("member", "creator", "administrator")
    except Exception:
        telegram_ok = False

    result = "\u2705 Подписка на Telegram проверена." if telegram_ok else "\u274C Не подписан на Telegram."
    await query.edit_message_text(result)

    if LOG_CHAT_ID:
        text = f"User {query.from_user.mention_html()} submitted tasks. Telegram: {'OK' if telegram_ok else 'FAIL'}"
        await context.bot.send_message(LOG_CHAT_ID, text, parse_mode="HTML")

async def router(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if query.data == "buy":
        await buy_menu(update, context)
    elif query.data == "services":
        await services_menu(update, context)
    elif query.data == "tasks":
        await tasks_menu(update, context)
    elif query.data == "check_tasks":
        await check_tasks(update, context)
    elif query.data == "start":
        await start(update, context)


def main() -> None:
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is not set")

    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(router))

    application.run_polling()


if __name__ == "__main__":
    main()
