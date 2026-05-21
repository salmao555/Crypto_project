import hashlib

from rich import text

from algorithms.symmetric import (
    cesar_cipher,
    cesar_decipher,
    vigenere_cipher,
    vigenere_decipher,
    vernam_cipher,
    vernam_decipher,
    rc4_cipher,
    rc4_decipher
)

from Crypto.Cipher import AES, DES, ARC4, ChaCha20
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Util.Padding import pad, unpad



# =========================================================
# HELPERS (SAFE + CONSISTENT)
# =========================================================

def to_hex(data):
    if isinstance(data, bytes):
        return data.hex()
    if isinstance(data, str):
        return data.encode(errors="ignore").hex()
    return str(data)


def pad_8(text):
    if isinstance(text, str):
        text = text.encode()
    return text.ljust(8, b'\x00')[:8]


def pad_16(text):
    if isinstance(text, str):
        text = text.encode()
    return text.ljust(16, b'\x00')[:16]


def pad_32(text):
    """ChaCha20 requires 32-byte key"""
    if isinstance(text, str):
        text = text.encode()
    return text.ljust(32, b'\x00')[:32]


# =========================================================
# SYMMETRIC COMPARISON
# =========================================================

def compare_symmetric(text, key):
    print("\n═══ SYMMETRIC ALGORITHMS COMPARISON ═══\n")

    print("Your Implementations:\n")

    # Caesar
    c = cesar_cipher(text, 3)
    d = cesar_decipher(c, 3)
    print(f"Caesar   : {c}  | decrypt: {d}  | match: {d == text}")

    # Vigenere
    v = vigenere_cipher(text, key)
    vd = vigenere_decipher(v, key)
    print(f"Vigenere : {v}  | decrypt: {vd}  | match: {vd == text}")

    # Vernam
    ve = vernam_cipher(text, key)
    ved = vernam_decipher(ve, key)
    print(f"Vernam   : {ve}  | decrypt: {ved}  | match: {ved == text}")

    # RC4 (your implementation)
    r = rc4_cipher(text, key)
    rd = rc4_decipher(r, key)

    r_hex = r.hex() if isinstance(r, bytes) else str(r)
    print(f"RC4      : {r_hex}  | decrypt: {rd}  | match: {rd == text}")

    # ---------------- LIBRARY IMPLEMENTATIONS ----------------
    print("\nLibrary Implementations:\n")

    # AES (ECB demo)
    aes = AES.new(pad_16(key), AES.MODE_ECB)
    aes_enc = aes.encrypt(pad_16(text))
    aes_dec = aes.decrypt(aes_enc).rstrip(b"\x00").decode(errors="ignore")
    print(f"AES      : {aes_enc.hex()}  | decrypt: {aes_dec}  | match: {aes_dec == text}")

    # DES (ECB demo)

    des = DES.new(pad_8(key), DES.MODE_ECB)

    des_enc = des.encrypt(pad(text.encode(), 8))
    des_dec = unpad(des.decrypt(des_enc), 8).decode(errors="ignore")

    print(f"DES      : {des_enc.hex()}  | decrypt: {des_dec}  | match: {des_dec == text}")

    # RC4 library
    rc4_lib = ARC4.new(pad_16(key))
    rc4_enc = rc4_lib.encrypt(text.encode())
    rc4_lib2 = ARC4.new(pad_16(key))
    rc4_dec = rc4_lib2.decrypt(rc4_enc).decode(errors="ignore")

    print(f"RC4(lib) : {rc4_enc.hex()}  | decrypt: {rc4_dec}  | match: {rc4_dec == text}")

    # ChaCha20 (FIXED KEY LENGTH)
    cipher = ChaCha20.new(key=pad_32(key))
    nonce = cipher.nonce
    ch_enc = cipher.encrypt(text.encode())

    cipher2 = ChaCha20.new(key=pad_32(key), nonce=nonce)
    ch_dec = cipher2.decrypt(ch_enc).decode(errors="ignore")

    print(f"ChaCha20 : {ch_enc.hex()}  | decrypt: {ch_dec}  | match: {ch_dec == text}")


# =========================================================
# HASH COMPARISON
# =========================================================

def compare_hashes(text):
    print("\n═══ HASH FUNCTIONS COMPARISON ═══\n")

    print("Hashlib Implementations:")

    sha1 = hashlib.sha1(text.encode()).hexdigest()
    sha256 = hashlib.sha256(text.encode()).hexdigest()

    print(f"SHA1   : {sha1}")
    print(f"SHA256 : {sha256}")


# =========================================================
# ASYMMETRIC COMPARISON
# =========================================================

def compare_asymmetric(text):
    print("\n═══ ASYMMETRIC ALGORITHMS COMPARISON ═══\n")

    # RSA (FIXED PKCS1_OAEP USAGE)
    key = RSA.generate(2048)
    cipher = PKCS1_OAEP.new(key.publickey())
    cipher2 = PKCS1_OAEP.new(key)

    encrypted = cipher.encrypt(text.encode())
    decrypted = cipher2.decrypt(encrypted).decode()

    print(f"RSA Encrypted : {encrypted.hex()[:80]}...")
    print(f"RSA Decrypted : {decrypted}")

    # Diffie-Hellman (clean demo only)
    p = 23
    g = 5
    a = 6
    b = 15

    A = pow(g, a, p)
    B = pow(g, b, p)

    K1 = pow(B, a, p)
    K2 = pow(A, b, p)

    print("\nDiffie-Hellman (demo):")
    print(f"A = {A}, B = {B}")
    print(f"Shared Key = {K1} (match: {K1 == K2})")


# =========================================================
# MAIN ENTRY
# =========================================================

def run_comparison():
    print("\n════════════════════════════════════")
    print("      > ALGORITHM COMPARISON")
    print("════════════════════════════════════")

    text = input("\nEnter text to test: ")
    key = input("Enter key: ")

    compare_symmetric(text, key)
    compare_hashes(text)
    compare_asymmetric(text)

    input("\nPress Enter to continue...")

