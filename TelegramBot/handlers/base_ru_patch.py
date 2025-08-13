from telebot import types
from bot import bot

# импортируем модули разделов
import handlers.tasks as tasks
import handlers.shoop as shoop
import handlers.airdrop as airdrop
import handlers.game as game
import handlers.web as web

# --- Главное меню (ReplyKeyboard) — опционально ---
def main_menu_ru() -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("📋 Задания", "🛒 Магазин", "🪙 Купить $KAFKA")
    return markup

# --- Инлайн-меню (для навигации без новых сообщений) ---
def inline_root_ru() -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup()
    kb.row(
        types.InlineKeyboardButton("🪙 Купить $KAFKA", callback_data="open_buy"),
        types.InlineKeyboardButton("📋 Задания", callback_data="open_tasks"),
    )
    kb.row(
        types.InlineKeyboardButton("🛒 Магазин", callback_data="open_shoop"),
        types.InlineKeyboardButton("🎁 Аирдроп", callback_data="open_airdrop"),
        types.InlineKeyboardButton("🎮 Игра", callback_data="open_game"),
    )
    kb.row(
        types.InlineKeyboardButton("🌐 Веб", callback_data="open_web")
    )
    return kb

# --- Универсальный вызов "главного экрана" модуля ---
def _try_call(module, call):
    """
    Пытаемся найти и вызвать в модуле одну из функций
    для открытия раздела. Порядок подобран по частым паттернам.
    Функция может принимать либо (call), либо (message).
    Возвращаем True, если что-то вызвали, иначе False.
    """
    candidates = [
        "open_inline", "open_ru", "open",
        "show_inline", "show_main", "show",
        "render", "start_inline", "start",
        "handle_inline", "handle_main", "handle",
    ]
    for name in candidates:
        func = getattr(module, name, None)
        if callable(func):
            try:
                # пробуем (call)
                func(call)
                return True
            except TypeError:
                # пробуем (message)
                try:
                    func(call.message)
                    return True
                except TypeError:
                    pass
    return False

# --- Роутер по колбэкам ---
ROUTES = {
    "open_tasks":   tasks,
    "open_shoop":   shoop,
    "open_airdrop": airdrop,
    "open_game":    game,
    "open_web":     web,
    # "open_buy" обрабатывается в handlers.buy_ru (там свой хэндлер cb_open_buy)
}

@bot.callback_query_handler(func=lambda c: getattr(c, "data", "") in ROUTES)
def cb_open_section_ru(call):
    bot.answer_callback_query(call.id)  # снимаем “крутилку” сразу

    module = ROUTES[call.data]
    if _try_call(module, call):
        # модуль сам отрисовал экран (желательно через edit_message_text)
        return

    # Фолбэк, если модуль не дал входной точки
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="Раздел в разработке.",
        reply_markup=inline_root_ru()
    )
