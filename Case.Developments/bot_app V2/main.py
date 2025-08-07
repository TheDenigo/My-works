
import threading
import time
import logging
import asyncio

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.exceptions import VkApiError

from telegram.ext import Application
from config import VK_TOKEN, TELEGRAM_TOKEN, GROUP_ID
from handlers import get_handlers
from database import Database

# --- Логирование ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(threadName)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

db = Database()

# События для остановки (глобально)
stop_event_vk = threading.Event()
stop_event_tg = threading.Event()


class VKBot:
    def __init__(self, stop_event: threading.Event):
        self.vk = vk_api.VkApi(token=VK_TOKEN).get_api()
        self.stop_event = stop_event
        logger.info("VKBot: инициализация…")
        logger.info("VKBot: инициализирован.")

    def run(self):
        logger.info("VKBot: Long Poll старт…")
        try:
            longpoll = VkBotLongPoll(vk_api.VkApi(token=VK_TOKEN), GROUP_ID)
        except Exception as e:
            logger.error(f"VKBot: не удалось подключиться: {e}")
            return

        try:
            for ev in longpoll.listen():
                if self.stop_event.is_set():
                    break
                self._handle(ev)
        except VkApiError as e:
            logger.error(f"VKBot: VkApiError: {e}")
        except Exception:
            logger.exception("VKBot: ошибка в цикле")

        logger.info("VKBot: остановлен.")

    def _handle(self, event):
        try:
            if event.type == "like_add" and event.object.get("object_type") == "post":
                uid = event.object["liker_id"]
                action = f"лайк на пост {event.object['object_id']}"
            elif event.type == VkBotEventType.WALL_POST_NEW and event.object.get("copy_history"):
                uid = event.object.get("from_id") or event.object.get("signer_id")
                orig = event.object["copy_history"][0]
                action = f"репост поста {orig['owner_id']}_{orig['id']}"
            else:
                return

            if db.was_user_invited(uid):
                logger.info(f"VKBot: {uid} уже приглашён")
                return

            logger.info(f"VKBot: событие {action} от {uid}")
            db.log_vk_action(uid, action)
            self.vk.messages.send(
                user_id=uid,
                message=(
                    f"Спасибо за {action}! 🎁\n"
                    f"Получите подарок в Telegram → t.me/Ваш_Bot"
                ),
                random_id=int(time.time() * 1000) + uid
            )
            db.mark_user_invited(uid)

        except Exception:
            logger.exception("VKBot: ошибка в _handle")

    def stop(self):
        logger.info("VKBot: получен сигнал остановки")
        self.stop_event.set()


class TelegramBotThread(threading.Thread):
    def __init__(self, stop_event: threading.Event):
        super().__init__(daemon=True)
        self.stop_event = stop_event
        self.app = Application.builder().token(TELEGRAM_TOKEN).build()
        self.app.add_handler(get_handlers())

    def run(self):
        # Настраиваем свой asyncio-loop для этого потока
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        logger.info("TelegramBot: запуск polling…")
        # Этот метод блокирует поток до вызова app.stop()
        self.app.run_polling()
        logger.info("TelegramBot: polling завершён")

    def stop(self):
        logger.info("TelegramBot: запланирована остановка")
        # Безопасно поставить задачу остановки в event loop
        self.loop.call_soon_threadsafe(lambda: asyncio.create_task(self.app.stop()))


# Глобальные объекты
vk_bot = None
vk_thread = None
tg_thread = None


def start_bot():
    global vk_bot, vk_thread, tg_thread
    stop_event_vk.clear()
    stop_event_tg.clear()

    vk_bot = VKBot(stop_event_vk)
    vk_thread = threading.Thread(target=vk_bot.run, name="VKBotThread", daemon=True)
    vk_thread.start()
    logger.info("MAIN_APP: VKBot запущен")

    tg_thread = TelegramBotThread(stop_event_tg)
    tg_thread.name = "TelegramBotThread"
    tg_thread.start()
    logger.info("MAIN_APP: TelegramBot запущен")


def stop_bot():
    logger.info("MAIN_APP: посылаем сигнал остановки обоим ботам…")
    if tg_thread:
        tg_thread.stop()
    if vk_bot:
        vk_bot.stop()
    logger.info("MAIN_APP: сигналы отправлены, потоки завершатся без блокировки GUI")


if __name__ == "__main__":
    start_bot()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stop_bot()