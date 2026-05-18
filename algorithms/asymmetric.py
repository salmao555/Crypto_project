"""
Asymmetric Encryption Algorithm - RSA
"""
import random


def est_premier(n):
    """Check if a number is prime"""
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


def pgcd(a, b):
    """Calculate Greatest Common Divisor using Euclidean algorithm"""
    while b != 0:
        r = a % b
        a = b
        b = r
    return a


def mod_inverse(a, m):
    """Calculate modular multiplicative inverse using Extended Euclidean Algorithm"""
    r0, r1 = a, m
    x0, x1 = 1, 0
    y0, y1 = 0, 1
    
    while r1 != 0:
        q = r0 // r1
        
        r0, r1 = r1, r0 - q * r1
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    
    if r0 != 1:
        return None
    
    return x0 % m


def generer_cles_rsa(p, q):
    """Generate RSA key pair from two prime numbers"""
    if not (est_premier(p) and est_premier(q)):
        raise ValueError("Both p and q must be prime numbers")
    
    n = p * q
    phi = (p - 1) * (q - 1)
    
    # Find e such that 1 < e < phi and gcd(e, phi) = 1
    e = 3
    while pgcd(e, phi) != 1:
        e += 2
    
    # Calculate d (modular inverse of e)
    d = mod_inverse(e, phi)
    
    return (e, n), (d, n)  # (public_key, private_key)


def generer_cles_rsa_securisees(bits=512):
    """Generate secure RSA keys with random primes"""
    def generate_prime(bits):
        """Generate a random prime number"""
        while True:
            num = random.randrange(2**(bits-1), 2**bits)
            if est_premier(num):
                return num
    
    p = generate_prime(bits // 2)
    q = generate_prime(bits // 2)
    
    return generer_cles_rsa(p, q)


def cryptage_rsa(message, e, n):
    """RSA encryption (for numeric message)"""
    return pow(message, e, n)


def decryptage_rsa(ciphertext, d, n):
    """RSA decryption"""
    return pow(ciphertext, d, n)


def cryptage_rsa_texte(texte, cle_publique):
    """RSA encryption for text (encrypts each character)"""
    e, n = cle_publique
    encrypted = []
    
    for char in texte:
        m = ord(char)
        if m >= n:
            raise ValueError(f"Character value {m} is too large for modulus {n}")
        c = cryptage_rsa(m, e, n)
        encrypted.append(c)
    
    return encrypted


def decryptage_rsa_texte(encrypted_list, cle_privee):
    """RSA decryption for text"""
    d, n = cle_privee
    decrypted = []
    
    for c in encrypted_list:
        m = decryptage_rsa(c, d, n)
        decrypted.append(chr(m))
    
    return "".join(decrypted)
