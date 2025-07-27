from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentTypes
from aiogram.dispatcher.filters.state import State, StatesGroup
import config


class StickerOrder(StatesGroup):
    waiting_for_tx = State()
    waiting_for_username = State()
    waiting_for_purpose = State()


class TaskSubmission(StatesGroup):
    waiting_for_screenshot = State()


def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("\u041A\u0443\u043F\u0438\u0442\u044C KAFKA")
    markup.row("\u0423\u0441\u043B\u0443\u0433\u0438")
    markup.row("\u0417\u0430\u0434\u0430\u043D\u0438\u044F")
    return markup


async def start(message: types.Message):
    await message.answer(
        "\u041F\u0440\u0438\u0432\u0435\u0442! \u042F KafkaDropBot. \u0412\u044B\u0431\u0435\u0440\u0438\u0442\u0435 \u0434\u0435\u0439\u0441\u0442\u0432\u0438\u0435:",
        reply_markup=main_menu(),
    )


async def buy(message: types.Message):
    await message.answer(
        "\u0427\u0442\u043E\u0431\u044B \u043A\u0443\u043F\u0438\u0442\u044C $KAFKA, \u043F\u043E\u0441\u0435\u0442\u0438\u0442\u0435 https://devilsuniverse.com \u0438\u043B\u0438 \u0438\u0441\u043F\u043E\u043B\u044C\u0437\u0443\u0439\u0442\u0435 \u043A\u043E\u043D\u0442\u0440\u0430\u043A\u0442 0x0023caf04B4fAc8B894Fc7fA49d38ddc4606a816."
    )


async def services(message: types.Message):
    await message.answer("\u041C\u044B \u043F\u0440\u0435\u0434\u043B\u0430\u0433\u0430\u0435\u043C NFT, \u0441\u0442\u0438\u043A\u0435\u0440\u044B \u0438 \u0434\u0440\u0443\u0433\u0438\u0435 \u0443\u0441\u043B\u0443\u0433\u0438.")


async def tasks(message: types.Message):
    await message.answer("\u0412\u044B\u043F\u043E\u043B\u043D\u044F\u0439\u0442\u0435 \u0437\u0430\u0434\u0430\u043D\u0438\u044F \u0441\u043E\u043E\u0431\u0449\u0435\u0441\u0442\u0432\u0430 \u0438 \u043F\u043E\u043B\u0443\u0447\u0430\u0439\u0442\u0435 \u043D\u0430\u0433\u0440\u0430\u0434\u044B.")


async def log_sticker(message: types.Message):
    if config.LOG_CHAT_ID:
        await message.bot.forward_message(
            chat_id=int(config.LOG_CHAT_ID),
            from_chat_id=message.chat.id,
            message_id=message.message_id,
        )


def register_user_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(start, commands=["start"])
    dp.register_message_handler(buy, lambda m: m.text == "\u041A\u0443\u043F\u0438\u0442\u044C KAFKA")
    dp.register_message_handler(services, lambda m: m.text == "\u0423\u0441\u043B\u0443\u0433\u0438")
    dp.register_message_handler(tasks, lambda m: m.text == "\u0417\u0430\u0434\u0430\u043D\u0438\u044F")
    dp.register_message_handler(log_sticker, content_types=ContentTypes.STICKER)
