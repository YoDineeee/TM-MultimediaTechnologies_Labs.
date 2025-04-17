import os
import random
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

        # Load piano samples
        self.piano_notes = {}
        self.load_piano()

    def load_piano(self):
        base_dir = os.path.join(os.path.dirname(__file__), "assets/piano")
        notes = ['C4', 'C5','D4', 'E4', 'G4']
        for note in notes:
            path = os.path.join(base_dir, f"{note}.wav")
            if os.path.isfile(path):
                self.piano_notes[note] = pygame.mixer.Sound(path)
            else:
                print(f"Warning: piano sample '{note}.wav' not found in {base_dir}")

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
        return sum(1 for dr,dc in offsets
                   if cells[(row+dr) % self.rows][(col+dc) % self.columns] == 1)

    def play_piano(self, row):
    
        if not self.piano_notes:
            return
        notes = list(self.piano_notes.keys())
        idx   = row % len(notes)
        self.piano_notes[notes[idx]].play()

    def update(self):
        if not self.running:
            return

        # Reset temp grid
        for r in range(self.rows):
            for c in range(self.columns):
                self.temp_grid.cells[r][c] = 0

        # Asteroid movement phase (unchanged) …
        for r in range(self.rows):
            for c in range(self.columns):
                if self.grid.cells[r][c] != 2:
                    continue
                if self.grid.is_in_green_zone(r, c):
                    self.temp_grid.cells[r][c] = 1
                    continue
                nbrs = [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]
                random.shuffle(nbrs)
                moved = False
                for dr, dc in nbrs:
                    nr, nc = r+dr, c+dc
                    if not (0 <= nr < self.rows and 0 <= nc < self.columns):
                        nr, nc = r-dr, c-dc
                    if 0 <= nr < self.rows and 0 <= nc < self.columns:
                        if self.grid.is_in_green_zone(nr, nc):
                            self.temp_grid.cells[nr][nc] = 1
                        else:
                            self.temp_grid.cells[nr][nc] = 2
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
                n        = self.count_live_neighbors(self.grid.cells, r, c)

                if val == 1:
                    # Survival rules
                    if n < 2 or n > 3:
                        self.temp_grid.cells[r][c] = 0
                    else:
                        self.temp_grid.cells[r][c] = 2 if in_red else 1
                else:
                    # Birth
                    if n == 3:
                        self.temp_grid.cells[r][c] = 1
                        births.append((r, c))

        # Commit new state
        for r in range(self.rows):
            for c in range(self.columns):
                self.grid.cells[r][c] = self.temp_grid.cells[r][c]

        # Play piano notes for each birth
        for (r, c) in births:
            self.play_piano(r)

    def draw(self, window):
        self.grid.draw(window)
        self.grid.draw_zone_overlay(window)
