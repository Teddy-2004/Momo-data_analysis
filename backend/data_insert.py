import csv
import mysql.connector
from datetime import datetime

CSV_FILE_PATH = "MoMo-Data-Analysis/Backend/extracted_transactions_final.csv"

conn = mysql.connector.connect(
    host="localhost",
    user="momo_user",
    password="Momo@1234",
    database="momo_db"
)
cursor = conn.cursor()

with open(CSV_FILE_PATH, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f, quotechar='"')
    for row in reader:
        transaction_id = row["TransactionID"].strip() if row["TransactionID"].strip() else None
        transaction_date_str = row["Date"].strip()
        sms_body = row["Body"].strip() if row["Body"].strip() else None
        amount_str = row["Amount"].strip()
        category = row["Category"].strip() if row["Category"].strip() else None

        transaction_date = None
        if transaction_date_str:
            try:
                transaction_date = datetime.strptime(transaction_date_str, "%m/%d/%Y").strftime("%Y-%m-%d")
            except ValueError:
                print(f"Skipping row with invalid date format: {transaction_date_str}")
                continue

        amount = None
        if amount_str and amount_str.lower() != "unknown":
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
            """, (transaction_id, transaction_date, sms_body, amount, category))

        except mysql.connector.IntegrityError as e:
            print(f"Database error: {e}. Skipping this row...")

conn.commit()
cursor.close()
conn.close()
print("Data inserted successfully!")
