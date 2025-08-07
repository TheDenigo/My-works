from telegram import Update
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    ContextTypes,
    ConversationHandler,
    filters
)
from database import Database

db = Database()

ASK_NAME, ASK_EMAIL, ASK_PHONE = range(3)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    if db.check_user(user_id):
        await update.message.reply_text("Вы уже получали подарок 🎁")
        return ConversationHandler.END
    else:
        context.user_data["user_id"] = user_id
        await update.message.reply_text("Привет! Чтобы получить подарок, напиши своё имя 😊")
        return ASK_NAME


async def ask_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["name"] = update.message.text
    await update.message.reply_text("Теперь напиши свою почту 📧")
    return ASK_EMAIL


async def ask_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["email"] = update.message.text
    await update.message.reply_text("И последний шаг — номер телефона 📱")
    return ASK_PHONE


async def save_and_finish(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["phone"] = update.message.text

    user_id = context.user_data["user_id"]
    name = context.user_data["name"]
    email = context.user_data["email"]
    phone = context.user_data["phone"]

    db.add_user(user_id, name, email, phone)

    await update.message.reply_text(f"Спасибо, {name}! 🎉 Вот ваш промокод: *PROMO123*", parse_mode="Markdown")
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Окей, отменено. Если передумаешь — просто напиши /start 🙂")
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
