from aiogram import Bot, Dispatcher
from aiogram.utils import executor
import config
from handlers.user_handlers import register_user_handlers


def main() -> None:
    if not config.BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is not set")

    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher(bot)

    register_user_handlers(dp)

    executor.start_polling(dp)


if __name__ == "__main__":
    main()
