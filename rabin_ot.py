from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes, inverse
import random

def generate_rabin_keys(bits=512):
    p = getPrime(bits)
    q = getPrime(bits)
    N = p * q
    return (p, q, N)

def encode_message(msg):
    return bytes_to_long(msg.encode('utf-8'))

def decode_message(encoded):
    try:
        return long_to_bytes(encoded).decode('utf-8')
    except:
        return "[!] Failed to decode message."

def receiver_prepare(N, choice):
    r = random.randrange(1, N)
    if choice == 0:
        k = pow(r, 2, N)  # Send a perfect square
    else:
        k = (pow(r, 2, N) * 2) % N  # Non-square by multiplying with non-square like 2
    return r, k

def sender_prepare(p, q, N, k, m0, m1):
    # Check if k has a square root modulo N (quadratic residuosity)
    def is_quadratic_residue(k, p, q):
        return pow(k, (p-1)//2, p) == 1 and pow(k, (q-1)//2, q) == 1

    # Encrypt
    if is_quadratic_residue(k, p, q):
        c0 = (k + m0) % N
        c1 = random.randint(1, N-1)  # Random garbage
    else:
        c0 = random.randint(1, N-1)  # Random garbage
        c1 = (k + m1) % N
    return c0, c1

def receiver_recover(r, c0, c1, choice, N):
    if choice == 0:
        result = (c0 - pow(r,2,N)) % N
    else:
        result = (c1 - (pow(r,2,N)*2)%N) % N
    return result
