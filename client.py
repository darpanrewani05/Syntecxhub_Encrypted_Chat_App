import socket
import threading
from crypto_utils import encrypt_message, decrypt_message

HOST = '127.0.0.1'
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

print("[CONNECTED] Connected to server.")


# Receive messages
def receive():

    while True:
        try:
            encrypted = client.recv(1024)

            if not encrypted:
                break

            print(f"\n[ENCRYPTED RECEIVED]: {encrypted}")

            message = decrypt_message(encrypted)

            print(f"[DECRYPTED MESSAGE]: {message}")

        except:
            print("[ERROR] Connection closed.")
            break


# Start receive thread
thread = threading.Thread(target=receive)
thread.daemon = True
thread.start()


# Send messages
while True:

    message = input("You: ")

    if message.lower() == 'exit':
        client.close()
        print("[DISCONNECTED]")
        break

    encrypted = encrypt_message(message)

    print(f"[ENCRYPTED SENT]: {encrypted}")

    client.send(encrypted)
