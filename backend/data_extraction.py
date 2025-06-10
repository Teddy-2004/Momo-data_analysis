import xml.etree.ElementTree as ET
import pandas as pd
import re
import csv

file_path = "/workspaces/MoMo-Data-Analysis/backend/modified_sms_v2.xml"
csv_file_path = "/workspaces/MoMo-Data-Analysis/backend/extracted_transactions_final.csv"

tree = ET.parse(file_path)
root = tree.getroot()

data = []

for sms in root.findall('sms'):
    body = sms.get('body')
    date = sms.get('readable_date')

    transaction_id_match = re.search(r'TxId: (\d+)', body)
    transaction_id = transaction_id_match.group(1) if transaction_id_match else ""

    amount_match = re.search(r'(\d{1,3}(?:,\d{3})*|\d+) RWF', body)
    amount = amount_match.group(1) if amount_match else ""

    text_lower = body.lower()
    if "dear customer, your mtn momo application one-time password" in text_lower:
        category = "MTN SMS"
    elif "reversed" in text_lower or "reversal" in text_lower:
        category = "Reversed"
    elif "failed" in text_lower:
        category = "Failed"
    elif "you have received" in text_lower or "a bank deposit of" in text_lower:
        category = "Incoming Money"
    elif "your payment of" in text_lower:
        category = "Payments to Code Holders"
    elif "you have transferred" in text_lower:
        category = "Transfers to Mobile Numbers"
    elif "transferred to" in text_lower or ("transaction of" in text_lower and "by" in text_lower and "on your momo account" in text_lower):
        category = "Transfers to Mobile Numbers"
    elif "transaction of" in text_lower and "by" in text_lower:
        category = "Transactions Initiated by Third Parties"
    elif "bank deposit" in text_lower or "a bank deposit of" in text_lower:
        category = "Bank Deposits"
    elif "airtime" in text_lower:
        category = "Airtime Bill Payments"
    elif "cash power" in text_lower:
        category = "Cash Power Bill Payments"
    elif "you" in text_lower and "have via agent" in text_lower:
        category = "Withdrawals from Agents"
    elif "bank transfer" in text_lower:
        category = "Bank Transfers"
    elif "internet and voice bundle" in text_lower or "umaze kugura" in text_lower:
        category = "Internet and Voice Bundle Purchases"
    else:
        category = "Unknown"

    data.append([date, body, transaction_id, amount, category])

df = pd.DataFrame(data, columns=["Date", "Body", "TransactionID", "Amount", "Category"])
df.to_csv(csv_file_path, index=False, quoting=csv.QUOTE_ALL)
print(f"✅ CSV file saved at: {csv_file_path}")
