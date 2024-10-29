from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

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
        "Phone : +971509107077"
    ]
    
    # Позиция для реквизитов, центрирование по горизонтали
    y_position -= 100  # Отступ вниз после TOTAL
    for line in bank_details:
        text_width = c.stringWidth(line, "Helvetica", 10)
        c.drawString(50, y_position, line)
        y_position -= 15  # Отступ вниз между строками
    
    # Сохранение PDF
    c.save()
    return output_file
