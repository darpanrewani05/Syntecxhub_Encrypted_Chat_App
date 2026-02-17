import socket
import threading
from datetime import datetime

HOST = '127.0.0.1'
PORT = 5000

clients = []


# Broadcast encrypted message to all clients
def broadcast(encrypted_message, sender_socket):

    for client in clients:
        if client != sender_socket:
            try:
                client.send(encrypted_message)
            except:
                client.close()
                clients.remove(client)


# Handle each client
def handle_client(client_socket, address):

    print(f"[NEW CONNECTION] {address} connected.")

    while True:
        try:
            encrypted_message = client_socket.recv(1024)

            if not encrypted_message:
                break

            print(f"[FORWARDING] Encrypted message from {address}")

            # Log encrypted message
            with open("chat_log.txt", "a") as file:
                file.write(f"{datetime.now()} {address}: {encrypted_message}\n")

            # Broadcast encrypted message
            broadcast(encrypted_message, client_socket)

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

        thread = threading.Thread(
            target=handle_client,
            args=(client_socket, address)
        )

        thread.start()


start_server()
