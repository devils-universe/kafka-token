from bot import bot
from telebot import types
from utils.language import t

def game_main_text(uid) -> str:
    return f"🥭 {t(uid, 'coming_soon')}"

def game_main_markup(uid):
    return types.InlineKeyboardMarkup()

# Вход через reply‑кнопку (англ/рус)
@bot.message_handler(func=lambda m: m.text in {"🥭 Game", "🎮 Игра"})
def handle_game(message):
    uid = message.from_user.id
    bot.send_message(
        message.chat.id,
        game_main_text(uid),
        parse_mode="Markdown",
        disable_web_page_preview=True,
        reply_markup=game_main_markup(uid)
    )

def open(call):
    uid = call.from_user.id
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=game_main_text(uid),
        parse_mode="Markdown",
        disable_web_page_preview=True,
        reply_markup=game_main_markup(uid)
    )
