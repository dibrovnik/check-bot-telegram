import logging
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Функция для создания PDF счета с позициями и реквизитами
def create_invoice(month, holder_name, mobile, items, output_file="invoice.pdf"):
    output_file = f"invoice_{holder_name}_{month}.pdf"
    logging.info("Создание счета для %s за %s", holder_name, month)
    c = canvas.Canvas(output_file, pagesize=A4)
    width, height = A4
    
    try:
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 50, f"Invoice for {month}")
        
        c.setFont("Helvetica", 12)
        c.drawString(50, height - 80, holder_name)
        c.drawString(50, height - 100, mobile)
        
        c.drawString(50, height - 150, "Description")
        c.drawString(400, height - 150, "Price (AED)")
        
        y_position = height - 170
        total_amount = 0
        
        for item, price in items:
            c.drawString(50, y_position, item)
            price_str = f"AED {price:.2f}"
            points_length = width - 150 - 100
            dots = '.' * int(points_length / 5)
            c.drawString(150, y_position, dots)
            c.drawString(400, y_position, price_str)
            total_amount += price
            y_position -= 20
        
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y_position - 20, "TOTAL:")
        c.drawString(400, y_position - 20, f"AED {total_amount:.2f}")
        
        bank_details = [
            "Account Holder Name : Nika Dibrova",
            "Bank Name : Mashreq Bank",
            "Account Number : 019101523718",
            "IBAN : AE090330000019101523718",
            "Phone : +971509107077"
        ]
        
        y_position -= 100
        for line in bank_details:
            c.drawString(50, y_position, line)
            y_position -= 15
        
        c.save()
        logging.info("Счет %s успешно создан", output_file)
        
    except Exception as e:
        logging.error("Ошибка при создании счета: %s", e)
        raise
    return output_file
