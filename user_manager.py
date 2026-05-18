"""
User and Password Management System
Stores data securely with encryption
"""
import json
import os
import base64
from datetime import datetime
from algorithms.hashing import SHA256
from algorithms.symmetric import rc4_cipher, rc4_decipher


class UserManager:
    """Manages users with encrypted storage"""
    
    def __init__(self, data_file='data/users.json', master_key='CRYPTOVAULT_MASTER'):
        self.data_file = data_file
        self.master_key = master_key
        self.users = {}
        self.load_users()
    
    def load_users(self):
        """Load users from encrypted file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    encrypted_base64 = f.read()
                    if encrypted_base64:
                        # Decode from base64
                        encrypted_data = base64.b64decode(encrypted_base64)
                        # Convert bytes to string for RC4
                        encrypted_str = encrypted_data.decode('latin-1')
                        decrypted = rc4_decipher(encrypted_str, self.master_key)
                        self.users = json.loads(decrypted)
            except Exception as e:
                print(f"Error loading users: {e}")
                self.users = {}
        else:
            # Create data directory if it doesn't exist
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
    
    def save_users(self):
        """Save users to encrypted file"""
        json_data = json.dumps(self.users, indent=2)
        encrypted = rc4_cipher(json_data, self.master_key)
        
        # Convert encrypted string to bytes then base64 for safe storage
        encrypted_bytes = encrypted.encode('latin-1')
        encrypted_base64 = base64.b64encode(encrypted_bytes).decode('utf-8')
        
        with open(self.data_file, 'w', encoding='utf-8') as f:
            f.write(encrypted_base64)
    
    def create_user(self, username, password, email=''):
        """Create a new user"""
        if username in self.users:
            return False, "User already exists"
        
        # Hash the password
        password_hash = SHA256(password)
        
        self.users[username] = {
            'password_hash': password_hash,
            'email': email,
            'created_at': datetime.now().isoformat(),
            'last_login': None
        }
        
        self.save_users()
        return True, f"User '{username}' created successfully"
    
    def authenticate(self, username, password):
        """Verify user credentials"""
        if username not in self.users:
            return False
        
        password_hash = SHA256(password)
        if self.users[username]['password_hash'] == password_hash:
            self.users[username]['last_login'] = datetime.now().isoformat()
            self.save_users()
            return True
        return False
    
    def modify_user(self, username, new_password=None, new_email=None):
        """Modify user information"""
        if username not in self.users:
            return False, "User not found"
        
        if new_password:
            self.users[username]['password_hash'] = SHA256(new_password)
        
        if new_email:
            self.users[username]['email'] = new_email
        
        self.save_users()
        return True, f"User '{username}' modified successfully"
    
    def delete_user(self, username):
        """Delete a user"""
        if username not in self.users:
            return False, "User not found"
        
        del self.users[username]
        self.save_users()
        return True, f"User '{username}' deleted successfully"
    
    def list_users(self):
        """Get list of all users"""
        return list(self.users.keys())
    
    def get_user_info(self, username):
        """Get user information (without password hash)"""
        if username not in self.users:
            return None
        
        user_data = self.users[username].copy()
        user_data.pop('password_hash', None)  # Don't expose hash
        return user_data


class PasswordManager:
    """Manages passwords with encryption"""
    
    def __init__(self, username, data_file='data/passwords.json', master_key='CRYPTOVAULT_PWD'):
        self.username = username
        self.data_file = data_file
        self.master_key = master_key
        self.passwords = {}
        self.load_passwords()
    
    def load_passwords(self):
        """Load passwords from encrypted file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    encrypted_base64 = f.read()
                    if encrypted_base64:
                        # Decode from base64
                        encrypted_data = base64.b64decode(encrypted_base64)
                        # Convert bytes to string for RC4
                        encrypted_str = encrypted_data.decode('latin-1')
                        decrypted = rc4_decipher(encrypted_str, self.master_key)
                        all_passwords = json.loads(decrypted)
                        self.passwords = all_passwords.get(self.username, {})
            except Exception as e:
                print(f"Error loading passwords: {e}")
                self.passwords = {}
        else:
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
    
    def save_passwords(self):
        """Save passwords to encrypted file"""
        # Load all users' passwords
        all_passwords = {}
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    encrypted_base64 = f.read()
                    if encrypted_base64:
                        # Decode from base64
                        encrypted_data = base64.b64decode(encrypted_base64)
                        # Convert bytes to string for RC4
                        encrypted_str = encrypted_data.decode('latin-1')
                        decrypted = rc4_decipher(encrypted_str, self.master_key)
                        all_passwords = json.loads(decrypted)
            except:
                pass
        
        # Update this user's passwords
        all_passwords[self.username] = self.passwords
        
        # Encrypt and save
        json_data = json.dumps(all_passwords, indent=2)
        encrypted = rc4_cipher(json_data, self.master_key)
        
        # Convert encrypted string to bytes then base64 for safe storage
        encrypted_bytes = encrypted.encode('latin-1')
        encrypted_base64 = base64.b64encode(encrypted_bytes).decode('utf-8')
        
        with open(self.data_file, 'w', encoding='utf-8') as f:
            f.write(encrypted_base64)
    
    def create_password(self, service, password, notes=''):
        """Store a password for a service"""
        if service in self.passwords:
            return False, f"Password for '{service}' already exists"
        
        self.passwords[service] = {
            'password': password,  # Will be encrypted when saved
            'notes': notes,
            'created_at': datetime.now().isoformat(),
            'modified_at': None
        }
        
        self.save_passwords()
        return True, f"Password for '{service}' created successfully"
    
    def modify_password(self, service, new_password=None, new_notes=None):
        """Modify a stored password"""
        if service not in self.passwords:
            return False, f"Password for '{service}' not found"
        
        if new_password:
            self.passwords[service]['password'] = new_password
        
        if new_notes is not None:
            self.passwords[service]['notes'] = new_notes
        
        self.passwords[service]['modified_at'] = datetime.now().isoformat()
        
        self.save_passwords()
        return True, f"Password for '{service}' modified successfully"
    
    def get_password(self, service):
        """Retrieve a password"""
        if service not in self.passwords:
            return None
        return self.passwords[service]
    
    def list_services(self):
        """Get list of all services"""
        return list(self.passwords.keys())
    
    def delete_password(self, service):
        """Delete a stored password"""
        if service not in self.passwords:
            return False, f"Password for '{service}' not found"
        
        del self.passwords[service]
        self.save_passwords()
        return True, f"Password for '{service}' deleted successfully"
    
    def get_password_strength(self, password):
        """Analyze password strength"""
        strength = {
            'length': len(password),
            'has_upper': any(c.isupper() for c in password),
            'has_lower': any(c.islower() for c in password),
            'has_digit': any(c.isdigit() for c in password),
            'has_special': any(not c.isalnum() for c in password)
        }
        
        score = 0
        if strength['length'] >= 8:
            score += 1
        if strength['length'] >= 12:
            score += 1
        if strength['has_upper']:
            score += 1
        if strength['has_lower']:
            score += 1
        if strength['has_digit']:
            score += 1
        if strength['has_special']:
            score += 1
        
        strength['score'] = score
        
        if score <= 2:
            strength['rating'] = 'Weak'
        elif score <= 4:
            strength['rating'] = 'Medium'
        else:
            strength['rating'] = 'Strong'
        
        return strength
