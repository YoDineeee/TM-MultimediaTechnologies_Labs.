import random
import pygame
import numpy as np
from grid import Grid

class Simulation:
    def __init__(self, width, height, cell_size):
        self.grid = Grid(width, height, cell_size)
        self.temp_grid = Grid(width, height, cell_size)
        self.rows = height // cell_size
        self.columns = width // cell_size
        self.running = False

        # Audio setup
        self.sample_rate = 44100
        self._tone_cache = {}

    def is_running(self):
        return self.running

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def clear(self):
        if not self.running:
            self.grid.clear()

    def create_random_state(self):
        if not self.running:
            self.grid.fill_random()

    def toggle_cell(self, row, column):
        if not self.running:
            self.grid.toggle_cell(row, column)

    def set_cell_alive(self, row, col):
        self.grid.set_cell(row, col, 1)

    def count_live_neighbors(self, cells, row, col):
        offsets = [(-1, -1), (-1, 0), (-1, 1),
                   (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        count = 0
        for dr, dc in offsets:
            r = (row + dr) % self.rows
            c = (col + dc) % self.columns
            if cells[r][c] == 1:
                count += 1
        return count

    def _get_tone(self, freq, duration=0.12, kind='sine'):
        key = (freq, duration, kind)
        if key in self._tone_cache:
            return self._tone_cache[key]

        length = int(self.sample_rate * duration)
        t = np.linspace(0, duration, length, False)
        if kind == 'sine':
            wave = 0.2 * np.sin(2 * np.pi * freq * t)
        else:
            wave = 0.2 * np.sign(np.sin(2 * np.pi * freq * t))

        audio = np.int16(wave * 32767)
        audio_stereo = np.column_stack((audio, audio))
        sound = pygame.sndarray.make_sound(audio_stereo)
        self._tone_cache[key] = sound
        return sound

    def update(self):
        if not self.running:
            return

        births = []

        # Clear temp grid
        for row in range(self.rows):
            for col in range(self.columns):
                self.temp_grid.cells[row][col] = 0

        # Asteroid movement
        for r in range(self.rows):
            for c in range(self.columns):
                if self.grid.cells[r][c] != 2:
                    continue

                if self.grid.is_in_green_zone(r, c):
                    self.temp_grid.cells[r][c] = 1
                    continue

                neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1),
                             (-1, -1), (-1, 1), (1, -1), (1, 1)]
                random.shuffle(neighbors)
                moved = False

                for dr, dc in neighbors:
                    nr, nc = r + dr, c + dc
                    if not (0 <= nr < self.rows and 0 <= nc < self.columns):
                        # Bounce
                        nr, nc = r - dr, c - dc

                    if 0 <= nr < self.rows and 0 <= nc < self.columns:
                        if self.grid.is_in_green_zone(nr, nc):
                            self.temp_grid.cells[nr][nc] = 1
                            moved = True
                            break
                        elif self.grid.cells[nr][nc] == 1:
                            self.temp_grid.cells[nr][nc] = 2
                            moved = True
                            break
                        elif self.grid.cells[nr][nc] == 0 and not moved:
                            self.temp_grid.cells[nr][nc] = 2
                            moved = True

                if not moved:
                    self.temp_grid.cells[r][c] = 2

        # Game of Life logic with birth detection
        for r in range(self.rows):
            for c in range(self.columns):
                if self.temp_grid.cells[r][c] != 0:
                    continue

                val = self.grid.cells[r][c]
                in_red = self.grid.is_in_red_zone(r, c)
                in_green = self.grid.is_in_green_zone(r, c)
                live_n = self.count_live_neighbors(self.grid.cells, r, c)

                if val == 1:
                    # Planet survival
                    if live_n < 2 or (not in_green and live_n > 3) or (in_green and live_n > 6):
                        self.temp_grid.cells[r][c] = 0
                    else:
                        if in_red and live_n >= 2:
                            self.temp_grid.cells[r][c] = 2
                        else:
                            self.temp_grid.cells[r][c] = 1
                else:
                    # Birth
                    if live_n == 3 or (in_green and live_n == 4):
                        self.temp_grid.cells[r][c] = 1
                        births.append((r, c))

        # Commit the new state
        for r in range(self.rows):
            for c in range(self.columns):
                self.grid.cells[r][c] = self.temp_grid.cells[r][c]

        # Sonify births
        for r, c in births:
            freq = 200 + (r / self.rows) * 1000  # map row to frequency
            tone = self._get_tone(freq)
            tone.play()

    def draw(self, window):
        self.grid.draw(window, self.running)
        self.grid.draw_zone_overlay(window)