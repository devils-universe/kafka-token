from bot import bot

# --- базовые разделы/хэндлеры ---
import handlers.user_handlers      # меню, старт и т.п.
import handlers.airdrop
import handlers.game
import handlers.web

# --- BUY (разнесённые по языкам) ---
import handlers.buy_ru             # RU покупки
import handlers.buy_en             # EN покупки

# --- SHOP (общие + по языкам) ---
import handlers.shop_common        # общие константы/хелперы (грузим до ru/en)
import handlers.shop_ru            # RU магазин
import handlers.shop_en            # EN shop

# --- TASKS (общие + по языкам) ---
import handlers.tasks_common       # общий safe_edit_or_send
import handlers.tasks_ru           # RU задания
import handlers.tasks_en           # EN tasks

# --- Патчи/локальные фиксы (если реально нужен этот модуль) ---
# import handlers.base_ru_patch    # удалите или оставьте при необходимости

if __name__ == "__main__":
    # infinity_polling устойчивее к обрывам соединения и пропускает «залежавшиеся» апдейты
    bot.infinity_polling(skip_pending=True, timeout=20)
