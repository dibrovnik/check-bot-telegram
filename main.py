import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
from dotenv import load_dotenv
from create_invoice import create_invoice

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot.log"),  # Лог-файл
        logging.StreamHandler()  # Вывод в консоль
    ]
)

load_dotenv()  # Загружает переменные окружения из .env файла
TELEGRAM_API_KEY = os.getenv("TELEGRAM_API_KEY")

# Команда start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("Команда /start вызвана пользователем %s", update.message.from_user.username)
    await update.message.reply_text(
        "Привет! Чтобы создать счет, отправьте данные в формате:\n\n"
        "Месяц, Имя держателя, Телефон, Позиция1:Цена1, Позиция2:Цена2, ...\n\n"
        "Пример: October 2024, John Doe, +1234567890, Yoga Classes:500, Pilates:300"
    )

# Обработка сообщений с данными
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    logging.info("Получено сообщение от %s: %s", update.message.from_user.username, text)
    
    try:
        parts = [item.strip() for item in text.split(',')]
        month = parts[0]
        holder_name = parts[1]
        mobile = parts[2]
        
        items = []
        for item in parts[3:]:
            description, price_str = item.split(':')
            price = float(price_str)
            items.append((description.strip(), price))
        
        pdf_path = create_invoice(month, holder_name, mobile, items)
        logging.info("Счет успешно создан для %s на %s", holder_name, pdf_path)
        
        with open(pdf_path, 'rb') as pdf_file:
            await update.message.reply_document(pdf_file)
        logging.info("Счет отправлен пользователю %s", update.message.from_user.username)
        
        os.remove(pdf_path)
        logging.info("Файл счета %s удален", pdf_path)
        
    except Exception as e:
        logging.error("Ошибка при обработке сообщения от %s: %s", update.message.from_user.username, e)
        await update.message.reply_text(f"Произошла ошибка. Проверьте данные и формат. Ошибка: {e}")

# Запуск бота
def main():
    logging.info("Запуск бота...")
    application = Application.builder().token(TELEGRAM_API_KEY).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    application.run_polling()
    logging.info("Бот завершил работу")

if __name__ == "__main__":
    main()
