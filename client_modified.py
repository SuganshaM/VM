"""
Challenge-response authentication client.

Follows the same protocol as server_modified.py. The password is never
sent over the network -- instead, the client proves it knows the password
by computing an HMAC-SHA256 over a server-supplied random challenge
(nonce), keyed with the password.

Run with:
    python3 client_modified.py
"""

import socket
import hmac
import hashlib

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

        # 4. Receive the challenge
        challenge_msg = recv_line(sock)
        print(f"[CLIENT] Server says: {challenge_msg}")
        nonce = challenge_msg.split("CHALLENGE:", 1)[1]

        # 5. Compute HMAC-SHA256(password, nonce) and send it back
        digest = hmac.new(
            password.encode("utf-8"),
            nonce.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()
        send_line(sock, f"RESPONSE:{digest}")

        # 6. Receive result
        result = recv_line(sock)
        print(f"[CLIENT] Server says: {result}")

        if result == "SUCCESS":
            print("Login successful!")
        else:
            print("Login failed.")


if __name__ == "__main__":
    main()
