import socket
import os
from rabin_ot import generate_rabin_keys, encode_message, sender_prepare

HOST = '127.0.0.1'
PORT = 65434

# Generate keys
p, q, N = generate_rabin_keys()

print("[Sender] Ready.")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"[Sender] Connected to {addr}")

        # Send N
        conn.sendall(str(N).encode())

        # Receive k and type_choice
        received = conn.recv(4096).decode()
        k_str, type_choice = received.split(',')
        k = int(k_str)
        type_choice = int(type_choice)

        if type_choice == 0:  # Message mode
            m0 = input("Enter message 0: ")
            m1 = input("Enter message 1: ")

            m0_encoded = encode_message(m0)
            m1_encoded = encode_message(m1)

        else:  # File mode
            file0 = input("Enter path for file 0: ")
            file1 = input("Enter path for file 1: ")

            with open(file0, 'rb') as f:
                m0_encoded = int.from_bytes(f.read(), byteorder='big')

            with open(file1, 'rb') as f:
                m1_encoded = int.from_bytes(f.read(), byteorder='big')

        c0, c1 = sender_prepare(p, q, N, k, m0_encoded, m1_encoded)

        # Send ciphertexts
        conn.sendall(f"{c0},{c1}".encode())
