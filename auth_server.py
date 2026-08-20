"""
Simple username/password authentication server.

Protocol (alternating send/receive):
    1. Client sends: "HELLO"
    2. Server receives HELLO, sends: "USERNAME?"
    3. Client receives request, sends: <username>
    4. Server receives username, sends: "PASSWORD?"
    5. Client receives request, sends: <password>
    6. Server checks credentials, sends: "SUCCESS" or "FAILURE"

Run with:
    python3 auth_server.py
"""

import socket

HOST = "127.0.0.1"
PORT = 5000

# Hard-coded valid credentials (in a real system these would be looked up
# in a database, and passwords would never be stored in plaintext).
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

    # 4. Ask for password
    send_line(conn, "PASSWORD?")

    # 5. Receive password
    password = recv_line(conn)
    print(f"[SERVER] Received password: {password!r}")

    # 6. Check credentials and respond
    if username == VALID_USERNAME and password == VALID_PASSWORD:
        print("[SERVER] Authentication SUCCESS")
        send_line(conn, "SUCCESS")
    else:
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
