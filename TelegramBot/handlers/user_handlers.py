from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup

class StickerOrder(StatesGroup):
    waiting_for_tx = State()
    waiting_for_username = State()
    waiting_for_purpose = State()

def register_user_handlers(dp: Dispatcher):
    @dp.message_handler(commands=["start"])
    async def start_command(message: types.Message):
        await message.answer("Привет! Это KafkaBot 🐿")

