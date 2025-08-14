from bot import bot
from telebot import types
import os
import urllib.parse

# === SHARED CONFIG ===
PAYMENT_ADDRESS = "0xaa0de276F5E87730431A032aD335D21EFd133Fa9"

RELIC_R001_PHOTOS = [
    "assets/shoop/du_shop_final_01_square.jpg",
    "assets/shoop/du_shop_final_02_square.jpg",
    "assets/shoop/du_shop_final_03_square.jpg",
]

# stickers used in both locales (replace/add if needed)
STICKER_IDS = [
    "CAACAgIAAxkBAAIBuWiHKOetWo-SdCruW2yorH8Wi15nAAI8ewACL4IoSIc0a3D7YkOpNgQ",
    "CAACAgIAAxkBAAIBuGiHKNz3c9yTLXQ7lLYcBm7IkvZdAAILfQACTjAgSKxOMQABd531PTYE",
    "CAACAgIAAxkBAAIBxmiHKqMAAYDeYfoAARz-6wGbE74EQL4AAut6AAKcrClIURryc3I7N242BA"
]

def safe_edit_or_send(call, text, reply_markup=None):
    try:
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=text,
            parse_mode="Markdown",
            disable_web_page_preview=True,
            reply_markup=reply_markup
        )
    except Exception:
        bot.send_message(
            call.message.chat.id,
            text,
            parse_mode="Markdown",
            disable_web_page_preview=True,
            reply_markup=reply_markup
        )

def send_relic_photos_group(chat_id: int, caption: str | None = None):
    """Sends media group of RELIC_R001_PHOTOS. Caption only on first image."""
    media = []
    open_files = []
    caption_set = False
    for path in RELIC_R001_PHOTOS:
        if not os.path.exists(path):
            continue
        f = open(path, "rb")
        open_files.append(f)
        if not caption_set and caption:
            media.append(types.InputMediaPhoto(f, caption=caption, parse_mode="Markdown"))
            caption_set = True
        else:
            media.append(types.InputMediaPhoto(f))
    if media:
        try:
            bot.send_media_group(chat_id, media)
        finally:
            for f in open_files:
                try:
                    f.close()
                except Exception:
                    pass

def build_share_button(text_label: str, share_text: str) -> types.InlineKeyboardButton:
    encoded = urllib.parse.quote(share_text, safe='')
    return types.InlineKeyboardButton(
        text_label,
        url=f"https://t.me/share/url?url={PAYMENT_ADDRESS}&text={encoded}"
    )
