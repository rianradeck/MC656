import pygame

from client.ui.tools import InputBox


class Lobby:
    def __init__(self, font):
        self.font = font
        self.ib_nickname = InputBox(
            220, 150, 200, 40, font, "white", "Nickname"
        )
        self.ib_ip = InputBox(220, 230, 200, 40, font, "white", "IP")
        self.input_boxes = [self.ib_nickname, self.ib_ip]
        # Play button
        self.button_rect = pygame.Rect(270, 300, 100, 50)

    def handle_lobby_event(self, event):
        for box in self.input_boxes:
            box.handle_event(event)

        # Handle button click
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button_rect.collidepoint(event.pos):
                print("Play button pressed")
                print("Nickname:", self.ib_nickname.text)
                print("IP:", self.ib_ip.text)
                # Add action for play button
                return self.ib_nickname.text, self.ib_ip.text

    def draw_lobby(self, screen):
        for box in self.input_boxes:
            box.update()

        screen.fill("black")
        for box in self.input_boxes:
            box.draw(screen)

        # Draw the play button
        pygame.draw.rect(screen, "gray", self.button_rect)
        play_text = self.font.render("Play", True, "black")
        screen.blit(
            play_text, (self.button_rect.x + 20, self.button_rect.y + 10)
        )
