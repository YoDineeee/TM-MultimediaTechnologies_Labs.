import pygame
import random

class Grid:
    def __init__(self, width, height, cell_size):
        self.rows = height // cell_size
        self.columns = width // cell_size
        self.cell_size = cell_size
        self.cells = [[0 for _ in range(self.columns)] for _ in range(self.rows)]

    def draw(self, window):
        for row in range(self.rows):
            for column in range(self.columns):
                cell_value = self.cells[row][column]
                if cell_value == 1:
                    color = (255, 255, 255)  # Planet (white)
                elif cell_value == 2:
                    color = (160, 160, 160)  # Asteroid (gray)
                else:
                    color = (7, 7, 56)       # Empty space

                pygame.draw.rect(
                    window, color,
                    (column * self.cell_size, row * self.cell_size,
                     self.cell_size - 1, self.cell_size - 1)
                )

    def fill_random(self):
        for row in range(self.rows):
            for column in range(self.columns):
                self.cells[row][column] = random.choice([1, 0, 0, 0])

    def clear(self):
        for row in range(self.rows):
            for column in range(self.columns):
                self.cells[row][column] = 0

    def toggle_cell(self, row, column):
        if 0 <= row < self.rows and 0 <= column < self.columns:
            self.cells[row][column] = 0 if self.cells[row][column] != 0 else 1

    def is_in_red_zone(self, row, column):
        return (
            row > 0 and row < self.rows // 4 and
            column >= self.columns * 3 // 4 and column < self.columns - 1
        )

    def is_in_green_zone(self, row, column):
        return (
            row > self.rows * 3 // 4 and row < self.rows - 1 and
            column > 0 and column < self.columns // 4
        )
    
    def draw_zone_overlay(self, window):
        overlay_color = (0, 255, 255, 60)  # Neon blue with transparency
        zone_surface = pygame.Surface((self.columns * self.cell_size, self.rows * self.cell_size), pygame.SRCALPHA)

        # Red Zone: top-right quarter
        red_zone_rect = pygame.Rect(
            self.columns * 3 // 4 * self.cell_size,
            self.cell_size,  # start below top row
            (self.columns // 4 - 1) * self.cell_size,
            (self.rows // 4 - 1) * self.cell_size
        )
        pygame.draw.rect(zone_surface, overlay_color, red_zone_rect)

        # Green Zone: bottom-left quarter, excluding leftmost col and bottom row
        green_zone_rect = pygame.Rect(
            self.cell_size,  # start after first column
            self.rows * 3 // 4 * self.cell_size,
            (self.columns // 4 - 1) * self.cell_size,
            (self.rows // 4 - 1) * self.cell_size
        )
        pygame.draw.rect(zone_surface, overlay_color, green_zone_rect)

        window.blit(zone_surface, (0, 0))
