"""
Hash Algorithms - SHA-1 and SHA-256
"""


def padding(message):
    """Add padding to message for SHA (512-bit blocks)"""
    msg = message.encode() + b'\x80'
    
    while len(msg) * 8 % 512 != 448:
        msg += b'\x00'
    
    L = len(message.encode()) * 8
    msg += L.to_bytes(8, byteorder='big')
    
    return msg


def split_blocks(msg):
    """Split padded message into 512-bit (64-byte) blocks"""
    blocks = []
    for i in range(0, len(msg), 64):
        blocks.append(msg[i:i+64])
    return blocks


def left_rotate(x, n):
    """Left rotate a 32-bit integer"""
    return (x << n | x >> (32 - n)) & 0xFFFFFFFF


def right_rotate(x, n):
    """Right rotate a 32-bit integer"""
    return (x >> n | x << (32 - n)) & 0xFFFFFFFF


# ==================== SHA-1 ====================

def generate_W(block):
    """Generate message schedule W for SHA-1 (80 words)"""
    W = []
    
    # First 16 words directly from block
    for i in range(0, len(block), 4):
        word = int.from_bytes(block[i:i+4], byteorder='big')
        W.append(word)
    
    # Generate remaining 64 words
    for i in range(16, 80):
        word = left_rotate(W[i-3] ^ W[i-8] ^ W[i-14] ^ W[i-16], 1)
        W.append(word)
    
    return W


def compression_sha1(block, H):
    """SHA-1 compression function"""
    W = generate_W(block)
    
    A, B, C, D, E = H[0], H[1], H[2], H[3], H[4]
    
    # Round constants
    K = [0x5A827999, 0x6ED9EBA1, 0x8F1BBCDC, 0xCA62C1D6]
    
    # 80 rounds
    for i in range(80):
        if 0 <= i < 20:
            f = (B & C) | (~B & D)
            k = K[0]
        elif 20 <= i < 40:
            f = B ^ C ^ D
            k = K[1]
        elif 40 <= i < 60:
            f = (B & C) | (B & D) | (C & D)
            k = K[2]
        else:
            f = B ^ C ^ D
            k = K[3]
        
        temp = (left_rotate(A, 5) + f + E + k + W[i]) & 0xFFFFFFFF
        E = D
        D = C
        C = left_rotate(B, 30)
        B = A
        A = temp
    
    # Add to hash state
    H[0] = (H[0] + A) & 0xFFFFFFFF
    H[1] = (H[1] + B) & 0xFFFFFFFF
    H[2] = (H[2] + C) & 0xFFFFFFFF
    H[3] = (H[3] + D) & 0xFFFFFFFF
    H[4] = (H[4] + E) & 0xFFFFFFFF
    
    return H


def SHA1(message):
    """Complete SHA-1 hash function"""
    # Initial hash values
    H = [
        0x67452301,
        0xEFCDAB89,
        0x98BADCFE,
        0x10325476,
        0xC3D2E1F0
    ]
    
    # Process message
    padded = padding(message)
    blocks = split_blocks(padded)
    
    for block in blocks:
        H = compression_sha1(block, H)
    
    # Convert to hex string
    return ''.join(f'{h:08x}' for h in H)


# ==================== SHA-256 ====================

# SHA-256 round constants (first 32 bits of fractional parts of cube roots of first 64 primes)
K_256 = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
]


def generate_W256(block):
    """Generate message schedule W for SHA-256 (64 words)"""
    W = []
    
    # First 16 words from block
    for i in range(0, len(block), 4):
        word = int.from_bytes(block[i:i+4], byteorder='big')
        W.append(word)
    
    # Generate remaining 48 words
    for i in range(16, 64):
        s0 = right_rotate(W[i-15], 7) ^ right_rotate(W[i-15], 18) ^ (W[i-15] >> 3)
        s1 = right_rotate(W[i-2], 17) ^ right_rotate(W[i-2], 19) ^ (W[i-2] >> 10)
        W.append((W[i-16] + s0 + W[i-7] + s1) & 0xFFFFFFFF)
    
    return W


def compression_sha256(block, H):
    """SHA-256 compression function"""
    W = generate_W256(block)
    
    a, b, c, d, e, f, g, h = H[0], H[1], H[2], H[3], H[4], H[5], H[6], H[7]
    
    # 64 rounds
    for i in range(64):
        S1 = right_rotate(e, 6) ^ right_rotate(e, 11) ^ right_rotate(e, 25)
        ch = (e & f) ^ (~e & g)
        temp1 = (h + S1 + ch + K_256[i] + W[i]) & 0xFFFFFFFF
        
        S0 = right_rotate(a, 2) ^ right_rotate(a, 13) ^ right_rotate(a, 22)
        maj = (a & b) ^ (a & c) ^ (b & c)
        temp2 = (S0 + maj) & 0xFFFFFFFF
        
        h = g
        g = f
        f = e
        e = (d + temp1) & 0xFFFFFFFF
        d = c
        c = b
        b = a
        a = (temp1 + temp2) & 0xFFFFFFFF
    
    # Add to hash state
    H[0] = (H[0] + a) & 0xFFFFFFFF
    H[1] = (H[1] + b) & 0xFFFFFFFF
    H[2] = (H[2] + c) & 0xFFFFFFFF
    H[3] = (H[3] + d) & 0xFFFFFFFF
    H[4] = (H[4] + e) & 0xFFFFFFFF
    H[5] = (H[5] + f) & 0xFFFFFFFF
    H[6] = (H[6] + g) & 0xFFFFFFFF
    H[7] = (H[7] + h) & 0xFFFFFFFF
    
    return H


def SHA256(message):
    """Complete SHA-256 hash function"""
    # Initial hash values (first 32 bits of fractional parts of square roots of first 8 primes)
    H = [
        0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
        0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
    ]
    
    # Process message
    padded = padding(message)
    blocks = split_blocks(padded)
    
    for block in blocks:
        H = compression_sha256(block, H)
    
    # Convert to hex string
    return ''.join(f'{h:08x}' for h in H)
