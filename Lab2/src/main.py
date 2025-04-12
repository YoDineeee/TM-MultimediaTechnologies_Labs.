import pygame
import sys
from simulation import Simulation

pygame.init()

CELL_BORDER = (28, 37, 60)
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
CELL_SIZE = 10
FPS = 12

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Game of Life: Space Edition")

clock = pygame.time.Clock()
simulation = Simulation(WINDOW_WIDTH, WINDOW_HEIGHT, CELL_SIZE)

# Simulation Loop
while True:
    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            row = pos[1] // CELL_SIZE
            column = pos[0] // CELL_SIZE
            simulation.toggle_cell(row, column)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                simulation.start()
                pygame.display.set_caption("Game of Life is running")
            elif event.key == pygame.K_SPACE:
                simulation.stop()
                pygame.display.set_caption("Game of Life has stopped")
            elif event.key == pygame.K_f:
                FPS += 2
            elif event.key == pygame.K_s:
                if FPS > 5:
                    FPS -= 2
            elif event.key == pygame.K_r:
                simulation.create_random_state()
            elif event.key == pygame.K_c:
                simulation.clear()

    # Updating State
    simulation.update()

    # Drawing
    window.fill(CELL_BORDER)
    simulation.draw(window)

    pygame.display.update()
    clock.tick(FPS)