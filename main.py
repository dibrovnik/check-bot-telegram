from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

import os
from dotenv import load_dotenv
from create_invoice import create_invoice

load_dotenv()  # Загружает переменные окружения из .env файла

TELEGRAM_API_KEY = os.getenv("TELEGRAM_API_KEY")


# Команда start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Чтобы создать счет, отправьте данные в формате:\n\n"
        "Месяц, Имя держателя, Телефон, Позиция1:Цена1, Позиция2:Цена2, ...\n\n"
        "Пример: October 2024, John Doe, +1234567890, Yoga Classes:500, Pilates:300"
    )

# Обработка сообщений с данными
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    try:
        # Разделение текста на основную информацию и позиции
        parts = [item.strip() for item in text.split(',')]
        month = parts[0]
        holder_name = parts[1]
        mobile = parts[2]
        
        # Обработка позиций
        items = []
        for item in parts[3:]:
            description, price_str = item.split(':')
            price = float(price_str)
            items.append((description.strip(), price))
        
        # Создание PDF с данными
        pdf_path = create_invoice(month, holder_name, mobile, items)
        
        # Отправка PDF пользователю
        with open(pdf_path, 'rb') as pdf_file:
            await update.message.reply_document(pdf_file)
        
        # Удаление PDF после отправки
        os.remove(pdf_path)
        
    except Exception as e:
        await update.message.reply_text(f"Произошла ошибка. Проверьте данные и формат. Ошибка: {e}")

# Запуск бота
def main():
    # Вставьте свой API ключ от BotFather
    application = Application.builder().token(TELEGRAM_API_KEY).build()
    
    # Обработчики команд и сообщений
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Запуск
    application.run_polling()

if __name__ == "__main__":
    main()
