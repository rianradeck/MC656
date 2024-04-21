import multiprocessing
import time

from client.network import ClientConnection
from server.network import ServerConnection


def run_server():
    server = ServerConnection()
    server.start_listening()


def run_client():
    client = ClientConnection()

    client.start_connection()

    message = "Hello Server!"
    client.send_message(message)

    time.sleep(1)
    client.close_connection()


def main():
    pserver = multiprocessing.Process(target=run_server)
    pserver.start()

    time.sleep(1)
    run_client()
    time.sleep(1)

    pserver.kill()
    pserver.join()


if __name__ == "__main__":
    main()
