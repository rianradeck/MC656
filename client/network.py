from __future__ import annotations

import socket
import sys


class ClientConnection:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start_connection(
        self, server_host: str = "127.0.0.1", server_port: int = 12345
    ):
        self.socket.connect((server_host, server_port))

    def send_message(self, message: str) -> bool:
        """
        Returns True if the message was "exit" and closes the connection
        """

        if message.lower() == "exit":
            self.close_connection()
            return True

        try:
            self.socket.send(message.encode("utf-8"))
        except ConnectionResetError:
            print("Server closed connection")

        return False

    def close_connection(self) -> None:
        print("Closing connection...")
        self.socket.close()


if __name__ == "__main__":
    try:
        message = sys.argv[1]
    except Exception:
        message = ""

    client = ClientConnection()
    client.start_connection()

    while True:
        try:
            if message:
                exited = client.send_message(message)
                message = ""
            else:
                exited = client.send_message(
                    input("Enter a message (or 'exit' to quit): ")
                )

            if exited:
                break
        except KeyboardInterrupt:
            client.close_connection()
            break
