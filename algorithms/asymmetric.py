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
    """RSA encryption for ANY text (safe byte-based)"""
    e, n = cle_publique

    data = texte.encode("utf-8")
    encrypted = []

    for byte in data:
        encrypted.append(pow(byte, e, n))

    return encrypted



def decryptage_rsa_texte(encrypted_list, cle_privee):
    """RSA decryption for text (byte-based)"""
    d, n = cle_privee

    decrypted_bytes = bytearray()

    for c in encrypted_list:
        decrypted_bytes.append(pow(c, d, n))

    return decrypted_bytes.decode("utf-8", errors="ignore")






# =========================================================
# EL-GAMAL ENCRYPTION (Classic - Discrete Logarithm)
# =========================================================

def generer_cles_elgamal(p, g):
    """
    Generate ElGamal key pair
    p: large prime number (modulus)
    g: generator (primitive root modulo p)
    
    Private key: x (random)
    Public key: y = g^x mod p
    
    Returns: (public_key, private_key)
    """
    import random
    
    # Private key: random x where 1 < x < p-1
    x = random.randint(2, p - 2)
    
    # Public key: y = g^x mod p
    y = pow(g, x, p)
    
    public_key = (p, g, y)  # (p, g, y)
    private_key = x          # just x
    
    return public_key, private_key


def cryptage_elgamal(message, public_key):
    """
    ElGamal encryption for numeric message
    
    Encryption:
    - c1 = g^r mod p
    - c2 = m × y^r mod p
    
    message: integer to encrypt (must be < p)
    public_key: (p, g, y)
    Returns: (c1, c2)
    """
    import random
    
    p, g, y = public_key
    
    # Random ephemeral key r
    r = random.randint(2, p - 2)
    
    # c1 = g^r mod p
    c1 = pow(g, r, p)
    
    # c2 = m × y^r mod p
    c2 = (message * pow(y, r, p)) % p
    
    return (c1, c2)


def decryptage_elgamal(ciphertext, private_key, p):
    """
    ElGamal decryption
    
    Decryption:
    - s = c1^x mod p
    - m = c2 × s^(-1) mod p
    
    ciphertext: (c1, c2)
    private_key: x
    p: modulus (from public key)
    Returns: decrypted message
    """
    c1, c2 = ciphertext
    x = private_key
    
    # s = c1^x mod p
    s = pow(c1, x, p)
    
    # s_inv = s^(-1) mod p (modular inverse)
    s_inv = mod_inverse(s, p)
    
    # m = c2 × s^(-1) mod p
    message = (c2 * s_inv) % p
    
    return message


def cryptage_elgamal_texte(texte, cle_publique):
    """
    ElGamal encryption for text (byte-based)
    texte: string to encrypt
    cle_publique: (p, g, y)
    Returns: list of encrypted tuples [(c1, c2), ...]
    """
    p, g, y = cle_publique
    
    data = texte.encode("utf-8")
    encrypted = []
    
    for byte in data:
        encrypted.append(cryptage_elgamal(byte, cle_publique))
    
    return encrypted


def decryptage_elgamal_texte(encrypted_list, cle_privee, p):
    """
    ElGamal decryption for text
    encrypted_list: list of (c1, c2) tuples
    cle_privee: x
    p: modulus
    Returns: decrypted string
    """
    decrypted_bytes = bytearray()
    
    for ciphertext in encrypted_list:
        decrypted_bytes.append(decryptage_elgamal(ciphertext, cle_privee, p))
    
    return decrypted_bytes.decode("utf-8", errors="ignore")


# =========================================================
# ELLIPTIC CURVE (EC) OPERATIONS
# =========================================================

class EllipticCurve:
    """Elliptic Curve y^2 = x^3 + ax + b (mod p)"""
    
    def __init__(self, a, b, p):
        self.a = a
        self.b = b
        self.p = p
    
    def is_on_curve(self, point):
        """Check if point is on the curve"""
        if point is None:  # Point at infinity
            return True
        
        x, y = point
        return (y * y - x * x * x - self.a * x - self.b) % self.p == 0
    
    def add(self, P, Q):
        """Add two points on the curve (ECC addition)"""
        if P is None:
            return Q
        if Q is None:
            return P
        
        x1, y1 = P
        x2, y2 = Q
        
        if x1 == x2:
            if y1 == y2:
                # Point doubling
                s = (3 * x1 * x1 + self.a) * mod_inverse(2 * y1, self.p) % self.p
            else:
                # Points are inverses
                return None
        else:
            # Point addition
            s = (y2 - y1) * mod_inverse(x2 - x1, self.p) % self.p
        
        x3 = (s * s - x1 - x2) % self.p
        y3 = (s * (x1 - x3) - y1) % self.p
        
        return (x3, y3)
    
    def multiply(self, k, P):
        """Scalar multiplication k*P (point addition k times)"""
        if k == 0 or P is None:
            return None
        
        result = None
        addend = P
        
        while k:
            if k & 1:
                result = self.add(result, addend)
            addend = self.add(addend, addend)
            k >>= 1
        
        return result
    
    def subtract(self, P, Q):
        """Subtract two points: P - Q"""
        if Q is None:
            return P
        
        x, y = Q
        # Negate Q: (x, -y mod p)
        neg_Q = (x, (-y) % self.p)
        return self.add(P, neg_Q)




# =========================================================
# DIFFIE-HELLMAN KEY EXCHANGE (EDUCATIONAL IMPLEMENTATION)
# =========================================================

def est_premier(n):
    """Simple primality test (enough for school project)."""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def diffie_hellman_generer_parametres(p, g):
    """
    Public parameters: p and g
    """
    if not est_premier(p):
        raise ValueError("p must be a prime number")
    return p, g


def diffie_hellman_generer_secret(p, g, secret=None):
    """
    Generate private secret and public value
    If secret is not given, generate random one
    """
    import random

    if secret is None:
        secret = random.randint(2, p - 2)

    public_value = pow(g, secret, p)

    return secret, public_value


def diffie_hellman_calculer_cle(public_recu, secret_prive, p):
    """
    Compute shared secret
    """
    return pow(public_recu, secret_prive, p)


def diffie_hellman_chiffrer(message, key):
    """
    XOR encryption using derived key
    """
    if isinstance(message, str):
        message = message.encode()

    key_byte = key % 256

    result = bytearray()

    for b in message:
        result.append(b ^ key_byte)

    return bytes(result)


def diffie_hellman_dechiffrer(ciphertext, key):
    """
    XOR decryption (same operation)
    """
    key_byte = key % 256

    result = bytearray()

    for b in ciphertext:
        result.append(b ^ key_byte)

    return result.decode(errors="ignore")