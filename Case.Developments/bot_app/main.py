import asyncio
import sys
import threading
import time
import logging
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.exceptions import VkApiError
from telegram.ext import Application
from config import VK_TOKEN, TELEGRAM_TOKEN, GROUP_ID
from handlers import get_handlers
from database import Database

# Логирование
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(threadName)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("main")

# Глобальные переменные
db = Database()
vk_bot_instance = None
vk_thread = None
tg_bot = None
tg_thread = None
tg_loop = None


class VKBot:
    def __init__(self):
        logger.info("VKBot: инициализация…")
        self.vk_session = vk_api.VkApi(token=VK_TOKEN)
        self.vk = self.vk_session.get_api()
        self._running = False
        logger.info("VKBot: инициализирован.")

    def run(self):
        self._running = True
        logger.info("VKBot: Long Poll старт…")
        try:
            longpoll = VkBotLongPoll(self.vk_session, GROUP_ID)
        except Exception as e:
            logger.error(f"VKBot: LongPoll ошибка: {e}", exc_info=True)
            return

        while self._running:
            try:
                for event in longpoll.check():
                    self._handle_event(event)
            except Exception as e:
                logger.warning(f"VKBot: ошибка: {e}", exc_info=True)
                time.sleep(5)

        logger.info("VKBot: остановлен.")

    def _handle_event(self, event):
        try:
            user_id = None
            action = None

            if event.type == "like_add" and event.object.get("object_type") == "post":
                user_id = event.object.get("liker_id")
                post_id = event.object.get("object_id")
                action = f"лайк на пост {post_id}"

            elif event.type == VkBotEventType.WALL_POST_NEW:
                if event.object.get("copy_history"):
                    user_id = event.object.get("from_id") or event.object.get("signer_id")
                    original = event.object["copy_history"][0]
                    action = f"репост поста {original.get('owner_id')}_{original.get('id')}"

            if user_id and action:
                if db.was_user_invited(user_id):
                    logger.info(f"VKBot: пользователь {user_id} уже получал приглашение — пропускаем")
                    return
                db.log_vk_action(user_id, action)
                self._send_invite(user_id, action)
                db.mark_user_invited(user_id)
            else:
                logger.debug(f"VKBot: необработанное событие: {event.type}")
        except Exception as e:
            logger.error(f"VKBot: ошибка в обработке события: {e}", exc_info=True)

    def _send_invite(self, user_id, action_type):
        try:
            text = (
                f"Спасибо за {action_type}! 🎁\n"
                f"Получите подарок в Telegram → https://t.me/Ваш_Telegram_Бот"
            )
            self.vk.messages.send(
                user_id=user_id,
                message=text,
                random_id=int(time.time() * 1000) + user_id
            )
            logger.info(f"VKBot: сообщение отправлено {user_id}")
        except Exception as e:
            logger.warning(f"VKBot: ошибка отправки {user_id}: {e}")

    def stop(self):
        logger.info("VKBot: получен сигнал остановки")
        self._running = False


class TelegramBot:
    def __init__(self):
        logger.info("TelegramBot: инициализация…")
        self.app = Application.builder().token(TELEGRAM_TOKEN).build()
        self.app.add_handler(get_handlers())
        self.loop = None
        self.running = False

    def start(self):
        logger.info("TelegramBot: запускаем polling…")
        if sys.platform.startswith("win"):
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.running = True
        self.loop.run_until_complete(self.app.initialize())
        self.loop.run_until_complete(self.app.start())
        self.loop.run_until_complete(self.app.updater.start_polling())
        self.loop.run_forever()

    def stop(self):
        if not self.running:
            return
        logger.info("TelegramBot: получен сигнал остановки")
        if self.loop and self.loop.is_running():
            self.loop.call_soon_threadsafe(self._shutdown)

    def _shutdown(self):
        async def _close():
            await self.app.updater.stop()
            await self.app.stop()
            await self.app.shutdown()
            self.loop.stop()
            self.running = False
            logger.info("TelegramBot: остановлен")

        asyncio.create_task(_close())


def start_bot():
    global vk_bot_instance, vk_thread, tg_bot, tg_thread

    # VKBot
    vk_bot_instance = VKBot()
    vk_thread = threading.Thread(target=vk_bot_instance.run, name="VKBotThread", daemon=True)
    vk_thread.start()
    logger.info("MAIN_APP: VKBot запущен")

    # TelegramBot
    tg_bot = TelegramBot()
    tg_thread = threading.Thread(target=tg_bot.start, name="TelegramBotThread", daemon=True)
    tg_thread.start()
    logger.info("MAIN_APP: TelegramBot запущен")


def stop_bot():
    global tg_bot, vk_bot_instance
    logger.info("MAIN_APP: посылаем сигнал остановки обоим ботам…")

    if tg_bot:
        tg_bot.stop()
    if vk_bot_instance:
        vk_bot_instance.stop()

    logger.info("MAIN_APP: оба бота остановлены")
