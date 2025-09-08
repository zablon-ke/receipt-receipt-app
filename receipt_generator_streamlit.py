import streamlit as st
from reportlab.lib.pagesizes import portrait
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

# Function to format KES amounts
def format_amount(value):
    try:
        amount = float(value)
        return f"KES {amount:.2f}" if amount >= 50 else f"KES {int(amount)}"
    except ValueError:
        return value

# Function to generate PDF receipt
def generate_receipt_pdf(data, output_file="receipt.pdf"):
    receipt_width = 80 * mm
    receipt_height = 150 * mm
    c = canvas.Canvas(output_file, pagesize=portrait((receipt_width, receipt_height)))

    font_size = 10
    c.setFont("Courier", font_size)
    line_height = font_size + 2
    y = receipt_height - 20

    # Top left lines
    c.drawString(5 * mm, y, "kaps@kaps.co.ke")
    y -= line_height
    c.drawString(5 * mm, y, "Tel: +254732146000")
    y -= line_height

    # KAPS LTD centered
    y -= line_height
    c.drawCentredString(receipt_width / 2, y, "KAPS LTD")
    y -= line_height * 2

    # Header lines indented
    indent_x = 10 * mm
    for text in ["PIN: P051171982Y", "VAT No. 0150223D", "Payment for Parking Fee"]:
        c.drawString(indent_x, y, text)
        y -= line_height
    y -= 5

    # Top dashed line
    c.drawString(5 * mm, y, "="*30)
    y -= line_height + 2

    # Receipt details
    details_keys = ["Ticket No.", "Receipt No.", "Entry Time", "Pay Time", "Duration",
                    "Sub Total", "Tax Amount", "Total Due", "Tendered", "Change",
                    "Pay Mode", "Pay Point", "Parked at"]
    
    label_x = 5 * mm
    value_x = 32 * mm

    for key in details_keys:
        val = format_amount(data[key]) if key in ["Sub Total","Tax Amount","Total Due","Tendered","Change"] else data[key]
        c.drawString(label_x, y, key)
        c.drawString(value_x, y, val)
        y -= line_height
    y -= line_height * 1.2

    # VAT and footer
    y -= 5
    c.drawString(5 * mm, y, "Amount Inclusive of 16% VAT")
    y -= (line_height + 5)
    c.drawString(5 * mm, y, "="*30)
    y -= line_height

    for text in ["You have 15 Mins to Exit", "Use your ticket to Exit"]:
        c.drawString(indent_x, y, text)
        y -= line_height
    y -= 2

    # CU placeholders
    c.drawString(5 * mm, y, "="*30)
    y -= line_height
    c.drawString(5 * mm, y, "CU IN No: {{cu_serial_no}}")
    y -= line_height
    c.drawString(5 * mm, y, "CU SN No: {{cu_invoice_no}}")
    y -= 2
    c.drawString(5 * mm, y, "="*30)

    c.save()
    return output_file

# Streamlit app
st.title("Parking Receipt Generator")

# Collect user inputs
ticket_data = {}
fields = ["Ticket No.", "Receipt No.", "Entry Time", "Pay Time", "Duration",
          "Sub Total", "Tax Amount", "Total Due", "Tendered", "Change",
          "Pay Mode", "Pay Point", "Parked at"]

for field in fields:
    ticket_data[field] = st.text_input(field)

if st.button("Generate Receipt"):
    pdf_file = generate_receipt_pdf(ticket_data)
    st.success(f"Receipt generated: {pdf_file}")
    with open(pdf_file, "rb") as f:
        st.download_button("Download PDF", f, file_name=pdf_file, mime="application/pdf")
