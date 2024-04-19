import os
import sys
import time
from pathlib import Path
from threading import Thread

from client.network import ClientConnection
from server.network import ServerConnection

source_dir = Path(os.path.dirname(__file__)).parent
sys.path.append(str(source_dir) + "/.")


def main():
    # Start the server
    server = ServerConnection()
    server_thread = Thread(target=server.start_listening)
    server_thread.start()

    # Allow some time for the server to start listening
    time.sleep(1)

    # Connect the client to the server
    client = ClientConnection()
    message = "Hello, server!"
    client.send_message(message)

    # Close the client connection
    client.close_connection()

    # Stop the server
    server.stop_server()


if __name__ == "__main__":
    main()
