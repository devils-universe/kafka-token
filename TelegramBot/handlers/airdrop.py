from bot import bot
from telebot import types
from utils.language import t

def airdrop_main_text(uid) -> str:
    return (
        f"🎁 *{t(uid, 'airdrop_title')}*\n\n"
        f"{t(uid, 'airdrop_desc')}\n\n"
        f"{t(uid, 'airdrop_howto')}"
    )

def airdrop_main_markup(uid):
    kb = types.InlineKeyboardMarkup()
    kb.row(types.InlineKeyboardButton(t(uid, "follow_us"))
    

@bot.message_handler(func=lambda m: m.text in {"🎁 Airdrop", "🎁 Аирдроп"})
def handle_airdrop(message):
    uid = message.from_user.id
    bot.send_message(
        message.chat.id,
        airdrop_main_text(uid),
        parse_mode="Markdown",
        disable_web_page_preview=True,
        reply_markup=airdrop_main_markup(uid)
    )

@bot.callback_query_handler(func=lambda c: c.data == "airdrop_follow_us")
def cb_airdrop_follow_us(call):
    uid = call.from_user.id
    text = (
        f"📣 *{t(uid, 'follow_us')}:*\n"
        "• [TikTok](https://www.tiktok.com/@devils_kafka)\n"
        "• [X](https://x.com/devils_kafka)\n"
        "• [Facebook](https://www.facebook.com/devilsuniversecom)"
    )
   
