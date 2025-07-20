import os
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler
)
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Конфигурация
TOKEN = os.getenv(7572835912:AAEGPe3TIKPnQDVKq55uNwB8y7vW8MCEnjY)
ADMIN_CHAT_ID = os.getenv(497225787)  # Ваш chat_id
PORT = int(os.getenv('PORT', 5000))

# Состояния для ConversationHandler
NAME, REQUEST = range(2)

# Клавиатура
main_keyboard = [
    ["📝 Оставить заявку", "ℹ️ О боте"],
    ["📞 Контакты", "❌ Отмена"]
]

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"✨ Добро пожаловать, {user.first_name}!\n\n"
        "Я - ваш виртуальный помощник. Чем могу помочь?",
        reply_markup=ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)
    )

# Начало оформления заявки
async def start_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 Пожалуйста, введите ваше имя:",
        reply_markup=ReplyKeyboardRemove()
    )
    return NAME

# Получение имени
async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['name'] = update.message.text
    await update.message.reply_text("📝 Теперь введите вашу заявку:")
    return REQUEST

# Получение заявки и отправка админу
async def get_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    request_text = update.message.text
    user = update.effective_user
    
    # Форматированное сообщение для админа
    admin_message = (
        f"🚀 Новая заявка!\n\n"
        f"👤 Имя: {context.user_data['name']}\n"
        f"🆔 ID: {user.id}\n"
        f"📛 Username: @{user.username}\n\n"
        f"📝 Заявка:\n{request_text}"
    )
    
    # Отправка админу
    await context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=admin_message
    )
    
    # Подтверждение пользователю
    await update.message.reply_text(
        "✅ Ваша заявка отправлена! Скоро с вами свяжутся.",
        reply_markup=ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)
    )
    
    return ConversationHandler.END

# Отмена заявки
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "❌ Заявка отменена.",
        reply_markup=ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)
    )
    return ConversationHandler.END

# Информация о боте
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ℹ️ Этот бот создан для быстрой обработки ваших заявок.\n\n"
        "Просто нажмите «📝 Оставить заявку» и следуйте инструкциям."
    )

# Контакты
async def contacts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📞 Связь с администратором:\n"
        "@ваш_username\n"
        "✉️ email@example.com"
    )

# Ошибка
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")

def main():
    # Создаем Application
    app = Application.builder().token(TOKEN).build()

    # ConversationHandler для заявки
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^📝 Оставить заявку$"), start_request)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            REQUEST: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_request)]
        },
        fallbacks=[MessageHandler(filters.Regex("^❌ Отмена$"), cancel)],
    )

    # Регистрируем обработчики
    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)
    app.add_handler(MessageHandler(filters.Regex("^ℹ️ О боте$"), about))
    app.add_handler(MessageHandler(filters.Regex("^📞 Контакты$"), contacts))
    app.add_error_handler(error)

    # Запускаем бота
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=f"https://your-app-name.scalingo.io/{TOKEN}"
    )

if __name__ == "__main__":
    main()
