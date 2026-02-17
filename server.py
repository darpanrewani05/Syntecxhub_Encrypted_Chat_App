import socket
import threading
from crypto_utils import decrypt_message, encrypt_message
from datetime import datetime


HOST = '127.0.0.1'
PORT = 5000

clients = []


# Broadcast message to all clients
def broadcast(message, sender_socket):

    for client in clients:
        if client != sender_socket:
            try:
                encrypted = encrypt_message(message)
                client.send(encrypted)
            except:
                client.close()
                clients.remove(client)


# Handle client
def handle_client(client_socket, address):

    print(f"[NEW CONNECTION] {address} connected.")

    while True:
        try:
            encrypted_message = client_socket.recv(1024)

            if not encrypted_message:
                break

            message = decrypt_message(encrypted_message)

            print(f"[{address}] {message}")

            # Log message
            with open("chat_log.txt", "a") as file:
                file.write(f"{datetime.now()} {address}: {message}\n")

            # Broadcast to others
            broadcast(message, client_socket)

        except:
            break

    clients.remove(client_socket)
    client_socket.close()
    print(f"[DISCONNECTED] {address}")


# Start server
def start_server():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind((HOST, PORT))

    server.listen()

    print(f"[LISTENING] Server running on {HOST}:{PORT}")

    while True:

        client_socket, address = server.accept()

        clients.append(client_socket)

        thread = threading.Thread(target=handle_client, args=(client_socket, address))

        thread.start()


start_server()
