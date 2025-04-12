from grid import Grid
import random

class Simulation:
    def __init__(self, width, height, cell_size):
        self.grid = Grid(width, height, cell_size)
        self.temp_grid = Grid(width, height, cell_size)
        self.rows = height // cell_size
        self.columns = width // cell_size
        self.run = False

    def draw(self, window):
        self.grid.draw(window)

    def is_running(self):
        return self.run

    def start(self):
        self.run = True

    def stop(self):
        self.run = False

    def clear(self):
        if not self.is_running():
            self.grid.clear()

    def create_random_state(self):
        if not self.is_running():
            self.grid.fill_random()

    def toggle_cell(self, row, column):
        if not self.is_running():
            self.grid.toggle_cell(row, column)

    def count_live_neighbors(self, grid, row, column, kind=1):
        count = 0
        neighbor_offsets = [(-1, -1), (-1, 0), (-1, 1),
                            (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for offset in neighbor_offsets:
            new_row = (row + offset[0]) % self.rows
            new_col = (column + offset[1]) % self.columns
            if grid.cells[new_row][new_col] == kind:
                count += 1
        return count

    def get_neighbors(self, row, col):
        offsets = [(-1, -1), (-1, 0), (-1, 1),
                   (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        return [((row + dr) % self.rows, (col + dc) % self.columns) for dr, dc in offsets]

    def update(self):
        if not self.is_running():
            return

        # Clear temp grid
        for row in range(self.rows):
            for col in range(self.columns):
                self.temp_grid.cells[row][col] = 0

                # ASTEROID MOVEMENT PHASE
        for row in range(self.rows):
            for col in range(self.columns):
                if self.grid.cells[row][col] == 2:
                    # Green zone check
                    if self.grid.is_in_green_zone(row, col):
                        self.temp_grid.cells[row][col] = 1
                        continue

                    neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1),
                                 (-1, -1), (-1, 1), (1, -1), (1, 1)]
                    random.shuffle(neighbors)
                    moved = False

                    for dr, dc in neighbors:
                        n_row = row + dr
                        n_col = col + dc

                        # If it's out of bounds
                        if not (0 <= n_row < self.rows and 0 <= n_col < self.columns):
                            # Try opposite direction
                            bounce_row = row - dr
                            bounce_col = col - dc
                            if 0 <= bounce_row < self.rows and 0 <= bounce_col < self.columns:
                                if self.grid.is_in_green_zone(bounce_row, bounce_col):
                                    self.temp_grid.cells[bounce_row][bounce_col] = 1
                                    moved = True
                                    break
                                elif self.grid.cells[bounce_row][bounce_col] == 1:
                                    self.temp_grid.cells[bounce_row][bounce_col] = 2
                                    moved = True
                                    break
                                elif self.grid.cells[bounce_row][bounce_col] == 0 and not moved:
                                    self.temp_grid.cells[bounce_row][bounce_col] = 2
                                    moved = True
                        else:
                            if self.grid.is_in_green_zone(n_row, n_col):
                                self.temp_grid.cells[n_row][n_col] = 1
                                moved = True
                                break
                            elif self.grid.cells[n_row][n_col] == 1:
                                self.temp_grid.cells[n_row][n_col] = 2
                                moved = True
                                break
                            elif self.grid.cells[n_row][n_col] == 0 and not moved:
                                self.temp_grid.cells[n_row][n_col] = 2
                                moved = True

                    if not moved:
                        self.temp_grid.cells[row][col] = 2

        # GAME OF LIFE PHASE
        for row in range(self.rows):
            for col in range(self.columns):
                # Skip asteroid-handled cells
                if self.temp_grid.cells[row][col] != 0:
                    continue

                current_value = self.grid.cells[row][col]
                in_green_zone = self.grid.is_in_green_zone(row, col)
                in_red_zone = self.grid.is_in_red_zone(row, col)

                if current_value == 1:
                    live_neighbors = self.count_live_neighbors(self.grid, row, col, 1)

                    if in_red_zone and live_neighbors >= 2:
                        self.temp_grid.cells[row][col] = 2
                    elif live_neighbors < 2:
                        self.temp_grid.cells[row][col] = 0
                    elif in_green_zone and live_neighbors > 6:
                        self.temp_grid.cells[row][col] = 0
                    elif not in_green_zone and live_neighbors > 3:
                        self.temp_grid.cells[row][col] = 0
                    else:
                        self.temp_grid.cells[row][col] = 1

                elif current_value == 0:
                    live_neighbors = self.count_live_neighbors(self.grid, row, col, 1)
                    if live_neighbors == 3:
                        self.temp_grid.cells[row][col] = 1

        # Copy temp back to main grid
        for row in range(self.rows):
            for col in range(self.columns):
                self.grid.cells[row][col] = self.temp_grid.cells[row][col]