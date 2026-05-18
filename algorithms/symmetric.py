"""
Symmetric Encryption Algorithms
Caesar, Vigenere, Vernam, RC4
"""

def cesar_cipher(plaintext, key):
    """Caesar cipher encryption using full ASCII range (95 printable chars)"""
    ciphertext = []
    for char in plaintext:
        shifted = (ord(char) - 32 + key) % 95 + 32
        ciphertext.append(chr(shifted))
    return "".join(ciphertext)


def cesar_decipher(ciphertext, key):
    """Caesar cipher decryption"""
    return cesar_cipher(ciphertext, -key)


def vigenere_cipher(plaintext, key):
    """Vigenere cipher encryption using full ASCII range"""
    ciphertext = []
    for i in range(len(plaintext)):
        shifted = (ord(plaintext[i]) - 32 + ord(key[i % len(key)]) - 32) % 95 + 32
        ciphertext.append(chr(shifted))
    return "".join(ciphertext)


def vigenere_decipher(ciphertext, key):
    """Vigenere cipher decryption"""
    plaintext = []
    for i in range(len(ciphertext)):
        shifted = (ord(ciphertext[i]) - 32 - (ord(key[i % len(key)]) - 32)) % 95 + 32
        plaintext.append(chr(shifted))
    return "".join(plaintext)


def vernam_cipher(plaintext, key):
    """Vernam (One-Time Pad) cipher encryption using XOR"""
    ciphertext = []
    # Add padding if needed
    how_many = 0
    if len(plaintext) % len(key) != 0:
        how_many = len(key) - len(plaintext) % len(key)
    plaintext = plaintext + '0' * how_many

    for i in range(len(plaintext)):
        shifted = ((ord(plaintext[i]) - 32) ^ (ord(key[i % len(key)]) - 32)) + 32
        ciphertext.append(chr(shifted))
    return "".join(ciphertext)


def vernam_decipher(ciphertext, key):
    """Vernam cipher decryption (same as encryption for XOR)"""
    plaintext = []
    for i in range(len(ciphertext)):
        shifted = ((ord(ciphertext[i]) - 32) ^ (ord(key[i % len(key)]) - 32)) + 32
        plaintext.append(chr(shifted))
    return "".join(plaintext)


def rc4_cipher(message, key):
    """RC4 stream cipher encryption"""
    # KSA (Key Scheduling Algorithm)
    S = list(range(256))
    j = 0
    
    for i in range(256):
        j = (j + S[i] + ord(key[i % len(key)])) % 256
        S[i], S[j] = S[j], S[i]
    
    # PRGA (Pseudo-Random Generation Algorithm)
    i = j = 0
    result = []
    
    for char in message:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        
        k = (S[i] + S[j]) % 256
        result.append(chr(ord(char) ^ S[k]))
    
    return ''.join(result)


def rc4_decipher(ciphertext, key):
    """RC4 decryption (same as encryption)"""
    return rc4_cipher(ciphertext, key)
