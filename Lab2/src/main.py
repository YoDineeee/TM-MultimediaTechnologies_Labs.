import pygame
import sys
from simulation import Simulation

pygame.init()

icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

CELL_BORDER = (28, 37, 60)
WINDOW_WIDTH = 720
WINDOW_HEIGHT = 720
CELL_SIZE = 15
FPS = 15

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Game of Life")

clock = pygame.time.Clock()
simulation = Simulation(WINDOW_WIDTH, WINDOW_HEIGHT, CELL_SIZE)
# At the top, before the loop
mouse_down = False

# Inside your simulation loop
while True:
    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                mouse_down = True
                pos = pygame.mouse.get_pos()
                row = pos[1] // CELL_SIZE
                column = pos[0] // CELL_SIZE
                simulation.toggle_cell(row, column)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mouse_down = False
        elif event.type == pygame.MOUSEMOTION and mouse_down:
            pos = pygame.mouse.get_pos()
            row = pos[1] // CELL_SIZE
            column = pos[0] // CELL_SIZE
            simulation.set_cell_alive(row, column)  # You'll need to implement this
        elif event.type == pygame.KEYDOWN:
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

