from bot import bot

# Импорт всех хендлеров (очень важно, чтобы они зарегистрировали свои обработчики)
import handlers.user_handlers
import handlers.base
import handlers.buy
import handlers.tasks
import handlers.shoop

if __name__ == "__main__":
    bot.remove_webhook()
    bot.infinity_polling(skip_pending=True)
