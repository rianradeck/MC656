import pygame

from common.grid import GridObject


class Game:
    def __init__(self, font):
        self.font = font

    def draw_stats(self, screen):
        font_img = self.font.render("Score: 0", True, "white")
        font_shadow = self.font.render("Score: 0", True, "black")
        screen.blit(font_shadow, (100 - 2, 100 + 2))
        screen.blit(font_img, (100, 100))

    def draw_grid(screen, grid, margin=10, cell_width=50, cell_height=50):
        background_border = 10

        width, height = screen.get_size()

        total_width = grid.width * (cell_width + margin) - margin
        total_height = grid.height * (cell_height + margin) - margin

        x_offset = (width - total_width) / 2
        y_offset = (height - total_height) / 2

        pygame.draw.rect(
            screen,
            "gray",
            pygame.Rect(
                x_offset - background_border / 2,
                y_offset - background_border / 2,
                total_width + background_border,
                total_height + background_border,
            ),
        )

        for i in range(grid.height):
            for j in range(grid.width):
                x_position = x_offset + (cell_width + margin) * j
                y_position = y_offset + (cell_height + margin) * i

                color = ""

                if grid[(i, j)] == GridObject.EMPTY:
                    color = "white"
                elif grid[(i, j)] == GridObject.WALL:
                    color = "black"
                elif grid[(i, j)] == GridObject.SNAKE_1:
                    color = "blue"
                elif grid[(i, j)] == GridObject.SNAKE_2:
                    color = "green"
                elif grid[(i, j)] == GridObject.APPLE:
                    color = "red"
                pygame.draw.rect(
                    screen,
                    color,
                    pygame.Rect(
                        x_position, y_position, cell_width, cell_height
                    ),
                )
