import pygame
from simulation.core import Cell

class View:
    def __init__(self, settings):
        self.settings = settings
        g = settings['grid']
        size = (g['width']*g['cell_size'], g['height']*g['cell_size'])
        pygame.display.set_caption("Liberation Day Trade War")
        self.screen = pygame.display.set_mode(size)
        self.font = pygame.font.SysFont(None, 24)

    def handle_events(self, grid, running):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                running = not running
            if e.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                gx = x // self.settings['grid']['cell_size']
                gy = y // self.settings['grid']['cell_size']
                if 0 <= gx < grid.width and 0 <= gy < grid.height:
                    c = grid.cells[gy][gx]
                    c.state = not c.state
        return running

    def draw(self, grid):
        s = self.settings
        cs = s['grid']['cell_size']
        cols = s['colors']
        self.screen.fill(pygame.Color(cols['background']))
        # draw cells
        for row in grid.cells:
            for cell in row:
                if cell.state:
                    color = cols['shipment'] if cell.zone=='export' else cols['demand']
                    rect = pygame.Rect(cell.x*cs, cell.y*cs, cs-1, cs-1)
                    pygame.draw.rect(self.screen, pygame.Color(color), rect)
        # draw grid lines
        w,h = grid.width*cs, grid.height*cs
        for x in range(0, w, cs):
            pygame.draw.line(self.screen, pygame.Color(cols['grid']), (x,0),(x,h))
        for y in range(0, h, cs):
            pygame.draw.line(self.screen, pygame.Color(cols['grid']), (0,y),(w,y))
        # generation counter
        txt = self.font.render(f"Gen: {grid.generation}", True, pygame.Color(cols['grid']))
        self.screen.blit(txt, (5,5))