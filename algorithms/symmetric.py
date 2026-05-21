"""
Symmetric Encryption Algorithms (CLEAN VERSION)
Caesar, Vigenere, Vernam, RC4, CFB, DES-like Feistel
"""

import base64

# =========================================================
# CAESAR CIPHER (ASCII 95 chars)
# =========================================================

def cesar_cipher(text, key):
    return ''.join(chr((ord(c) - 32 + key) % 95 + 32) for c in text)

def cesar_decipher(text, key):
    return cesar_cipher(text, -key)


# =========================================================
# VIGENERE CIPHER (ASCII 95 chars)
# =========================================================

def vigenere_cipher(text, key):
    return ''.join(
        chr(((ord(t) - 32) + (ord(key[i % len(key)]) - 32)) % 95 + 32)
        for i, t in enumerate(text)
    )

def vigenere_decipher(text, key):
    return ''.join(
        chr(((ord(t) - 32) - (ord(key[i % len(key)]) - 32)) % 95 + 32)
        for i, t in enumerate(text)
    )


# =========================================================
# VERNAM (XOR STREAM - base64 output)
# =========================================================

def vernam_cipher(text, key):
    text_b = text.encode()
    key_b = key.encode()

    out = bytes([text_b[i] ^ key_b[i % len(key_b)] for i in range(len(text_b))])
    return base64.b64encode(out).decode()

def vernam_decipher(text, key):
    data = base64.b64decode(text)
    key_b = key.encode()

    out = bytes([data[i] ^ key_b[i % len(key_b)] for i in range(len(data))])
    return out.decode(errors="ignore")


# =========================================================
# RC4 (FIXED - ALWAYS BASE64 OUTPUT)
# =========================================================

def rc4_cipher(data, key):
    if isinstance(data, str):
        data = data.encode()
    if isinstance(key, str):
        key = key.encode()

    S = list(range(256))
    j = 0

    # KSA
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]

    i = j = 0
    out = bytearray()

    for byte in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]

        k = S[(S[i] + S[j]) % 256]
        out.append(byte ^ k)

    return base64.b64encode(bytes(out)).decode()


def rc4_decipher(data, key):
    data = base64.b64decode(data)

    if isinstance(key, str):
        key = key.encode()

    S = list(range(256))
    j = 0

    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]

    i = j = 0
    out = bytearray()

    for byte in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]

        k = S[(S[i] + S[j]) % 256]
        out.append(byte ^ k)

    return out.decode(errors="ignore")


# =========================================================
# CFB MODE (FIXED + CLEAN HEX OUTPUT)
# =========================================================

def cfb_encrypt(plaintext, key):
    if isinstance(plaintext, str):
        plaintext = plaintext.encode()
    if isinstance(key, str):
        key = key.encode()

    block_size = len(key)
    iv = key

    ciphertext = bytearray()

    for i in range(0, len(plaintext), block_size):
        block = plaintext[i:i+block_size]

        keystream = rc4_cipher(iv, key)
        keystream = base64.b64decode(keystream)[:len(block)]

        enc = bytes([b ^ k for b, k in zip(block, keystream)])

        ciphertext.extend(enc)
        iv = enc

    return bytes(ciphertext)


def cfb_decrypt(ciphertext, key):
    # ciphertext is already bytes, don't convert again
    if isinstance(ciphertext, str):
        ciphertext = bytes.fromhex(ciphertext)
    
    if isinstance(key, str):
        key = key.encode()

    block_size = len(key)
    iv = key

    plaintext = bytearray()

    for i in range(0, len(ciphertext), block_size):
        block = ciphertext[i:i+block_size]

        keystream = rc4_cipher(iv, key)
        keystream = base64.b64decode(keystream)[:len(block)]

        dec = bytes([b ^ k for b, k in zip(block, keystream)])

        plaintext.extend(dec)
        iv = block

    return plaintext.decode(errors="ignore")


# =========================================================
# SIMPLE FEISTEL DES (FIXED + STABLE + HEX OUTPUT)
# =========================================================

def key_to_bits(key):
    if isinstance(key, str):
        key = key.encode()
    return ''.join(format(b, '08b') for b in key)


def xor_bits(a, b):
    return ''.join('1' if x != y else '0' for x, y in zip(a, b))


def split_half(b):
    mid = len(b) // 2
    return b[:mid], b[mid:]


def sbox(bits):
    return bits  # simplified safe placeholder (no crashes)


def f(right, key):
    expanded = (right * 2)[:32]
    x = xor_bits(expanded, key)
    return sbox(x)


def des_round(l, r, key):
    return r, xor_bits(l, f(r, key))


def des_encrypt(text, key):
    if isinstance(text, str):
        text = text.encode()

    bits = ''.join(format(b, '08b') for b in text)

    while len(bits) % 64 != 0:
        bits += '0'

    key_bits = (key_to_bits(key) * 8)[:32]

    out = ""

    for i in range(0, len(bits), 64):
        block = bits[i:i+64]
        l, r = split_half(block)

        for _ in range(16):
            l, r = des_round(l, r, key_bits)

        out += l + r

    return hex(int(out, 2))[2:]


def des_decrypt(cipher_hex, key):
    bits = bin(int(cipher_hex, 16))[2:].zfill(len(cipher_hex) * 4)

    key_bits = (key_to_bits(key) * 8)[:32]

    out = ""

    for i in range(0, len(bits), 64):
        block = bits[i:i+64]
        l, r = split_half(block)

        for _ in range(16):
            r, l = des_round(r, l, key_bits)

        out += l + r

    return bytes(int(out[i:i+8], 2) for i in range(0, len(out), 8)).decode(errors="ignore").rstrip("\x00")

def bits_to_text(bits):
    """Convert binary string to text"""
    text_bytes = bytes(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))
    return text_bytes.decode(errors="ignore").rstrip("\x00")
