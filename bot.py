import logging
import os
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    ContextTypes
)
from flask import Flask
from threading import Thread

# ===== Keep Alive Server =====
server = Flask(__name__)

@server.route('/')
def home():
    return "Бот работает! Мониторинг активен."

def run_server():
    server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

Thread(target=run_server).start()

# ===== Основной код бота =====
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.environ.get("TOKEN", "7572835912:AAEnLaTe1-L_Tvxr7XdwN6cwZWKnjhxItRg")
ADMIN_CHAT_ID = int(os.environ.get("ADMIN_CHAT_ID", 497225787))

NAME, PHONE, REQUEST = range(3)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Привет, {update.message.from_user.first_name}!\n"
        "Отправь /zayavka чтобы оставить заявку.",
        reply_markup=ReplyKeyboardRemove()
    )

# ... (остальные функции остаются без изменений) ...

def main():
    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('zayavka', zayavka)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
            REQUEST: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_request)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)
    app.add_error_handler(error_handler)

    print("🚀 Бот запущен на Railway!")
    app.run_polling()

if __name__ == '__main__':
    main()
