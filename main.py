from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
from dotenv import load_dotenv

load_dotenv()  # Загружает переменные окружения из .env файла

TELEGRAM_API_KEY = os.getenv("TELEGRAM_API_KEY")

# Функция для создания PDF счета с позициями и реквизитами
def create_invoice(month, holder_name, mobile, items, output_file="invoice.pdf"):
    output_file= f"invoice_{holder_name}_{month}.pdf"
    c = canvas.Canvas(output_file, pagesize=A4)
    width, height = A4
    
    # Статичные данные
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, f"Invoice for {month}")  # Месяц счета
    
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, holder_name)
    c.drawString(50, height - 100, mobile)
    
    # Заголовки колонок
    c.drawString(50, height - 150, "Description")
    c.drawString(400, height - 150, "Price (AED)")
    
    # Переменные для расчёта и вывода позиций
    y_position = height - 170
    total_amount = 0
    
    # Отображение каждой позиции
    for item, price in items:
        c.drawString(50, y_position, item)
        price_str = f"AED {price:.2f}"
        # Вычисляем длину точки между названием и ценой
        points_length = width - 150 - 100  # Учитываем отступы (50 слева и 100 справа)
        dots = '.' * int(points_length / 5)  # Примерный расчет точек
        c.drawString(150, y_position, dots)  # Отрисовка точек
        c.drawString(400, y_position, price_str)  # Отрисовка цены
        total_amount += price
        y_position -= 20  # Перемещение вниз для следующей позиции
    
    # Итоговая сумма
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_position - 20, "TOTAL:")
    c.drawString(400, y_position - 20, f"AED {total_amount:.2f}")
    
    # Банковские реквизиты
    bank_details = [
        "Account Holder Name : Nika Dibrova",
        "Bank Name : Mashreq Bank",
        "Account Number : 019101523718",
        "IBAN : AE090330000019101523718"
    ]
    
    # Позиция для реквизитов, центрирование по горизонтали
    y_position -= 60  # Отступ вниз после TOTAL
    for line in bank_details:
        text_width = c.stringWidth(line, "Helvetica", 10)
        c.drawString((width - text_width) / 2, y_position, line)
        y_position -= 15  # Отступ вниз между строками
    
    # Сохранение PDF
    c.save()
    return output_file

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
