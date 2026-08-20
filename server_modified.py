"""
Challenge-response authentication server.

Protocol:
    1. Client sends: "HELLO"
    2. Server sends: "USERNAME?"
    3. Client sends: <username>
    4. Server generates a random challenge (nonce), sends: "CHALLENGE:<hex_nonce>"
    5. Client computes HMAC-SHA256(password, nonce), sends: "RESPONSE:<hex_digest>"
    6. Server computes the same HMAC using its stored password and compares,
       sends: "SUCCESS" or "FAILURE"

Unlike the original protocol, the password itself is never sent over the
network. Instead, the client proves it knows the password by producing a
keyed HMAC over a fresh random challenge supplied by the server.

Run with:
    python3 server_modified.py
"""

import socket
import os
import hmac
import hashlib

HOST = "127.0.0.1"
PORT = 5000

# In a real system, only a hash or the plaintext password would be stored
# server-side (never both, and ideally salted/hashed at rest too).
VALID_USERNAME = "sugansha"
VALID_PASSWORD = "123"


def recv_line(conn):
    """Receive a message from the socket and decode it to a string."""
    data = conn.recv(1024)
    return data.decode("utf-8").strip()


def send_line(conn, message):
    """Encode and send a string message over the socket."""
    conn.sendall(message.encode("utf-8"))


def handle_client(conn, addr):
    print(f"[SERVER] Connection from {addr}")

    # 1. Expect HELLO from client
    hello = recv_line(conn)
    print(f"[SERVER] Received: {hello!r}")
    if hello != "HELLO":
        send_line(conn, "FAILURE")
        return

    # 2. Ask for username
    send_line(conn, "USERNAME?")

    # 3. Receive username
    username = recv_line(conn)
    print(f"[SERVER] Received username: {username!r}")

    # 4. Generate a random challenge (nonce) and send it
    nonce = os.urandom(16).hex()
    send_line(conn, f"CHALLENGE:{nonce}")
    print(f"[SERVER] Sent challenge: {nonce}")

    # 5. Receive the client's response
    response = recv_line(conn)
    print(f"[SERVER] Received response: {response!r}")

    if not response.startswith("RESPONSE:"):
        print("[SERVER] Authentication FAILURE (malformed response)")
        send_line(conn, "FAILURE")
        return
    client_digest = response.split("RESPONSE:", 1)[1]

    # 6. Compute the expected HMAC using the stored password and compare
    if username == VALID_USERNAME:
        expected_digest = hmac.new(
            VALID_PASSWORD.encode("utf-8"),
            nonce.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()

        if hmac.compare_digest(client_digest, expected_digest):
            print("[SERVER] Authentication SUCCESS")
            send_line(conn, "SUCCESS")
            return

    print("[SERVER] Authentication FAILURE")
    send_line(conn, "FAILURE")


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((HOST, PORT))
        server_sock.listen(1)
        print(f"[SERVER] Listening on {HOST}:{PORT}")

        while True:
            conn, addr = server_sock.accept()
            with conn:
                handle_client(conn, addr)


if __name__ == "__main__":
    main()
