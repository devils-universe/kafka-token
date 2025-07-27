from aiogram import types, Dispatcher

async def review_command(message: types.Message):
    await message.answer("📋 Задания на проверку пока отсутствуют.")

def register_admin(dp: Dispatcher):
    dp.register_message_handler(review_command, commands=["review"], is_chat_admin=True)
