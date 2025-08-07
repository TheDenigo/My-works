import asyncio
import sys
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.exceptions import VkApiError
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import VK_TOKEN, TELEGRAM_TOKEN, GROUP_ID, GIFT_TYPE
from handlers import get_handlers
import threading
import time
import logging
from database import Database
db = Database()


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(threadName)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

vk_bot_instance = None

class VKBot:
    def __init__(self):
        logger.info("Инициализация VKBot...")
        self.vk_session = vk_api.VkApi(token=VK_TOKEN)
        self.vk = self.vk_session.get_api()
        self._running = False
        logger.info("VKBot инициализирован.")

    def run(self):
        self._running = True
        logger.info("VK бот запускается...")
        longpoll = None

        try:
            longpoll = VkBotLongPoll(self.vk_session, GROUP_ID)
            logger.info("VK бот успешно запущен. Ожидание событий...")

            while self._running:
                try:
                    events = longpoll.check()
                    for event in events:
                        logger.debug(f"VK_Bot: Получено событие: {event.type}, данные: {event.object}")
                        self._handle_event(event)
                except VkApiError as e:
                    logger.error(f"VK_Bot: Ошибка API VK: {e}")
                    if self._running:
                        time.sleep(15)
                except Exception as e:
                    logger.error(f"VK_Bot: Ошибка в цикле событий VK: {e}", exc_info=True)
                    if self._running:
                        time.sleep(5)
            logger.info("VK_Bot: Цикл событий завершен (флаг _running стал False).")

        except Exception as e:
            logger.error(f"VK_Bot: Фатальная ошибка VK бота: {e}", exc_info=True)
        finally:
            logger.info("VK_Bot: VK бот остановлен.")

    def _handle_event(self, event):
        try:
            user_id = None
            action_type = None

            # Лайк
            if event.type == 'like_add':
                if event.object.get('object_type') == 'post':
                    user_id = event.object.get('liker_id')
                    post_id = event.object.get('object_id')
                    action_type = f"лайк на пост {post_id}"

            # Репост
            elif event.type == VkBotEventType.WALL_POST_NEW:
                if event.object.get('copy_history'):
                    user_id = event.object.get('from_id') or event.object.get('signer_id')
                    original = event.object['copy_history'][0]
                    action_type = f"репост поста {original.get('owner_id')}_{original.get('id')}"

            if user_id and action_type:
                logger.info(f"VK_Bot: {action_type} от пользователя {user_id}")
                db.log_vk_action(user_id, action_type)
                self._send_invite(user_id, action_type)
            else:
                logger.debug(f"VK_Bot: Необработанное событие: {event.type}")

        except Exception as e:
            logger.error(f"VK_Bot: Ошибка в обработке события: {e}", exc_info=True)

    def _send_invite(self, user_id, action_type):
        try:
            text = (
                f"Спасибо за {action_type}! 🎁\n"
                f"Получите подарок в Telegram → t.me/Denigo_test_bot"
            )
            self.vk.messages.send(
                user_id=user_id,
                message=text,
                random_id=int(time.time() * 1000) + user_id
            )
            logger.info(f"VK_Bot: Приглашение отправлено пользователю {user_id}")
        except Exception as e:
            logger.warning(f"VK_Bot: Не удалось отправить сообщение пользователю {user_id}: {e}")

    def stop(self):
        logger.info("VK_Bot: Получен сигнал на остановку VK бота...")
        self._running = False


class TelegramBot:
    def __init__(self):
        logger.info("Инициализация TelegramBot...")
        if GIFT_TYPE != "promo_code": 
            logger.warning(
                f"TelegramBot: GIFT_TYPE в config.py ('{GIFT_TYPE}') не равен 'promo_code'. "
                f"Промокод не будет основной наградой по текущей логике handlers.py, если она ожидает 'promo_code'."
            )

        self.application = Application.builder().token(TELEGRAM_TOKEN).build()
        self.application.add_handler(get_handlers())
        logger.info("TelegramBot инициализирован, обработчики добавлены.")


def run_vk_bot_threaded():
    global vk_bot_instance
    vk_bot_instance = VKBot() 
    logger.info("VK_Bot_Thread: Запуск потока для VK бота.")
    try:
        if vk_bot_instance:
            vk_bot_instance.run()
    except Exception as e:
        logger.error(f"VK_Bot_Thread: Исключение в потоке VK бота: {e}", exc_info=True)
    finally:
        logger.info("VK_Bot_Thread: Поток для VK бота завершен.")


async def main_async_entrypoint():
    logger.info("Async_Main: 🚀 Запуск системы...")

    vk_thread = threading.Thread(target=run_vk_bot_threaded, name="VKBotThread", daemon=True)
    tg_bot = TelegramBot()
    application = tg_bot.application

    vk_thread.start() 
    logger.info("Async_Main: Поток VK бота запущен.")

    try:
        logger.info("Async_Main: Telegram_Bot: Запуск polling...")
        await application.run_polling()
        logger.info("Async_Main: Telegram_Bot: Polling завершен (обычно при штатной остановке).")

    except (KeyboardInterrupt, asyncio.CancelledError) as e:
        logger.info(f"Async_Main: Telegram_Bot: Polling остановлен ({type(e).__name__}).")
    except Exception as e:
        logger.error(f"Async_Main: ❌ Ошибка в основном цикле Telegram бота: {e}", exc_info=True)
    finally:
        logger.info("Async_Main: Вход в блок finally основного цикла.")

        if application:
            logger.info("Async_Main: Попытка остановить приложение Telegram...")
            try:
                await application.shutdown()
                logger.info("Async_Main: Приложение Telegram успешно остановлено.")
            except RuntimeError as e_runtime:
                 logger.error(f"Async_Main: RuntimeError при остановке приложения Telegram: {e_runtime}", exc_info=False)
            except Exception as e_shutdown:
                logger.error(f"Async_Main: Ошибка при остановке приложения Telegram: {e_shutdown}", exc_info=True)

        global vk_bot_instance
        if vk_bot_instance:
            logger.info("Async_Main: Попытка остановить VK бота...")
            vk_bot_instance.stop()
        else:
            logger.warning("Async_Main: Экземпляр VK бота не был инициализирован. Невозможно остановить.")

        if vk_thread and vk_thread.is_alive():
            logger.info("Async_Main: Ожидание завершения потока VK бота (до 10 секунд)...")
            vk_thread.join(timeout=10)
            if vk_thread.is_alive():
                logger.warning("Async_Main: Поток VK бота не завершился в течение 10 секунд.")
            else:
                logger.info("Async_Main: Поток VK бота успешно завершен.")
        elif vk_thread:
             logger.info("Async_Main: Поток VK бота уже был завершен или не был запущен.")
        logger.info("Async_Main: ✅ Все процессы должны быть остановлены.")

import sys

if __name__ == "__main__":
    import sys
    import asyncio

    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    logger.info("MAIN_APP_ENTRY: Приложение запускается...")

    try:
        
        vk_thread = threading.Thread(target=run_vk_bot_threaded, name="VKBotThread", daemon=True)
        vk_thread.start()
        logger.info("MAIN_APP_ENTRY: Поток VK бота запущен.")

        tg_bot = TelegramBot()
        tg_bot.application.run_polling()  

    except KeyboardInterrupt:
        logger.info("MAIN_APP_ENTRY: 🛑 Остановлено вручную.")
    except Exception as e:
        logger.error(f"MAIN_APP_ENTRY: ❌ Ошибка на верхнем уровне: {e}", exc_info=True)