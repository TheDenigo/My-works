import asyncio
import logging
import threading
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from config import TELEGRAM_TOKEN, GIFT_TYPE, PROMO_CODE, GIFT_IMAGE_PATH, GIFT_FILE_PATH
from google_sheets import GoogleSheetsClient


class GiftForm(StatesGroup):
    waiting_for_phone = State()


class TelegramBot:
    def __init__(self, stop_event: threading.Event):
        self.token = TELEGRAM_TOKEN
        self.bot = Bot(token=self.token)
        self.storage = MemoryStorage()
        self.dp = Dispatcher(self.bot, storage=self.storage)
        self.sheets = GoogleSheetsClient()
        self.stop_event = stop_event
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self._start_polling, daemon=True)

        self._setup_handlers()

    def start(self):
        logging.info("✅ TelegramBot запускается...")
        self.thread.start()

    def stop(self):
        self.stop_event.set()
        logging.info("🛑 TelegramBot остановлен.")

    def _start_polling(self):
        asyncio.set_event_loop(self.loop)
        try:
            self.loop.run_until_complete(self._run())
        except Exception:
            logging.exception("❌ TelegramBot аварийно завершился")

    async def _run(self):
        await self.dp.start_polling()
        logging.info("▶️ TelegramBot начал polling")

    def _setup_handlers(self):
        @self.dp.message_handler(commands=['start'])
        async def cmd_start(message: types.Message, state: FSMContext):
            user_id = str(message.from_user.id)
            if self.sheets.has_received_gift(user_id):
                await message.answer("🔁 Вы уже получили подарок.")
                return

            await message.answer("📱 Пожалуйста, отправьте свой номер телефона:")
            await GiftForm.waiting_for_phone.set()

        @self.dp.message_handler(state=GiftForm.waiting_for_phone)
        async def process_phone(message: types.Message, state: FSMContext):
            user_id = str(message.from_user.id)
            phone = message.text.strip()

            if not phone.startswith("+") or not phone[1:].isdigit():
                await message.answer("⚠️ Пожалуйста, введите номер в формате +79998887766.")
                return

            await self._send_gift(user_id, phone)
            await state.finish()

    async def _send_gift(self, user_id: str, phone: str):
        try:
            if GIFT_TYPE == "promo_code":
                await self.bot.send_message(user_id, f"🎁 Ваш промокод: {PROMO_CODE}")
            elif GIFT_TYPE == "image":
                with open(GIFT_IMAGE_PATH, "rb") as img:
                    await self.bot.send_photo(user_id, photo=img, caption="🎁 Ваш подарок:")
            elif GIFT_TYPE == "file":
                with open(GIFT_FILE_PATH, "rb") as f:
                    await self.bot.send_document(user_id, document=f, caption="🎁 Ваш подарок:")
            else:
                await self.bot.send_message(user_id, "❓ Неизвестный тип подарка.")

            self.sheets.mark_gift_sent(user_id, phone, platform="telegram")
            logging.info(f"✅ Telegram подарок отправлен {user_id}")
        except Exception:
            logging.exception(f"❌ Ошибка при отправке Telegram-подарка {user_id}")
