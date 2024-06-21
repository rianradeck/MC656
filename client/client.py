import argparse
import asyncio
import socket
import time

import pygame
import ui

import common.grid
import common.network
from common.direction import Direction
from common.packet import PacketType


async def process_events(serverConnection, running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            send_move = lambda x: serverConnection.send(
                int.to_bytes(PacketType.PLAYER_MOVE.value)
                + int.to_bytes(x.value)
            )

            if event.key in [pygame.K_LEFT, pygame.K_a]:
                send_move(Direction.LEFT)
            elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                send_move(Direction.RIGHT)
            elif event.key in [pygame.K_UP, pygame.K_w]:
                send_move(Direction.UP)
            elif event.key in [pygame.K_DOWN, pygame.K_s]:
                send_move(Direction.DOWN)
    return running


async def main(args):
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((args.ip, args.port))
    conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    conn.setblocking(False)

    serverConnection = common.network.NetworkConnection(conn)

    running = True

    lastFrameTime = time.time_ns()
    TARGET_UPS = 20

    grid = common.grid.Grid()

    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    # https://gameprogrammingpatterns.com/game-loop.html
    while running:
        serverConnection.process()

        running = await process_events(serverConnection, running)

        packet = serverConnection.recv()
        if packet is not None:
            type = PacketType(packet[0])
            if type == PacketType.PLAYER_ID:
                print(type, packet)
            elif type == PacketType.GRID_STATE:
                grid.deserialize(packet[1:])
                print(type)

        screen.fill("deepskyblue")
        ui.draw_grid(screen, grid)
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
