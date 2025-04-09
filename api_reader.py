import requests
import re
import base64
from datetime import date, timedelta
from transaction_manager import load_transactions, save_transactions
from config_manager import load_config, update_config

def fetch_and_save_transactions():
    config = load_config()
    last_id = config.get("last_id", 0)
    bank_number = config["bank_number"]
    token = config["token"]
    URL = config["api_url"]

    yesterday = date.today() - timedelta(days=1)
    yesterday_str = yesterday.strftime("%d/%m/%Y")

    payload = {
        "bankAccounts": f"{bank_number}",
        "begin": f"{yesterday_str}",
        "end": "31/3/2050"
    }

    encoded_text = base64.b64encode(token.encode()).decode()

    headers = {
        "pay2s-token": encoded_text,
        "Content-Type": "application/json"
    }

    response = requests.post(URL, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        transactions = data.get("transactions", [])
        existing_transactions = load_transactions()
        existing_ids = {t["id"] for t in existing_transactions}

        new_transactions = []
        for t in transactions:
            if t["type"] == "IN" and t["id"] not in existing_ids and t["id"] > last_id and "NAPTIEN " in t["description"]:
                content_match = re.search(r'NAPTIEN ([a-zA-Z0-9]+)', t["description"])
                content = content_match.group(1) if content_match else ""

                new_transactions.append({
                    "id": t["id"],
                    "content": content,
                    "datetime": t["transaction_date"],
                    "amount": t["amount"],
                    "status": "Chưa nạp tiền",
                })

        if transactions:
            max_new_id = max(t["id"] for t in transactions)
            if config["last_id"] == 0:
                update_config("last_id", max_new_id)

        if new_transactions:
            existing_transactions.extend(new_transactions)
            save_transactions(existing_transactions)