from bot import bot
import handlers.user_handlers
import handlers.buy
import handlers.tasks
import handlers.shop
import handlers.airdrop
import handlers.leaderboard
import handlers.stickers

if __name__ == "__main__":
    bot.polling(none_stop=True)
