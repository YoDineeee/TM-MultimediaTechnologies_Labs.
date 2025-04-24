import pygame
import sys
from simulation import Simulation

pygame.init()
icon = pygame.image.load("Lab2/src/icon.png")
pygame.display.set_icon(icon)

# Colors
CELL_BORDER = (28, 37, 60)
UI_BACKGROUND = (40, 50, 70)
BUTTON_COLOR = (60, 80, 120)
BUTTON_HOVER_COLOR = (80, 100, 140)
BUTTON_TEXT_COLOR = (220, 220, 220)
LABEL_COLOR = (180, 180, 200)

# Window settings
WINDOW_WIDTH = 1080
WINDOW_HEIGHT = 720
UI_HEIGHT = 80
CELL_SIZE = 15
FPS = 15

# Create window with extra height for UI
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT + UI_HEIGHT))
pygame.display.set_caption("Space Game of Life")
clock = pygame.time.Clock()

# Font setup
font = pygame.font.SysFont('Arial', 18)
title_font = pygame.font.SysFont('Arial', 22, bold=True)

# Create simulation with height adjusted to account for UI panel
simulation = Simulation(WINDOW_WIDTH, WINDOW_HEIGHT, CELL_SIZE)
mouse_down = False
last_mouse_pos = None
running = False
generation = 0
target_generation = None

# Button class for UI elements
class Button:
    def __init__(self, x, y, width, height, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.hovered = False

    def draw(self, surface):
        color = BUTTON_HOVER_COLOR if self.hovered else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        pygame.draw.rect(surface, (100, 120, 160), self.rect, 2, border_radius=5)

        text_surface = font.render(self.text, True, BUTTON_TEXT_COLOR)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)
        return self.hovered

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.hovered:
                self.action()
                return True
        return False

# Text input for generation limit
class TextInput:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ''
        self.active = False

    def draw(self, surface):
        color = (100, 120, 160) if self.active else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        pygame.draw.rect(surface, (150, 180, 210), self.rect, 2, border_radius=5)

        text_surface = font.render(self.text, True, BUTTON_TEXT_COLOR)
        surface.blit(text_surface, (self.rect.x + 8, self.rect.y + 10))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
                return self.text
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.unicode.isdigit():
                self.text += event.unicode
        return None

# Create UI buttons
buttons = []

def start_simulation():
    global running
    running = True
    simulation.start()
    pygame.display.set_caption("Game of Life is running")

def stop_simulation():
    global running
    running = False
    simulation.stop()
    pygame.display.set_caption(f"Game of Life paused at Generation {generation}")

def speed_up():
    global FPS
    FPS += 2

def slow_down():
    global FPS
    if FPS > 5:
        FPS -= 2

def random_state():
    global generation, target_generation
    generation = 0
    target_generation = None
    simulation.create_random_state()

def clear_board():
    global generation, target_generation
    generation = 0
    target_generation = None
    simulation.clear()

# Define button positions and sizes
button_width = 130
button_height = 40
button_spacing = 15
ui_y = WINDOW_HEIGHT + 20

# Add buttons to the UI
buttons.append(Button(20, ui_y, button_width, button_height, "Start (Enter)", start_simulation))
buttons.append(Button(20 + button_width + button_spacing, ui_y, button_width, button_height, "Stop (Space)", stop_simulation))
buttons.append(Button(20 + (button_width + button_spacing) * 2, ui_y, button_width, button_height, "Random (R)", random_state))
buttons.append(Button(20 + (button_width + button_spacing) * 3, ui_y, button_width, button_height, "Clear (C)", clear_board))
buttons.append(Button(20 + (button_width + button_spacing) * 4, ui_y, button_width, button_height, "Speed Up (F)", speed_up))
buttons.append(Button(20 + (button_width + button_spacing) * 5, ui_y, button_width, button_height, "Slow Down (S)", slow_down))

# Input box for generation limit
input_box_x = 20 + (button_width + button_spacing) * 6
generation_input = TextInput(input_box_x, ui_y, 100, button_height)

# Main game loop
while True:
    current_mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Handle button clicks
        for button in buttons:
            button.check_hover(current_mouse_pos)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button.handle_event(event):
                    break

        # Handle input box
        result = generation_input.handle_event(event)
        if result is not None:
            try:
                target_generation = int(result)
            except ValueError:
                target_generation = None

        # Cell toggling on click
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and current_mouse_pos[1] < WINDOW_HEIGHT:
                mouse_down = True
                pos = current_mouse_pos
                row = pos[1] // CELL_SIZE
                column = pos[0] // CELL_SIZE
                simulation.toggle_cell(row, column)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mouse_down = False
                last_mouse_pos = None

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                start_simulation()
            elif event.key == pygame.K_SPACE:
                stop_simulation()
            elif event.key == pygame.K_f:
                speed_up()
            elif event.key == pygame.K_s:
                slow_down()
            elif event.key == pygame.K_r:
                random_state()
            elif event.key == pygame.K_c:
                clear_board()

    # Draw cells while dragging
    if pygame.mouse.get_pressed()[0] and current_mouse_pos[1] < WINDOW_HEIGHT:
        if last_mouse_pos:
            x1, y1 = last_mouse_pos
            x2, y2 = current_mouse_pos
            dx = x2 - x1
            dy = y2 - y1
            distance = max(abs(dx), abs(dy))
            if distance == 0:
                distance = 1
            for i in range(distance + 1):
                interp_x = int(x1 + dx * i / distance)
                interp_y = int(y1 + dy * i / distance)
                if interp_y < WINDOW_HEIGHT:
                    row = interp_y // CELL_SIZE
                    column = interp_x // CELL_SIZE
                    simulation.set_cell_alive(row, column)
        last_mouse_pos = current_mouse_pos

    # Update simulation
    if running:
        simulation.update()
        generation += 1
        if target_generation is not None and generation >= target_generation:
            stop_simulation()
            target_generation = None

    # Draw background
    window.fill(CELL_BORDER)

    # Draw simulation
    simulation.draw(window)

    # Draw UI background
    pygame.draw.rect(window, UI_BACKGROUND, (0, WINDOW_HEIGHT, WINDOW_WIDTH, UI_HEIGHT))
    pygame.draw.line(window, (60, 70, 100), (0, WINDOW_HEIGHT), (WINDOW_WIDTH, WINDOW_HEIGHT), 2)

    # Draw buttons
    for button in buttons:
        button.draw(window)

    # Draw input box
    generation_input.draw(window)
    
    # Draw generation/fps
    fps_text = font.render(f"FPS: {FPS}", True, LABEL_COLOR)
    gen_text = font.render(f"Gen: {generation}", True, LABEL_COLOR)
    window.blit(fps_text, (WINDOW_WIDTH - 75, WINDOW_HEIGHT + 40))
    window.blit(gen_text, (WINDOW_WIDTH - 75, WINDOW_HEIGHT + 20))

    # Update display
    pygame.display.update()
    clock.tick(FPS)