from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from db.models.models import User, Role, UserRole, Product, Stock, Invoice
from fpdf import FPDF
from fastapi.responses import FileResponse
import os


def generate_report(db: Session) -> FileResponse:
    font_dir = os.path.join(os.path.dirname(__file__), "..", "fonts")
    font_dir = os.path.abspath(font_dir)
    print(f"Font directory: {font_dir}")
    font_regular = os.path.join(font_dir, "DejaVuSans.ttf")
    font_bold = os.path.join(font_dir, "DejaVuSans-Bold.ttf")

    if not os.path.exists(font_regular) or not os.path.exists(font_bold):
        raise FileNotFoundError(f"Font file not found")

    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("DejaVu", fname=font_regular, uni=True)
    pdf.add_font("DejaVu", style="B", fname=font_bold, uni=True)

    def header(text, size=14):
        pdf.set_font("DejaVu", size=size, style="B")
        pdf.cell(0, 10, txt=text, ln=True, align="L")
        pdf.ln(2)

    def row(label, value):
        pdf.set_font("DejaVu", size=10)
        pdf.cell(60, 8, label, border=1)
        pdf.cell(40, 8, str(value), border=1, ln=True)

    # Title
    pdf.set_font("DejaVu", size=16, style="B")
    pdf.cell(0, 10, txt="Analytics Report", ln=True, align="C")
    pdf.ln(10)

    # 1. User Analytics
    header("1. User Analytics")
    total_users = db.query(User).count()
    admin_count = db.query(UserRole).join(
        Role).filter(Role.name == 'admin').count()
    customer_count = db.query(UserRole).join(
        Role).filter(Role.name == 'user').count()
    row("Total Users", total_users)
    row("Admins", admin_count)
    row("Customers", customer_count)
    pdf.ln(5)

    # 2. Product Analytics
    header("2. Product Analytics")
    total_products = db.query(Product).count()
    avg_price = db.query(func.avg(Product.price)).scalar() or 0
    total_stock = db.query(func.sum(Stock.quantity)).scalar() or 0
    avg_stock = db.query(func.avg(Stock.quantity)).scalar() or 0
    row("Total Products", total_products)
    row("Avg Price", f"${avg_price:.2f}")
    row("Total Stock", total_stock)
    row("Avg Stock/Product", f"{avg_stock:.1f}")
    pdf.ln(5)

    # High stock products
    header("Top 10 High Stock Products")
    pdf.cell(80, 8, "Product", border=1)
    pdf.cell(30, 8, "Quantity", border=1, ln=True)
    high_stock = db.query(Product.name, Stock.quantity).join(Stock)\
        .order_by(desc(Stock.quantity)).limit(10).all()
    for p in high_stock:
        pdf.cell(80, 8, p.name, border=1)
        pdf.cell(30, 8, str(p.quantity), border=1, ln=True)

    pdf.ln(5)

    # Low stock products
    header("Top 10 Low Stock Products")
    pdf.cell(80, 8, "Product", border=1)
    pdf.cell(30, 8, "Quantity", border=1, ln=True)
    low_stock = db.query(Product.name, Stock.quantity).join(Stock)\
        .filter(Stock.quantity > 0).order_by(Stock.quantity).limit(10).all()
    for p in low_stock:
        pdf.cell(80, 8, p.name, border=1)
        pdf.cell(30, 8, str(p.quantity), border=1, ln=True)

    pdf.ln(10)

    # 3. Sales Analytics
    header("3. Sales Analytics")
    total_invoices = db.query(Invoice).count()
    total_revenue = db.query(func.sum(Invoice.total_amount)).scalar() or 0
    avg_invoice = db.query(func.avg(Invoice.total_amount)).scalar() or 0
    row("Total Invoices", total_invoices)
    row("Total Revenue", f"${total_revenue:.2f}")
    row("Avg Invoice", f"${avg_invoice:.2f}")
    pdf.ln(5)

    # Top invoices
    header("Top 10 Invoices by Amount")
    pdf.cell(30, 8, "Invoice ID", border=1)
    pdf.cell(60, 8, "Customer", border=1)
    pdf.cell(40, 8, "Amount", border=1, ln=True)
    top_invoices = db.query(
        Invoice.id, User.first_name, User.last_name, Invoice.total_amount
    ).join(User).order_by(desc(Invoice.total_amount)).limit(10).all()

    for inv in top_invoices:
        pdf.cell(30, 8, str(inv.id), border=1)
        pdf.cell(60, 8, f"{inv.first_name} {inv.last_name}", border=1)
        pdf.cell(40, 8, f"${inv.total_amount:.2f}", border=1, ln=True)

    # Save file
    import tempfile

    file_path = os.path.join(tempfile.gettempdir(), "report.pdf")
    pdf.output(file_path, "F")
    return FileResponse(file_path, media_type="application/pdf", filename="report.pdf")
