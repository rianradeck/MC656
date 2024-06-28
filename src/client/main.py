import socket
import uuid
from pathlib import Path

import pygame

import common.network
from client.ui.game import Game
from client.ui.lobby import Lobby
from common.grid import Grid
from common.packet import PacketType

pygame.font.init()
font = pygame.font.Font(
    Path(__file__).parent.parent / "resources/Jersey25-Regular.ttf", 40
)
screen_state = "lobby"

lobby = Lobby(font)
game = Game(font)
grid = Grid()
ip, nick = None, None
server_connection = None


async def connect_to_server(ip, port):
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((ip, port))
    conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    conn.setblocking(False)

    serverConnection = common.network.NetworkConnection(conn)
    return serverConnection


async def handle_event(event):
    global screen_state, ip, nick, server_connection

    match screen_state:
        case "lobby":
            args = lobby.handle_lobby_event(event)
            if args:
                await change_state("game", args)

        case "game":
            game.handle_game_event(event, server_connection)


def draw_screen(screen):
    global screen_state, grid

    match screen_state:
        case "lobby":
            lobby.draw_lobby(screen)
        case "game":
            game.draw_stats(screen)
            game.draw_grid(screen, grid)
            server_connection.process()
            packet = server_connection.recv()
            if packet is not None:
                type = PacketType(packet[0])
                if type == PacketType.PLAYER_ID:
                    print(type, packet)
                elif type == PacketType.GRID_STATE:
                    grid.deserialize(packet[1:])
                    print(type)


async def change_state(new_state, args):
    global screen_state, ip, nick, server_connection

    screen_state = new_state

    nick, ip = args
    if ip == "":
        nick = uuid.uuid4().hex[:8]
        ip = "127.0.0.1"
    server_connection = await connect_to_server(ip, 25565)


if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Cobrinha")

    font = pygame.font.Font("resources/Jersey25-Regular.ttf", 40)

    screen = pygame.display.set_mode((1280, 720))

    pygame.quit()
