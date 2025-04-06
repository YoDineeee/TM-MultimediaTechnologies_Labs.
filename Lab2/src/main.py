import pygame
import toml
from simulation.core import Grid
from simulation.view import View


def load_settings():
    return toml.load("src/config/settings.toml")


def main():
    settings = load_settings()
    pygame.init()
    view = View(settings)
    grid = Grid(settings)
    clock = pygame.time.Clock()
    running = False

    while True:
        running = view.handle_events(grid, running)
        if running:
            grid.step()
        view.draw(grid)
        pygame.display.flip()
        clock.tick(settings["simulation"]["fps"])


if __name__ == "__main__":
    main()