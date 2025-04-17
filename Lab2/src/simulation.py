import random
import numpy as np
import pygame
from grid import Grid

class Simulation:
    def __init__(self, width, height, cell_size):
        # Grid setup
        self.grid      = Grid(width, height, cell_size)
        self.temp_grid = Grid(width, height, cell_size)
        self.rows      = height // cell_size
        self.columns   = width  // cell_size
        self.running   = False

        # Audio setup (must match pre_init in main.py)
        self.sample_rate = 44100
        self._tone_cache = {}

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

    def count_live_neighbors(self, cells, row, col):
        offsets = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
        count = 0
        for dr, dc in offsets:
            nr, nc = (row + dr) % self.rows, (col + dc) % self.columns
            if cells[nr][nc] == 1:
                count += 1
        return count

    def _get_tone(self, freq, duration=0.12, kind='sine'):
        """Generate or retrieve a short Sound of given freq/duration."""
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
        sound = pygame.sndarray.make_sound(audio)
        self._tone_cache[key] = sound
        return sound

    def update(self):
        if not self.running:
            return

        # Prepare temp grid
        for r in range(self.rows):
            for c in range(self.columns):
                self.temp_grid.cells[r][c] = 0

        # Asteroid movement phase
        for r in range(self.rows):
            for c in range(self.columns):
                if self.grid.cells[r][c] != 2:
                    continue
                # If in green zone, revert to planet immediately
                if self.grid.is_in_green_zone(r, c):
                    self.temp_grid.cells[r][c] = 1
                    continue

                # Try to move/bounce
                nbrs = [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]
                random.shuffle(nbrs)
                moved = False
                for dr, dc in nbrs:
                    nr, nc = r + dr, c + dc
                    if not (0 <= nr < self.rows and 0 <= nc < self.columns):
                        # bounce
                        br, bc = r - dr, c - dc
                        nr, nc = br, bc
                    if 0 <= nr < self.rows and 0 <= nc < self.columns:
                        if self.grid.is_in_green_zone(nr, nc):
                            self.temp_grid.cells[nr][nc] = 1
                        elif self.grid.cells[nr][nc] in (0,1):
                            self.temp_grid.cells[nr][nc] = (
                                2 if self.grid.cells[nr][nc] == 0 else 2
                            )
                        moved = True
                        break
                if not moved:
                    self.temp_grid.cells[r][c] = 2

        # Game of Life phase + birth detection
        births = []
        for r in range(self.rows):
            for c in range(self.columns):
                if self.temp_grid.cells[r][c] != 0:
                    continue

                val = self.grid.cells[r][c]
                in_red   = self.grid.is_in_red_zone(r, c)
                in_green = self.grid.is_in_green_zone(r, c)
                live_n   = self.count_live_neighbors(self.grid.cells, r, c)

                if val == 1:
                    # Survival
                    if live_n < 2 or live_n > 3:
                        self.temp_grid.cells[r][c] = 0
                    else:
                        # Born/survive in red ⇒ asteroid
                        if in_red:
                            self.temp_grid.cells[r][c] = 2
                        else:
                            self.temp_grid.cells[r][c] = 1
                else:
                    # Birth
                    if live_n == 3:
                        self.temp_grid.cells[r][c] = 1
                        births.append((r, c))

        # Commit new state
        for r in range(self.rows):
            for c in range(self.columns):
                self.grid.cells[r][c] = self.temp_grid.cells[r][c]

        # Sonify births
        for (r, c) in births:
            freq = 200 + (r / self.rows) * 1000  # map row → 200–1200 Hz
            tone = self._get_tone(freq, duration=0.1, kind='sine')
            tone.play()

    def draw(self, window):
        self.grid.draw(window)
        self.grid.draw_zone_overlay(window)
