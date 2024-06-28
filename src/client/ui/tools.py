import pygame

# from client.ui.color import *


class InputBox:
    def __init__(self, x, y, w, h, font, color, text=""):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.text = ""
        self.box_text = text
        self.font = font
        self.box_surface = font.render(self.box_text, True, self.color)
        self.txt_surface = font.render("", True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input box rect.
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = "white" if self.active else "gray"
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(
                    self.text, True, self.color
                )

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.box_surface, (self.rect.x, self.rect.y - 40))
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2, 5)
