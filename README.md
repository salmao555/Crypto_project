# 

**Professional Cryptography & Password Management System**

A comprehensive Python-based cryptography toolkit featuring user management, password storage, and implementations of classical and modern encryption algorithms.

---

##  Features

###  User Management
- **Create** new users with secure password hashing (SHA-256)
- **Modify** user credentials and information
- **Delete** users with confirmation
- **Authenticate** with encrypted session management
- **List** all registered users

###  Password Manager
- **Store** passwords securely (encrypted with RC4)
- **Retrieve** passwords when needed
- **Modify** existing password entries
- **Delete** password entries
- **Strength Analysis** - Real-time password strength checking
- **Encrypted Storage** - All data encrypted at rest

###  Cryptographic Algorithms

#### Symmetric Encryption
- **Caesar Cipher** - Classic substitution cipher with full ASCII support
- **Vigenere Cipher** - Polyalphabetic substitution cipher
- **Vernam Cipher** - One-Time Pad (OTP) using XOR encryption
- **RC4** - Stream cipher (used for data encryption)

#### Asymmetric Encryption
- **RSA** - Public-key cryptography with key generation
  - Custom prime number generation
  - Modular arithmetic implementation
  - Text encryption support

#### Hash Functions
- **SHA-1** - 160-bit hash (educational purposes)
- **SHA-256** - 256-bit secure hash
  - Custom implementation from scratch
  - Matches official `hashlib` output


---

## Installation

### Requirements
- Python 3.7+
- `rich` library (for beautiful CLI)

### Setup

1. **Install dependencies:**
```bash
pip install rich
```

2. **Run the application:**
```bash
python main.py
```

Or make it executable:
```bash
chmod +x main.py
./main.py
```

---

## 📖 Usage

### Starting the Application

Run the main script:
```bash
python main.py
```

You'll see the beautiful CryptoVault Pro banner:

```
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║           CRYPTOVAULT PRO                            ║
║                                                           ║
║     Professional Cryptography & Password Manager         ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

### First Time Setup

1. **Register** a new account
2. **Login** with your credentials
3. Explore the features!

### Main Menu Options

1. **Manage Users** - Create, view, modify, or delete users
2. **Manage Passwords** - Store and retrieve passwords securely
3. **Encrypt/Decrypt** - Use various encryption algorithms
4. **Test Algorithms** - Test symmetric and asymmetric encryption
5. **Hash Passwords** - Generate SHA-1 and SHA-256 hashes
6. **Algorithm Comparison** - Compare all algorithms side-by-side

---

## Technical Details

### Project Structure

```
cryptovault/
├── algorithms/
│   ├── __init__.py
│   ├── symmetric.py      # Caesar, Vigenere, Vernam, RC4
│   ├── asymmetric.py     # RSA implementation
│   └── hashing.py        # SHA-1, SHA-256
├── data/
│   ├── users.json        # Encrypted user database
│   └── passwords.json    # Encrypted password vault
├── user_manager.py       # User and password management
└── main.py              # Main CLI application

theres also file management and comparaison.py 
```

### Encryption Details

#### User Storage
- **Passwords**: Hashed using SHA-256 (never stored in plaintext)
- **Database**: Encrypted using RC4 with master key
- **Format**: JSON (encrypted)

#### Password Vault
- **Encryption**: RC4 stream cipher
- **Storage**: Per-user encrypted JSON
- **Retrieval**: Decrypted on-the-fly when accessed

### Algorithm Implementations

All algorithms are implemented **from scratch** without using external cryptography libraries (except for comparison purposes):

- **Symmetric Ciphers**: Full ASCII character support (95 printable chars)
- **RSA**: Complete implementation including key generation
- **SHA**: Byte-level manipulation with proper padding and compression

---

##  Educational Value

This project demonstrates:

1. **Classical Cryptography** - Caesar, Vigenere, Vernam
2. **Modern Stream Ciphers** - RC4
3. **Public Key Cryptography** - RSA
4. **Hash Functions** - SHA-1, SHA-256
5. **Secure Storage** - Encrypted databases
6. **User Authentication** - Password hashing
7. **Software Architecture** - Modular design, separation of concerns

---


---





