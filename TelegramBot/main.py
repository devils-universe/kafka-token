from bot import bot
import handlers.user_handlers
import handlers.buy
import handlers.tasks
import handlers.shoop
import handlers.airdrop
import handlers.game
import handlers.web

if __name__ == "__main__":
    bot.polling(none_stop=True)
