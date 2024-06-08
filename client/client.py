import argparse
import enum
import socket
import time

import pygame
import ui

import common.grid
import common.network


class PacketType(enum.Enum):
    PLAYER_ID = enum.auto()
    GRID_STATE = enum.auto()
    PLAYER_MOVE = enum.auto()


class Direction(enum.Enum):
    UP = enum.auto()
    RIGHT = enum.auto()
    DOWN = enum.auto()
    LEFT = enum.auto()

    def get_displacement(self):
        return {
            Direction.UP: (-1, 0),
            Direction.DOWN: (1, 0),
            Direction.LEFT: (0, -1),
            Direction.RIGHT: (0, 1),
        }[self]


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="server executable")
    arg_parser.add_argument("--port", default=25565)
    arg_parser.add_argument("--ip", default="127.0.0.1")
    args = arg_parser.parse_args()

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

        packet = serverConnection.recv()
        if packet != None:
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
            time.sleep(sleeptime)
        lastFrameTime = curFrameTime
