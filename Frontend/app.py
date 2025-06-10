from flask import Flask, send_from_directory, request, jsonify
import psycopg2
from datetime import datetime
import os
from urllib.parse import urlparse

app = Flask(__name__, static_folder=".", static_url_path="")

DATABASE_URL = os.environ.get('postgresql://momo_db_user:A1hraJB9Wl4XLvcrBV2NIRxGGrSAMF0L@dpg-d143eo3uibrs73c2atfg-a/momo_db')

def get_db_connection():
    # Parse the database URL
    db_url = urlparse(DATABASE_URL)
    conn = psycopg2.connect(
        host=db_url.dpg-d143eo3uibrs73c2atfg-a,
        database=db_url.momo_db[1:],
        user=db_url.momo_db_user,
        password=db_url.A1hraJB9Wl4XLvcrBV2NIRxGGrSAMF0L,
        port=db_url.5432
    )
    return conn

@app.route("/")
def serve_index():
    return send_from_directory(".", "index.html")

@app.route("/<path:filename>")
def serve_static_files(filename):
    return send_from_directory(".", filename)

@app.route("/api/categories")
def get_categories():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT category AS name, 
                   SUM(amount) AS total_amount, 
                   COUNT(*) AS total_transactions
            FROM transactions
            GROUP BY category
        """)
        rows = cursor.fetchall()
        conn.close()

        return jsonify([
            {"name": row[0] or "Unknown", 
             "amount": float(row[1] or 0), 
             "transactions": row[2] or 0}
            for row in rows
        ])
    except Exception as e:
        print("Error fetching categories:", str(e))
        return jsonify([]), 500

@app.route("/api/transactions")
def get_transactions():
    category_filter = request.args.get("category")
    search_filter = request.args.get("search")
    date_from = request.args.get("dateFrom")
    date_to = request.args.get("dateTo")
    min_amount = request.args.get("minAmount")
    max_amount = request.args.get("maxAmount")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        sql = "SELECT * FROM transactions WHERE 1=1"
        params = []

        if category_filter:
            sql += " AND category = %s"
            params.append(category_filter)

        if search_filter:
            sql += " AND sms_body LIKE %s"
            params.append(f"%{search_filter}%")

        if date_from:
            try:
                date_from_obj = datetime.strptime(date_from, "%m/%d/%Y")
                date_from_str = date_from_obj.strftime("%Y-%m-%d")
                sql += " AND DATE(transaction_date) >= %s"
                params.append(date_from_str)
            except ValueError:
                print(f"Invalid date format for dateFrom: {date_from}")

        if date_to:
            try:
                date_to_obj = datetime.strptime(date_to, "%m/%d/%Y")
                date_to_str = date_to_obj.strftime("%Y-%m-%d")
                sql += " AND DATE(transaction_date) <= %s"
                params.append(date_to_str)
            except ValueError:
                print(f"Invalid date format for dateTo: {date_to}")

        if min_amount:
            sql += " AND amount >= %s"
            params.append(float(min_amount))

        if max_amount:
            sql += " AND amount <= %s"
            params.append(float(max_amount))

        cursor.execute(sql, params)
        # Get column names to create dictionary-like results
        colnames = [desc[0] for desc in cursor.description]
        rows = [dict(zip(colnames, row)) for row in cursor.fetchall()]
        conn.close()

        return jsonify(rows)
    except Exception as e:
        print("Error fetching transactions:", str(e))
        return jsonify([]), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)