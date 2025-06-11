from flask import Flask, send_from_directory, request, jsonify
import psycopg2
from datetime import datetime
import os
from urllib.parse import urlparse
from dotenv import load_dotenv

app = Flask(__name__, static_folder=".", static_url_path="")

load_dotenv()
DATABASE_URL = os.environ.get('DATABASE_URL')  # Fixed typo

def get_db_connection():
    try:
        if not DATABASE_URL:
            raise ValueError("DATABASE_URL not set")
            
        db_url = urlparse(DATABASE_URL)
        conn = psycopg2.connect(
            host=db_url.hostname,
            database=db_url.path[1:],
            user=db_url.username,
            password=db_url.password,
            port=db_url.port
        )
        return conn
    except Exception as e:
        print("Database connection error:", str(e))
        return None

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
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500
            
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
        return jsonify({"error": str(e)}), 500

@app.route("/api/transactions")
@app.route("/api/transactions")
def get_transactions():
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = conn.cursor()

        # Get query parameters
        offset = int(request.args.get("offset", 0))
        limit = int(request.args.get("limit", 20))
        category = request.args.get("category")

        if category:
            cursor.execute("""
                SELECT transaction_id, transaction_date, sms_body, amount, category
                FROM transactions
                WHERE category = %s
                ORDER BY transaction_date DESC
                LIMIT %s OFFSET %s
            """, (category, limit, offset))
        else:
            cursor.execute("""
                SELECT transaction_id, transaction_date, sms_body, amount, category
                FROM transactions
                ORDER BY transaction_date DESC
                LIMIT %s OFFSET %s
            """, (limit, offset))

        rows = cursor.fetchall()
        conn.close()

        return jsonify([
            {
                "id": row[0],
                "date": row[1].isoformat() if row[1] else None,
                "message": row[2],
                "amount": float(row[3]) if row[3] else 0,
                "category": row[4] or "Unknown"
            }
            for row in rows
        ])

    except Exception as e:
        print("Error fetching transactions:", str(e))
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)