import socket
import threading

HOST = '127.0.0.1'
PORT = 5050


def receive_messages(sock):
    while True:
        try:
            msg = sock.recv(1024).decode("utf-8")
            if not msg:
                break
            print(msg)
        except:
            print("Disconnected from server.")
            break


def main():
    print(f"Connecting to {HOST}:{PORT}...")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    threading.Thread(target=receive_messages, args=(client,), daemon=True).start()

    while True:
        message = input()
        client.sendall((message + "\n").encode())

        if message.lower() == "quit":
            break

    client.close()
    print("Client closed.")


if __name__ == "__main__":
    main()
