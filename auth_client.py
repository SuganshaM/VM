"""
Simple username/password authentication client.

Follows the same protocol as auth_server.py:
    1. Client sends: "HELLO"
    2. Server receives HELLO, sends: "USERNAME?"
    3. Client receives request, sends: <username>
    4. Server receives username, sends: "PASSWORD?"
    5. Client receives request, sends: <password>
    6. Server checks credentials, sends: "SUCCESS" or "FAILURE"

Run with:
    python3 auth_client.py
"""

import socket

HOST = "127.0.0.1"
PORT = 5000


def recv_line(sock):
    data = sock.recv(1024)
    return data.decode("utf-8").strip()


def send_line(sock, message):
    sock.sendall(message.encode("utf-8"))


def main():
    username = input("Username: ")
    password = input("Password: ")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))

        # 1. Send HELLO
        send_line(sock, "HELLO")

        # 2. Receive request for username
        request = recv_line(sock)
        print(f"[CLIENT] Server says: {request}")

        # 3. Send username
        send_line(sock, username)

        # 4. Receive request for password
        request = recv_line(sock)
        print(f"[CLIENT] Server says: {request}")

        # 5. Send password
        send_line(sock, password)

        # 6. Receive result
        result = recv_line(sock)
        print(f"[CLIENT] Server says: {result}")

        if result == "SUCCESS":
            print("Login successful!")
        else:
            print("Login failed.")


if __name__ == "__main__":
    main()
