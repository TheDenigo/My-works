import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from config import VK_TOKEN, GROUP_ID, GIFT_TYPE, PROMO_CODE, GIFT_IMAGE_PATH, GIFT_FILE_PATH
from google_sheets import GoogleSheetsHelper
import time

def run_vk_bot(log_callback=print, stop_flag=None):
    vk_session = vk_api.VkApi(token=VK_TOKEN)
    longpoll = VkBotLongPoll(vk_session, GROUP_ID)
    vk = vk_session.get_api()
    sheets = GoogleSheetsHelper()

    log_callback("✅ VK-бот запущен.")

    sent_users = set()

    try:
        for event in longpoll.listen():
            if stop_flag and stop_flag.is_set():
                log_callback("🛑 VK-бот остановлен.")
                break

            if event.type == VkBotEventType.LIKE_ADD:
                user_id = event.object.from_id

                if user_id in sent_users or sheets.is_user_recorded(user_id):
                    continue

                user_info = vk.users.get(user_ids=user_id)[0]
                full_name = f"{user_info.get('first_name', '')} {user_info.get('last_name', '')}".strip()

                vk.messages.send(
                    user_id=user_id,
                    random_id=int(time.time()),
                    message="🎁 Спасибо за лайк! Вот ваш подарок!"
                )

                if GIFT_TYPE == "promo_code":
                    vk.messages.send(
                        user_id=user_id,
                        random_id=int(time.time()),
                        message=f"💬 Ваш промокод: {PROMO_CODE}"
                    )
                elif GIFT_TYPE == "image":
                    # TODO: загрузка фото
                    vk.messages.send(
                        user_id=user_id,
                        random_id=int(time.time()),
                        message="(Изображение отправлено отдельно)"
                    )
                elif GIFT_TYPE == "file":
                    # TODO: загрузка файла
                    vk.messages.send(
                        user_id=user_id,
                        random_id=int(time.time()),
                        message="(Файл отправлен отдельно)"
                    )

                sheets.record_user(user_id, full_name, "VK")
                sent_users.add(user_id)
                log_callback(f"📤 Сообщение отправлено пользователю VK: {full_name} ({user_id})")
    except Exception as e:
        log_callback(f"❌ Ошибка VK-бота: {e}")
