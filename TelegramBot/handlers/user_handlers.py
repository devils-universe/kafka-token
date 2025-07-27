 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/TelegramBot/handlers/user_handlers.py b/TelegramBot/handlers/user_handlers.py
index a7fb7ec51a2904980429d5aff575d412b1cdfa7f..134d0394dd014582aad4ff6ea1b8500fe49c2d80 100644
--- a/TelegramBot/handlers/user_handlers.py
+++ b/TelegramBot/handlers/user_handlers.py
@@ -1,15 +1,132 @@
 from aiogram import types, Dispatcher
+from aiogram.types import ContentTypes
+from aiogram.dispatcher import FSMContext
+from aiogram.dispatcher.filters.state import State, StatesGroup
+import config
+
+
+def main_menu() -> types.ReplyKeyboardMarkup:
+    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
+    markup.row("\ud83e\ude99 Buy $KAFKA", "\ud83c\udf81 Services")
+    markup.row("\ud83d\udccb Tasks")
+    return markup
+
+
+class StickerOrder(StatesGroup):
+    waiting_for_tx = State()
+    waiting_for_username = State()
+    waiting_for_purpose = State()
+
+
+class TaskSubmission(StatesGroup):
+    waiting_for_screenshot = State()
+
 
 async def start_command(message: types.Message):
-    await message.answer("Привет! Это KafkaDropBot. Введи /tasks, чтобы начать выполнять задания.")
+    await message.answer(
+        "Welcome to Kafka Life Bot! \ud83d\udc3f\ufe0f Choose an option:",
+        reply_markup=main_menu(),
+    )
+
+
+async def buy_kafka(message: types.Message):
+    await message.answer(
+        "You can buy $KAFKA here (Web3 OKX): https://web3.okx.com/ul/1KaUamm",
+        reply_markup=main_menu(),
+    )
+
+
+async def show_services(message: types.Message):
+    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
+    markup.row("\ud83c\udf9d Create Meme", "\ud83d\udce6 Buy sticker pack")
+    markup.row("\ud83d\udd19 Back")
+    await message.answer("Select a service:", reply_markup=markup)
+
+
+async def show_tasks(message: types.Message):
+    text = (
+        "\ud83c\udfaf Available tasks:\n"
+        "1. Twitter subscription\n"
+        "2. Retweet our post\n"
+        "3. Telegram subscription\n"
+        "4. Story about the flying squirrel\n\n"
+        "Send a screenshot after completing the tasks."
+    )
+    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
+    markup.row("\ud83d\udd19 Back")
+    await message.answer(text, reply_markup=markup)
+    await TaskSubmission.waiting_for_screenshot.set()
+
+
+async def back_to_menu(message: types.Message, state: FSMContext):
+    if state:
+        await state.finish()
+    await message.answer("Main menu:", reply_markup=main_menu())
+
+
+async def create_meme(message: types.Message):
+    await message.answer(
+        "Send 42 $KAFKA to 0xef43a15a02345553702c2ef7daa1883e86792f6c and share your idea in our group: https://t.me/+LK08slIhqj1iZTMy",
+        reply_markup=main_menu(),
+    )
+
+
+async def buy_sticker_start(message: types.Message):
+    await message.answer("Please provide the transaction hash (TX-hash) of your payment:")
+    await StickerOrder.waiting_for_tx.set()
+
+
+async def process_task_screenshot(message: types.Message, state: FSMContext):
+    if message.photo or message.document:
+        if config.LOG_CHAT_ID:
+            await message.forward(int(config.LOG_CHAT_ID))
+        await message.answer(
+            "Thanks! Your submission has been sent for review.",
+            reply_markup=main_menu(),
+        )
+        await state.finish()
+    else:
+        await message.answer("Please send a screenshot of your subscriptions.")
+
+
+async def process_tx(message: types.Message, state: FSMContext):
+    await state.update_data(tx_hash=message.text.strip())
+    await message.answer("Thank you! Now, please enter your Telegram username (include @):")
+    await StickerOrder.next()
+
+
+async def process_username(message: types.Message, state: FSMContext):
+    await state.update_data(telegram_username=message.text.strip())
+    await message.answer("Got it. What did you pay for?")
+    await StickerOrder.next()
+
+
+async def process_payment_purpose(message: types.Message, state: FSMContext):
+    data = await state.get_data()
+    tx_hash = data.get("tx_hash")
+    telegram_username = data.get("telegram_username")
+    payment_purpose = message.text.strip()
+    log_text = (
+        f"Sticker Pack Order:\nTX-hash: {tx_hash}\nTelegram user: {telegram_username}\nPayment for: {payment_purpose}"
+    )
+    if config.LOG_CHAT_ID:
+        await message.bot.send_message(int(config.LOG_CHAT_ID), log_text)
+    await message.answer(
+        "Thanks! Kafka received your request. Stickers are coming \ud83d\udc3f\ufe0f",
+        reply_markup=main_menu(),
+    )
+    await state.finish()
 
-async def tasks_command(message: types.Message):
-    await message.answer("""🎯 Выбери задание:
-1. Подписка на Twitter
-2. Репост твита
-3. Подписка на Telegram
-4. История о белке-летяге""")
 
 def register_user(dp: Dispatcher):
-    dp.register_message_handler(start_command, commands=["start"])
-    dp.register_message_handler(tasks_command, commands=["tasks"])
+    dp.register_message_handler(start_command, commands=["start"], state="*")
+    dp.register_message_handler(buy_kafka, lambda m: m.text == "\ud83e\ude99 Buy $KAFKA", state="*")
+    dp.register_message_handler(show_services, lambda m: m.text == "\ud83c\udf81 Services", state="*")
+    dp.register_message_handler(show_tasks, lambda m: m.text == "\ud83d\udccb Tasks", state="*")
+    dp.register_message_handler(create_meme, lambda m: m.text == "\ud83c\udf9d Create Meme", state="*")
+    dp.register_message_handler(buy_sticker_start, lambda m: m.text == "\ud83d\udce6 Buy sticker pack", state="*")
+    dp.register_message_handler(back_to_menu, lambda m: m.text == "\ud83d\udd19 Back", state="*")
+    dp.register_message_handler(process_task_screenshot, state=TaskSubmission.waiting_for_screenshot, content_types=ContentTypes.ANY)
+    dp.register_message_handler(process_tx, state=StickerOrder.waiting_for_tx)
+    dp.register_message_handler(process_username, state=StickerOrder.waiting_for_username)
+    dp.register_message_handler(process_payment_purpose, state=StickerOrder.waiting_for_purpose)
 
EOF
)
