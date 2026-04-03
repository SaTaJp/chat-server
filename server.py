import socket
import threading

HOST = '0.0.0.0'
PORT = 5050

clients = []
client_ids = {}
next_id = 1
lock = threading.Lock()


def broadcast(message):
    with lock:
        for client in clients:
            try:
                client.sendall((message + "\n").encode("utf-8"))
            except:
                pass


def remove_client(client):
    global clients
    with lock:
        user_id = client_ids.get(client, "Unknown")
        if client in clients:
            clients.remove(client)
        broadcast(f"[Server] {user_id} left the chat.")
        print_user_list()


def print_user_list():
    with lock:
        users = [client_ids[c] for c in clients]
    msg = "[Server] Online users: " + ", ".join(users)
    print(msg)
    broadcast(msg)


def handle_client(client, address, user_id):
    try:
        client.sendall(f"[Server] Welcome! Your ID is {user_id}\n".encode())
        client.sendall("[Server] Type 'quit' to leave.\n".encode())

        while True:
            data = client.recv(1024)
            if not data:
                break

            message = data.decode("utf-8").strip()

            if message.lower() == "quit":
                break

            if message:
                broadcast(f"[{user_id}] {message}")

    except:
        pass
    finally:
        remove_client(client)
        client.close()


def start_server():
    global next_id

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"Server started on port {PORT}")

    while True:
        client, addr = server.accept()

        with lock:
            user_id = f"User{next_id}"
            next_id += 1

            clients.append(client)
            client_ids[client] = user_id

        threading.Thread(target=handle_client, args=(client, addr, user_id)).start()

        broadcast(f"[Server] {user_id} joined the chat.")
        print_user_list()


if __name__ == "__main__":
    start_server()
