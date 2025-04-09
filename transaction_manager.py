import json
import os

TRANSACTIONS_PATH = "data/processed_transactions.json"

def load_transactions(last_id=0):  # Thêm tham số last_id với giá trị mặc định là 0
    try:
        with open(TRANSACTIONS_PATH, "r", encoding="utf-8") as file:
            transactions = json.load(file)
            return [t for t in transactions if t["id"] > last_id]  # Lọc và đảo ngược danh sách
    except FileNotFoundError:
        return []

def save_transactions(transactions):
    with open(TRANSACTIONS_PATH, "w", encoding="utf-8") as file:
        json.dump(transactions, file, indent=4, ensure_ascii=False)