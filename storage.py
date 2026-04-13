"""
Persists and loads Bank data to/from a local JSON file.
"""

import json
import os
from bank import Bank, User

STORAGE_FILE = os.getenv("BANK_STORAGE_FILE", "bank_data.json")


def save_bank(bank: Bank) -> None:
    data = {
        "users": [
            {
                "username":       u.username,
                "password_hash":  u.password_hash,
                "display_name":   u.display_name,
                "email_verified": u.email_verified,
            }
            for u in bank.list_users()
        ]
    }
    with open(STORAGE_FILE, "w") as f:
        json.dump(data, f, indent=2)


def load_bank() -> Bank:
    if not os.path.exists(STORAGE_FILE):
        return Bank()
    with open(STORAGE_FILE) as f:
        data = json.load(f)
    bank = Bank()
    for u in data.get("users", []):
        user = bank.create_user(u["username"], u["password_hash"])
        user.display_name   = u.get("display_name", "")
        user.email_verified = u.get("email_verified", False)
    return bank
