import handlers.user_handlers
from bot import bot
import handlers.base
import handlers.buy
import handlers.tasks
import handlers.shoop

if __name__ == "__main__":
    bot.remove_webhook()
    bot.infinity_polling()