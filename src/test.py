import asyncio
from unittest.mock import Mock

import client_entrypoint
import server_entrypoint


async def main():
    args = Mock()
    args.port = 25565
    args.ip = "127.0.0.1"

    server_task = asyncio.create_task(server_entrypoint.main(args, 2))
    client1_task = asyncio.create_task(client_entrypoint.main(args))
    client2_task = asyncio.create_task(client_entrypoint.main(args))

    await server_task
    await client1_task
    await client2_task


asyncio.run(main())
