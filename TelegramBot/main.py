from bot import bot
import handlers.user_handlers
import handlers.buy
import handlers.tasks

if __name__ == "__main__":
    bot.remove_webhook()
    bot.infinity_polling(skip_pending=True)
