import socket
from rabin_ot import receiver_prepare, receiver_recover, decode_message
import os

HOST = '127.0.0.1'
PORT = 65434

print("[Receiver] Connecting...")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    # Receive N
    N = int(s.recv(4096).decode())

    print("What do you want to receive?")
    print("0 -> Message")
    print("1 -> File")

    type_choice = int(input("Enter your choice: "))
    choice = int(input("Which one? (0 or 1): "))

    r, k = receiver_prepare(N, choice)

    # Send k and type_choice
    s.sendall(f"{k},{type_choice}".encode())

    # Receive c0, c1
    data = s.recv(8192).decode()
    c0, c1 = map(int, data.split(','))

    result = receiver_recover(r, c0, c1, choice, N)

    if type_choice == 0:
        # Message Mode
        print("[Receiver] Message received:", decode_message(result))
    else:
        # File Mode
        output_filename = input("Enter filename to save received file (e.g., received.bin): ")
        file_bytes = result.to_bytes((result.bit_length() + 7) // 8, byteorder='big')
        with open(output_filename, 'wb') as f:
            f.write(file_bytes)
        print(f"[Receiver] File saved as {output_filename}")
