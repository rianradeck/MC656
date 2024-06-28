from pathlib import Path

import pygame

from client.ui.game import Game
from client.ui.lobby import Lobby
from common.grid import Grid

pygame.font.init()
font = pygame.font.Font(
    Path(__file__).parent.parent / "resources/Jersey25-Regular.ttf", 40
)
screen_state = "lobby"

lobby = Lobby(font)


def handle_event(event):
    global screen_state

    match screen_state:
        case "lobby":
            lobby.handle_lobby_event(event)
        case "game":
            game.handle_game_event(event)


def draw_screen(screen):
    global screen_state

    match screen_state:
        case "lobby":
            lobby.draw_lobby(screen)
        case "game":
            game.draw_stats(screen, font)
            game.draw_grid(screen, Grid())


def change_state(new_state):
    global screen_state

    if screen_state == "lobby" and new_state == "game":
        global game
        game = Game(font)
    screen_state = new_state


if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Cobrinha")

    font = pygame.font.Font("resources/Jersey25-Regular.ttf", 40)

    screen = pygame.display.set_mode((1280, 720))

    pygame.quit()
