import select
from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread


class ServerConnection:
    def __init__(self):
        self.open_client_sockets = []
        self.socket = self.get_socket()

    def get_socket(self, host: str = "127.0.0.1", port: int = 12345) -> socket:
        # Create a socket object
        server_socket = socket(AF_INET, SOCK_STREAM)

        # Bind the socket to the host and port
        server_socket.bind((host, port))

        return server_socket

    def start_listening(self) -> None:
        self.socket.listen()
        _ip, _port = self.socket.getsockname()
        print(f"Listening on {_ip}:{_port}")

        # Main listening loop
        while True:
            try:
                ready_to_read, _, _ = select.select(
                    [self.socket], [], [], 1.0
                )  # Timeout set to 1 second
                if self.socket in ready_to_read:
                    # Accept a client connection
                    client_socket, client_address = self.socket.accept()
                    self.open_client_sockets.append(client_socket)

                    # Start a new thread to handle the client
                    client_thread = Thread(
                        target=self.handle_client,
                        args=(client_socket, client_address),
                    )
                    client_thread.start()
            except KeyboardInterrupt:
                print("Stopping server...")
                self.stop_server()
                break

    def handle_client(
        self, client_socket: socket, client_address: str
    ) -> None:
        print("Connection from:", client_address)

        while True:
            # Receive data from the client
            try:
                data = client_socket.recv(1024).decode("utf-8")
            except ConnectionAbortedError:
                break
            if not data:
                break
            if data == "exit":
                break

            print(f"Received from {client_address}: {data}")

        # Close the connection
        client_socket.close()
        print(f"Connection with {client_address} closed.")

    def stop_server(self) -> None:
        for client_socket in self.open_client_sockets:
            client_socket.close()
        self.socket.close()


if __name__ == "__main__":
    server = ServerConnection()
    server.start_listening()
