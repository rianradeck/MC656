import argparse
import asyncio
import socket
import time

import common.grid
import common.network
from common.direction import Direction
from common.packet import PacketType


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


async def wait_connections(args, NUM_PLAYERS):
    listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listening_socket.bind(("0.0.0.0", args.port))
    listening_socket.listen()

    loop = asyncio.get_event_loop()

    player_connections = []
    for i in range(NUM_PLAYERS):
        # sock, addr = listening_socket.accept()
        sock, addr = await loop.sock_accept(listening_socket)
        print(f"Player {i} connected at {addr}")
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        sock.setblocking(False)

        player_connections.append(common.network.NetworkConnection(sock))
    listening_socket.close()
    return player_connections


async def init_players(grid, snakes, player_connections, NUM_PLAYERS):
    for i in range(NUM_PLAYERS):
        for pos in snakes[i]:
            grid[pos] = common.grid.GridObject.snake_from_index(i)

    for i in range(2):
        player_connections[i].send(
            int.to_bytes(PacketType.PLAYER_ID.value, length=1, byteorder="big")
            + int.to_bytes(i, length=1, byteorder="big")
        )
        player_connections[i].send(
            int.to_bytes(
                PacketType.GRID_STATE.value, length=1, byteorder="big"
            )
            + grid.serialize()
        )


async def tick(snakes, grid, last_move, player_connections, NUM_PLAYERS):
    game_over = False
    for i in range(NUM_PLAYERS):
        direction = last_move[i]

        last_snake = snakes[i].copy()
        snakes[i] = move_snake(direction, grid, snakes[i])
        if last_snake == snakes[i]:
            print(f"Player {i} didnt move. Game over")
            game_over = True

    for j in range(NUM_PLAYERS):
        player_connections[j].send(
            int.to_bytes(
                PacketType.GRID_STATE.value,
                length=1,
                byteorder="big",
            )
            + grid.serialize()
        )
        if game_over:
            player_connections[j].send(
                int.to_bytes(
                    PacketType.GAME_OVER.value, length=1, byteorder="big"
                )
            )

    return game_over


async def process_players(NUM_PLAYERS, player_connections, last_move):
    for i in range(NUM_PLAYERS):
        player_connections[i].process()

        packet = player_connections[i].recv()
        if packet is not None:
            type = PacketType(packet[0])
            if type == PacketType.PLAYER_MOVE:
                direction = Direction(packet[1])
                last_move[i] = direction


async def main(args, NUM_PLAYERS):
    player_connections = await wait_connections(args, NUM_PLAYERS)
    print("Both players connected. Starting match.")

    grid = common.grid.Grid()
    # grid.fill_borders()

    snakes = [
        # player1_snake
        [(3, 1), (4, 1), (5, 1)],
        # player2_snake
        [(6, 8), (5, 8), (4, 8)],
    ]

    await init_players(grid, snakes, player_connections, NUM_PLAYERS)

    lastFrameTime = time.time_ns()
    TARGET_UPS = 60

    timer = 0
    last_move = [Direction.UP, Direction.DOWN]

    running = True
    game_over = False
    while running:
        await process_players(NUM_PLAYERS, player_connections, last_move)

        if timer >= 1 / args.tickrate and not game_over:
            game_over = await tick(
                snakes, grid, last_move, player_connections, NUM_PLAYERS
            )
            timer = 0

        curFrameTime = time.time_ns()
        deltaTime = curFrameTime - lastFrameTime
        timer += deltaTime / 1e9
        sleeptime = 1 / TARGET_UPS - deltaTime / 1e9
        if sleeptime > 0:
            await asyncio.sleep(sleeptime)
        lastFrameTime = curFrameTime


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="server executable")
    arg_parser.add_argument("--port", default=25565)
    arg_parser.add_argument("--tickrate", default=1)
    args = arg_parser.parse_args()

    NUM_PLAYERS = 2
    asyncio.run(main(args, NUM_PLAYERS))
