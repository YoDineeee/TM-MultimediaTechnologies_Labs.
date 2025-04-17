import pygame
import sys
from simulation import Simulation


pygame.mixer.pre_init(44100, -16, 1, 128)  
pygame.init()


ICON_PATH    = "Lab2/src/assets/icon.png"
WINDOW_WIDTH = 1280
WINDOW_HEIGHT= 720
CELL_SIZE    = 10
FPS          = 12
CELL_BORDER  = (28, 37, 60)


icon = pygame.image.load(ICON_PATH)
pygame.display.set_icon(icon)
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Game of Life")

clock      = pygame.time.Clock()
simulation = Simulation(WINDOW_WIDTH, WINDOW_HEIGHT, CELL_SIZE)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Toggle cells by mouse when paused
        if event.type == pygame.MOUSEBUTTONDOWN:
            row, col = pygame.mouse.get_pos()[1] // CELL_SIZE, pygame.mouse.get_pos()[0] // CELL_SIZE
            simulation.toggle_cell(row, col)

        # Keyboard controls
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                simulation.start()
                pygame.display.set_caption("Game of Life is running")
            elif event.key == pygame.K_SPACE:
                simulation.stop()
                pygame.display.set_caption("Game of Life has stopped")
            elif event.key == pygame.K_f:
                FPS += 2
            elif event.key == pygame.K_s and FPS > 5:
                FPS -= 2
            elif event.key == pygame.K_r:
                simulation.create_random_state()
            elif event.key == pygame.K_c:
                simulation.clear()

    
    simulation.update()
    window.fill(CELL_BORDER)
    simulation.draw(window)
    pygame.display.update()
    clock.tick(FPS)
