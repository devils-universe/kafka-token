from aiogram import types, Dispatcher

async def start_command(message: types.Message):
    await message.answer("Привет! Это KafkaDropBot. Введи /tasks, чтобы начать выполнять задания.")

async def tasks_command(message: types.Message):
    await message.answer("""🎯 Выбери задание:
1. Подписка на Twitter
2. Репост твита
3. Подписка на Telegram
4. История о белке-летяге""")

def register_user(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=["start"])
    dp.register_message_handler(tasks_command, commands=["tasks"])
