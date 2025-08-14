from bot import bot

# --- базовые разделы/хэндлеры ---
import handlers.user_handlers   # меню, старт и т.п.
import handlers.tasks
import handlers.airdrop
import handlers.game
import handlers.web

# --- BUY (разнесённые по языкам) ---
import handlers.buy_ru          # RU покупки
import handlers.buy_en          # EN покупки

# --- SHOP (общие + по языкам) ---
import handlers.shop_common     # общие константы/хелперы (должен грузиться до ru/en)
import handlers.shop_ru         # RU магазин
import handlers.shop_en         # EN shop

# --- Патчи/локальные фиксы (если реально нужен этот модуль) ---
import handlers.base_ru_patch   # если он есть; иначе удалите эту строку

if __name__ == "__main__":
    # infinity_polling устойчивее к обрывам соединения
    bot.infinity_polling(skip_pending=True, timeout=20)
