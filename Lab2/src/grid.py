import pygame
import random

class Grid:
    def __init__(self, width, height, cell_size):
        self.rows      = height // cell_size
        self.columns   = width  // cell_size
        self.cell_size = cell_size
       
        self.cells     = [[0 for _ in range(self.columns)] for _ in range(self.rows)]

    def draw(self, window):
        for r in range(self.rows):
            for c in range(self.columns):
                val = self.cells[r][c]
                if val == 1:
                    color = (255, 255, 255)  
                elif val == 2:
                    color = (160, 160, 160)  
                else:
                    color = (7, 7, 56)       

                pygame.draw.rect(
                    window, color,
                    (c * self.cell_size, r * self.cell_size,
                     self.cell_size - 1, self.cell_size - 1)
                )

    def fill_random(self):
        for r in range(self.rows):
            for c in range(self.columns):
                self.cells[r][c] = random.choice([1, 0, 0, 0])

    def clear(self):
        for r in range(self.rows):
            for c in range(self.columns):
                self.cells[r][c] = 0

    def toggle_cell(self, row, column):
        if 0 <= row < self.rows and 0 <= column < self.columns:
            self.cells[row][column] = 0 if self.cells[row][column] != 0 else 1

    def is_in_red_zone(self, row, column):
        return (
            0 < row < self.rows // 4 and
            self.columns * 3 // 4 <= column < self.columns - 1
        )

    def is_in_green_zone(self, row, column):
        return (
            self.rows * 3 // 4 < row < self.rows - 1 and
            0 < column < self.columns // 4
        )

    def draw_zone_overlay(self, window):
        zone_surf = pygame.Surface(
            (self.columns * self.cell_size, self.rows * self.cell_size),
            pygame.SRCALPHA
        )
        glow_fill   = (0, 255, 255, 30)
        glow_border = (0, 255, 255, 120)

       
        rx = (self.columns * 3 // 4) * self.cell_size
        ry = self.cell_size
        rw = (self.columns // 4 - 1) * self.cell_size
        rh = (self.rows    // 4 - 1) * self.cell_size
        red_rect = pygame.Rect(rx, ry, rw, rh)
        pygame.draw.rect(zone_surf, glow_fill, red_rect)
        pygame.draw.rect(zone_surf, glow_border, red_rect, width=2)

       
        gx = self.cell_size
        gy = (self.rows * 3 // 4) * self.cell_size
        gw = (self.columns // 4 - 1) * self.cell_size
        gh = (self.rows    // 4 - 1) * self.cell_size
        green_rect = pygame.Rect(gx, gy, gw, gh)
        pygame.draw.rect(zone_surf, glow_fill, green_rect)
        pygame.draw.rect(zone_surf, glow_border, green_rect, width=2)

        window.blit(zone_surf, (0, 0))
