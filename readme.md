# 🚀 Auto Bot Modz – Inventory & POS Management System

Auto Bot Modz is a **production-ready Inventory and POS (Point of Sale) Management System** built for **automobile spare parts shops**.  
It is an **admin-only web application** that handles **stock, billing, customers, returns, GST invoices, and analytics** with a modern POS-style UI.

This project is designed around **real shop workflows**, not demos.

---

## ✨ Features

### 🔐 Authentication
- Secure admin login
- Password hashing
- Session-based authentication
- Protected routes

---

### 📦 Stock Management
- Add, edit, and soft-delete products
- Track:
  - Part name
  - Part number
  - Brand
  - Bike model
  - Purchase & selling price
  - Quantity & minimum stock level
- Prevents negative stock
- Automatic **low-stock alerts**
- Stock movement logs (sales, returns)

---

### 🧾 POS-Style Billing System
- Modern **POS-style billing UI**
- Fast product search and add-to-cart workflow
- Live stock availability checks
- Prevents overselling
- Auto bill number generation
- Live total and profit calculation
- Seamless customer auto-detection by mobile number

---

### 👤 Customer Management
- Auto-create customers during billing
- Search customers by name or mobile
- Edit customer details
- View customer purchase history
- View customer return history

---

### 🔁 Return Management
- Bill-specific returns only
- Prevents returning more than sold quantity
- Returned items are automatically added back to stock
- Profit and bill totals are recalculated accurately
- Full return audit trail

---

### 📊 Dashboard & Analytics
- Live dashboard with real-time data
- Total stock quantity
- Today’s sales and profit
- New customers today
- Today’s returns and monthly return summary
- Visual analytics using **Chart.js**

---

### 🧾 GST-Compliant Invoice System
- Professional invoice format with:
  - Shop name (**Auto Bot Modz**)
  - GST number
  - CGST & SGST calculation
  - Grand total
  - Product name & part number
- On-screen invoice view
- **Printable PDF invoices (A4)** using ReportLab
- Print-friendly invoice styling

---

### 🎨 Modern UI / UX
- Clean, trendy POS-inspired design
- Gradient KPI cards
- Subtle hover and focus animations
- Manual **Light / Dark mode toggle**
- Print-friendly layouts
- Responsive sidebar navigation
- Sidebar footer with branding and copyright

---

## 🛠️ Tech Stack

- **Backend:** Python 3.10+, Flask
- **Database:** SQLite + SQLAlchemy ORM
- **Frontend:** HTML5, CSS3, Bootstrap 5, Vanilla JavaScript
- **Charts:** Chart.js
- **PDF Generation:** ReportLab
- **Authentication:** Flask sessions + password hashing

---

## 📁 Project Structure

inventory_app/
│
├── app.py
├── config.py
├── database.db
├── requirements.txt
│
├── auth/
├── dashboard/
├── stock/
├── billing/
├── customers/
├── returns/
│
├── templates/
│ ├── base.html
│ ├── dashboard.html
│ ├── billing/
│ ├── stock/
│ ├── customers/
│ └── returns/
│
├── static/
│ ├── css/style.css
│ └── js/main.js
│
└── README.md

yaml
Copy code

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/auto-bot-modz.git
cd auto-bot-modz
2️⃣ Create Virtual Environment (Optional but Recommended)
bash
Copy code
python -m venv env
source env/bin/activate   # Windows: env\Scripts\activate
3️⃣ Install Dependencies
bash
Copy code
pip install -r requirements.txt
4️⃣ Run the Application
bash
Copy code
python app.py
🔑 Default Admin Login
makefile
Copy code
Username: admin
Password: admin123
⚠️ Change the password in production.

✅ Use Cases
Automobile spare parts shops

Bike & car accessory stores

Small retail POS systems

Internal inventory management tools

🧠 Project Highlights
Designed with real retail workflows

POS-style billing experience

GST-ready invoice generation

Clean Flask Blueprint architecture

No payment gateway (management-only system)

Easily extensible for barcode scanning, reports, or SaaS deployment

📌 Future Enhancements
Theme persistence (remember dark/light mode)

Barcode scanner support

GST reports & exports

CSV / Excel exports

Multi-admin roles

WhatsApp invoice sharing

🏁 License
This project is developed for educational and commercial use.
You are free to customize and extend it as per your needs.

🙌 Author
Developed with ❤️ for real-world retail usage.

Auto Bot Modz