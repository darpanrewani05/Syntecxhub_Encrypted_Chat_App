import socket
import threading
from crypto_utils import encrypt_message, decrypt_message


HOST = '127.0.0.1'
PORT = 5000


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

print("Connected to server.")


# Receive messages
def receive():

    while True:
        try:
            encrypted = client.recv(1024)

            message = decrypt_message(encrypted)

            print(f"\nReceived: {message}")

        except:
            break


threading.Thread(target=receive).start()


# Send messages
while True:

    message = input("You: ")

    if message.lower() == 'exit':
        break

    encrypted = encrypt_message(message)

    client.send(encrypted)


client.close()
