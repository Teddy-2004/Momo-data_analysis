import csv
import psycopg2
import os
from datetime import datetime
from dotenv import load_dotenv

# Load your Render DATABASE_URL from .env
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

CSV_FILE_PATH = "/home/teddy/Momo-data_analysis/backend/extracted_transactions_final.csv"

# Connect to PostgreSQL on Render
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

with open(CSV_FILE_PATH, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        transaction_id = row["TransactionID"].strip() or None
        transaction_date_str = row["Date"].strip()
        sms_body = row["Body"].strip() or None
        amount_str = row["Amount"].strip()
        category = row["Category"].strip() or None

        # Parse date
        transaction_date = None
        if transaction_date_str:
            try:
                transaction_date = datetime.strptime(transaction_date_str, "%m/%d/%Y").date()
            except ValueError:
                print(f"Skipping row with invalid date: {transaction_date_str}")
                continue

        # Parse amount
        amount = None
        if amount_str.lower() != "unknown":
            try:
                amount = float(amount_str.replace(",", ""))
            except ValueError:
                amount = None

        try:
            cursor.execute("""
                INSERT INTO transactions (
                    transaction_id,
                    transaction_date,
                    sms_body,
                    amount,
                    category
                )
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (transaction_id) DO NOTHING
            """, (transaction_id, transaction_date, sms_body, amount, category))
        except Exception as e:
            print(f"Error inserting row: {e}")

conn.commit()
cursor.close()
conn.close()
print("✅ Data inserted successfully!")
