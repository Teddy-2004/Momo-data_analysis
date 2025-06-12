# 📊 MoMo Data Analysis Dashboard

A web-based dashboard to visualize and analyze mobile money (MoMo) transaction data using a PostgreSQL database, Flask backend, and vanilla HTML/CSS/JS frontend.

## 🚀 Features

- Interactive visualization of total amounts by category (bar chart + table)
- Filter transactions by:
  - Category
  - Date range
  - Amount range
  - Search term (e.g. reference in SMS body)
- Mobile-friendly UI
- Backend API with filterable endpoints
- Deployable via Render or run locally

---

## 🧱 Project Structure

MoMo-Data-Analysis/
├── Backend/
│ ├── app.py # Flask backend
│ ├── extracted_transactions_final.csv
│ ├── populate_db.py # (Optional) script to load CSV into DB
│ ├── requirements.txt
├── static/
│ ├── index.html # Main dashboard UI
│ ├── style.css
│ ├── script.js
├── .env # Contains DATABASE_URL
├── README.md

yaml
Copy code

---

## 🖥️ Running Locally

### ✅ Prerequisites

- Python 3.8+
- PostgreSQL installed & running
- Node.js (optional, only if using frontend tooling or chart dependencies)
- Git

---

### 📦 Step 1: Clone the Repo

```bash
git clone https://github.com/yourusername/momo-data-analysis.git
cd momo-data-analysis
🛠️ Step 2: Setup Python Environment
bash
Copy code
cd Backend
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt

🗄️ Step 3: Set Up PostgreSQL Database
Create database and user:

sql
Copy code
CREATE DATABASE momo_db;
CREATE USER momo_user WITH PASSWORD 'Momo@1234';
GRANT ALL PRIVILEGES ON DATABASE momo_db TO momo_user;
Create the transactions table:

sql
Copy code
CREATE TABLE transactions (
    transaction_id TEXT,
    transaction_date DATE,
    sms_body TEXT,
    amount FLOAT,
    category TEXT
);
Populate the table (optional):

bash
Copy code
python populate_db.py
🧪 Step 4: Create .env file
In the project root (MoMo-Data-Analysis/), create a .env file:

perl
Copy code
DATABASE_URL=postgresql://momo_user:Momo@1234@localhost:5432/momo_db
▶️ Step 5: Run the Flask Server
bash
Copy code
python app.py
Visit: http://localhost:5000

🌍 Deployment (Render)
1. Push your project to GitHub
bash
Copy code
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/momo-data-analysis.git
git push -u origin main
2. Create a PostgreSQL DB on Render
Go to https://dashboard.render.com/

Click New + → PostgreSQL

After creation, copy the Internal Database URL, e.g.:

bash
Copy code
postgres://user:pass@host:port/dbname
3. Deploy Flask App
Click New + → Web Service

Connect your GitHub repo

Build command: pip install -r requirements.txt

Start command: python app.py

Add environment variable:

ini
Copy code
DATABASE_URL=your_render_database_url
🛠 Tech Stack
Backend: Python, Flask, psycopg2, PostgreSQL

Frontend: HTML, CSS, JavaScript (Vanilla)

Visualization: Chart.js

Deployment: Render

📂 API Endpoints
/api/categories
Returns summary of transactions grouped by category.

/api/transactions
Supports query parameters:

category

dateFrom, dateTo

minAmount, maxAmount

search

🤝 Contributions
Contributions are welcome! Feel free to open issues or PRs to improve functionality or design.

📄 License
MIT License — free to use, modify, and distribute.

Tedla Tesfaye Godebo 2025
