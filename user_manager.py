"""
User and Password Management System
FIXED: consistent bytes handling + stable encryption
"""

import json
import os
import base64
from datetime import datetime

from algorithms.hashing import SHA256
from algorithms.symmetric import rc4_cipher, rc4_decipher


# =========================================================
# USER MANAGER
# =========================================================

class UserManager:
    def __init__(self, data_file='data/users.json', master_key='CRYPTOVAULT_MASTER'):
        self.data_file = data_file
        self.master_key = master_key
        self.users = {}
        self.load_users()

    def load_users(self):
        if not os.path.exists(self.data_file):
            self.users = {}
            return

        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                encoded = f.read().strip()

            if not encoded:
                self.users = {}
                return

            encrypted_bytes = base64.b64decode(encoded)

            decrypted = rc4_decipher(encrypted_bytes, self.master_key)

            #  FIX: handle BOTH str and bytes safely
            if isinstance(decrypted, bytes):
                decrypted = decrypted.decode("utf-8")

            if not isinstance(decrypted, str):
                raise ValueError("Invalid decrypted data type")

            self.users = json.loads(decrypted)

        except Exception as e:
            print("Error loading users:", e)
            self.users = {}

    def save_users(self):
        json_data = json.dumps(self.users)

        encrypted = rc4_cipher(json_data, self.master_key)

        if isinstance(encrypted, str):
            encrypted = encrypted.encode("utf-8")

        encoded = base64.b64encode(encrypted).decode("utf-8")

        with open(self.data_file, "w", encoding="utf-8") as f:
            f.write(encoded)

    def create_user(self, username, password, email=''):
        if username in self.users:
            return False, "User already exists"

        self.users[username] = {
            "password_hash": SHA256(password),
            "email": email,
            "created_at": datetime.now().isoformat(),
            "last_login": None
        }

        self.save_users()
        return True, f"User '{username}' created successfully"

    def authenticate(self, username, password):
        if username not in self.users:
            return False

        if self.users[username]["password_hash"] == SHA256(password):
            self.users[username]["last_login"] = datetime.now().isoformat()
            self.save_users()
            return True

        return False


# =========================================================
# PASSWORD MANAGER
# =========================================================

class PasswordManager:
    def __init__(self, username, data_file='data/passwords.json', master_key='CRYPTOVAULT_PWD'):
        self.username = username
        self.data_file = data_file
        self.master_key = master_key
        self.passwords = {}
        self.load_passwords()

    def load_passwords(self):
        if not os.path.exists(self.data_file):
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            return

        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                encoded = f.read().strip()

            if not encoded:
                return

            encrypted_bytes = base64.b64decode(encoded)

            decrypted = rc4_decipher(encrypted_bytes, self.master_key)

            if isinstance(decrypted, bytes):
                decrypted = decrypted.decode("utf-8")

            all_data = json.loads(decrypted)

            self.passwords = all_data.get(self.username, {})

        except Exception as e:
            print(f"Error loading passwords: {e}")
            self.passwords = {}

    def load_passwords(self):
        if not os.path.exists(self.data_file):
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            self.passwords = {}
            return

        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                encoded = f.read().strip()

            if not encoded:
                self.passwords = {}
                return

            encrypted_bytes = base64.b64decode(encoded)

            decrypted = rc4_decipher(encrypted_bytes, self.master_key)

            if isinstance(decrypted, bytes):
                decrypted = decrypted.decode("utf-8")

            if not isinstance(decrypted, str):
                raise ValueError("Corrupted password data")

            all_data = json.loads(decrypted)

            self.passwords = all_data.get(self.username, {})

        except Exception as e:
            print(f"Error loading passwords: {e}")
            self.passwords = {}

    def create_password(self, service, password, notes=''):
        if service in self.passwords:
            return False, "Already exists"

        self.passwords[service] = {
            "password": password,
            "notes": notes,
            "created_at": datetime.now().isoformat(),
            "modified_at": None
        }

        self.save_passwords()
        return True, "Saved"