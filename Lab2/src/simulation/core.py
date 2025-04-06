from simulation.tarrifs import apply_rule

class Cell:
    def __init__(self, x, y, zone):
        self.x = x
        self.y = y
        self.zone = zone      # 'export', 'import_base', 'import_recip', 'market'
        self.state = False    # alive/dead
        self.next_state = False

class Grid:
    def __init__(self, settings):
        cfg = settings["grid"]
        self.width = cfg["width"]
        self.height = cfg["height"]
        self.shock_interval = settings["simulation"]["tariff_shock_interval"]
        self.generation = 0
        self.cells = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                zone = self._determine_zone(x, y)
                row.append(Cell(x, y, zone))
            self.cells.append(row)

    def _determine_zone(self, x, y):
        third = self.width // 3
        if x < third:
            return "export"
        elif x < 2*third:
            half = self.height // 2
            return "import_base" if y < half else "import_recip"
        else:
            return "market"

    def count_neighbors(self, x, y):
        dirs = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
        cnt = 0
        for dx, dy in dirs:
            nx, ny = x+dx, y+dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if self.cells[ny][nx].state:
                    cnt += 1
        return cnt

    def step(self):
        # apply rules to compute next_state
        for row in self.cells:
            for cell in row:
                n = self.count_neighbors(cell.x, cell.y)
                cell.next_state = apply_rule(
                    cell, n, self.generation, self.shock_interval
                )
        # commit
        for row in self.cells:
            for cell in row:
                cell.state = cell.next_state
        self.generation += 1