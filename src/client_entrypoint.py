import argparse
import asyncio
import socket
import time
from pathlib import Path

import pygame

import client.main
import common.grid
import common.network


async def process_events(running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        await client.main.handle_event(event)

    return running


async def connect_to_server(ip, port):
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((ip, port))
    conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    conn.setblocking(False)

    serverConnection = common.network.NetworkConnection(conn)
    return serverConnection


async def main(args):
    running = True

    lastFrameTime = time.time_ns()
    TARGET_UPS = 20

    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Cobrinha")
    # https://gameprogrammingpatterns.com/game-loop.html
    while running:
        running = await process_events(running)

        client.main.draw_screen(screen)

        pygame.display.flip()

        curFrameTime = time.time_ns()
        deltaTime = curFrameTime - lastFrameTime
        sleeptime = 1 / TARGET_UPS - deltaTime / 1000000000
        if sleeptime > 0:
            await asyncio.sleep(sleeptime)
        lastFrameTime = curFrameTime


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="server executable")
    arg_parser.add_argument("--port", default=25565)
    arg_parser.add_argument("--ip", default="127.0.0.1")
    args = arg_parser.parse_args()

    asyncio.run(main(args))
