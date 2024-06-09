import argparse
import enum
import socket
import time

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


def move_snake(direction, grid, snake):
    displacement = direction.get_displacement()
    head = snake[0]
    new_head = (
        head[0] + displacement[0],
        head[1] + displacement[1],
    )

    new_head = (new_head[0] % grid.height, new_head[1] % grid.width)

    if grid[new_head] == common.grid.GridObject.EMPTY:
        temp = grid[snake[0]]
        grid[snake[-1]] = common.grid.GridObject.EMPTY
        snake = [new_head] + snake[:-1]
        grid[new_head] = temp

    return snake


def wait_connections(args, NUM_PLAYERS):
    listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listening_socket.bind(("0.0.0.0", args.port))
    listening_socket.listen()

    player_connections = []
    for i in range(NUM_PLAYERS):
        sock, addr = listening_socket.accept()
        print(f"Player {i} connected at {addr}")
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        sock.setblocking(False)

        player_connections.append(common.network.NetworkConnection(sock))
    listening_socket.close()
    return player_connections


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="server executable")
    arg_parser.add_argument("--port", default=25565)
    args = arg_parser.parse_args()

    NUM_PLAYERS = 2
    player_connections = wait_connections(args, NUM_PLAYERS)
    print("Both players connected. Starting match.")

    grid = common.grid.Grid()
    # grid.fill_borders()

    snakes = [
        # player1_snake
        [(3, 1), (4, 1), (5, 1)],
        # player2_snake
        [(6, 8), (5, 8), (4, 8)],
    ]

    for i in range(NUM_PLAYERS):
        for pos in snakes[i]:
            grid[pos] = common.grid.GridObject.snake_from_index(i)

    for i in range(2):
        player_connections[i].send(
            int.to_bytes(PacketType.PLAYER_ID.value) + int.to_bytes(i)
        )
        player_connections[i].send(
            int.to_bytes(PacketType.GRID_STATE.value) + grid.serialize()
        )

    lastFrameTime = time.time_ns()
    TARGET_UPS = 60

    running = True
    while running:
        for i in range(NUM_PLAYERS):
            player_connections[i].process()

            packet = player_connections[i].recv()
            if packet is not None:
                type = PacketType(packet[0])
                if type == PacketType.PLAYER_MOVE:
                    direction = Direction(packet[1])

                    snakes[i] = move_snake(direction, grid, snakes[i])

                    for j in range(2):
                        player_connections[j].send(
                            int.to_bytes(PacketType.GRID_STATE.value)
                            + grid.serialize()
                        )

        curFrameTime = time.time_ns()
        deltaTime = curFrameTime - lastFrameTime
        sleeptime = 1 / TARGET_UPS - deltaTime / 1000000000
        if sleeptime > 0:
            time.sleep(sleeptime)
        lastFrameTime = curFrameTime
