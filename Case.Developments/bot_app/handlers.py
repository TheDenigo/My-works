from telegram import Update
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    ContextTypes,
    ConversationHandler,
    filters,
)
from config import PROMO_CODE
from database import Database

db = Database()

ASK_NAME, ASK_EMAIL, ASK_PHONE = range(3)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    # Если пользователь уже в Google Sheets — подарок уже был выдан
    if db.check_user(user_id):
        await update.message.reply_text("❌ Вы уже получали подарок 🎁")
        return ConversationHandler.END

    context.user_data["user_id"] = user_id
    await update.message.reply_text("👋 Привет! Введите своё имя для получения подарка 😊")
    return ASK_NAME


async def ask_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["name"] = update.message.text.strip()
    await update.message.reply_text("📧 Теперь введите вашу почту")
    return ASK_EMAIL


async def ask_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["email"] = update.message.text.strip()
    await update.message.reply_text("📱 И, наконец, ваш номер телефона")
    return ASK_PHONE


async def save_and_finish(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["phone"] = update.message.text.strip()

    user_id = context.user_data["user_id"]
    name = context.user_data["name"]
    email = context.user_data["email"]
    phone = context.user_data["phone"]

    # 1) Добавляем нового пользователя в Google Sheets
    db.add_user(user_id, name, email, phone)
    # 2) Немедленно помечаем, что подарок выдан (5-й столбец → 'да')
    db.mark_gift_sent(user_id)

    # 3) Отправляем промокод
    await update.message.reply_text(
        f"✅ Спасибо, {name}! Вот ваш промокод: *{PROMO_CODE}*", parse_mode="Markdown"
    )
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("❌ Отмена. Введите /start, когда будете готовы снова.")
    return ConversationHandler.END


def get_handlers():
    return ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_email)],
            ASK_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_phone)],
            ASK_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_and_finish)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
