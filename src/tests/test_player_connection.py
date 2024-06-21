import asyncio
import multiprocessing
from unittest.mock import Mock

import client.client
import server.server


def wip_test_connect():
    args = Mock()
    args.port = 25565

    server_proc = multiprocessing.Process(
        asyncio.run(server.server.main(args, 2))
    )
    args.ip = "127.0.0.1"
    client1_proc = multiprocessing.Process(
        asyncio.run(client.client.main(args))
    )
    client2_proc = multiprocessing.Process(
        asyncio.run(client.client.main(args))
    )

    server_proc.start()
    client1_proc.start()
    client2_proc.start()

    print("OK")

    try:
        server_proc.kill()
        client1_proc.kill()
        client2_proc.kill()

        server_proc.join()
        client1_proc.join()
        client2_proc.join()
    except Exception:
        pass


if __name__ == "__main__":
    wip_test_connect()
