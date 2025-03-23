import pygame
import sys


pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
DRAW_MODE = 'rectangle'  # По упол, тік төрт бұрыш
current_color = (0, 0, 0)  # Цвет черный

# Цветтер
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
colors = [RED, GREEN, BLUE, YELLOW, ORANGE]

# Настройка экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Drawing Program")

clock = pygame.time.Clock()


font = pygame.font.SysFont('Arial', 24)


drawing_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
drawing_surface.fill(WHITE)  

# -------------------
# Функций
# -------------------
def draw_button(color, x, y, width, height, label):
    pygame.draw.rect(screen, color, (x, y, width, height))
    text = font.render(label, True, (0, 0, 0))
    screen.blit(text, (x + 10, y + 10))

def draw_shape(shape, x, y, color, radius=0, width=0, height=0):
    
    if shape == 'rectangle':
        pygame.draw.rect(drawing_surface, color, (x, y, width, height))
    elif shape == 'circle':
        pygame.draw.circle(drawing_surface, color, (x, y), radius)

def game_loop():
    
    global DRAW_MODE, current_color
    drawing = False
    last_pos = None  
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Использование мышки
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # проверка когда мышка работает
                if event.button == 1:
                    if 10 <= mouse_x <= 110 and 10 <= mouse_y <= 50:
                        current_color = RED
                    elif 120 <= mouse_x <= 220 and 10 <= mouse_y <= 50:
                        current_color = GREEN
                    elif 230 <= mouse_x <= 330 and 10 <= mouse_y <= 50:
                        current_color = BLUE
                    elif 340 <= mouse_x <= 440 and 10 <= mouse_y <= 50:
                        current_color = YELLOW
                    elif 450 <= mouse_x <= 550 and 10 <= mouse_y <= 50:
                        current_color = ORANGE
                    elif 560 <= mouse_x <= 660 and 10 <= mouse_y <= 50:
                        DRAW_MODE = 'erase'
                    elif 670 <= mouse_x <= 770 and 10 <= mouse_y <= 50:
                        DRAW_MODE = 'rectangle'
                    elif 670 <= mouse_x <= 770 and 60 <= mouse_y <= 100:
                        DRAW_MODE = 'circle'
                    elif 670 <= mouse_x <= 770 and 110 <= mouse_y <= 150:
                        DRAW_MODE = 'pencil'  
                    else:
                        drawing = True
                        last_pos = mouse_x, mouse_y

            # НЕ использование мышки
            if event.type == pygame.MOUSEBUTTONUP:
                drawing = False
                last_pos = None

            # Движение мышки
            if event.type == pygame.MOUSEMOTION:
                if drawing:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if DRAW_MODE == 'rectangle':
                        rect_width = mouse_x - last_pos[0]
                        rect_height = mouse_y - last_pos[1]
                        draw_shape(DRAW_MODE, last_pos[0], last_pos[1], current_color, width=rect_width, height=rect_height)
                    elif DRAW_MODE == 'circle':
                        radius = int(((mouse_x - last_pos[0])**2 + (mouse_y - last_pos[1])**2)**0.5)
                        draw_shape(DRAW_MODE, last_pos[0], last_pos[1], current_color, radius=radius)
                    elif DRAW_MODE == 'erase':
                        pygame.draw.circle(drawing_surface, WHITE, (mouse_x, mouse_y), 10)  # 10 пх
                    elif DRAW_MODE == 'pencil':
                        if last_pos:
                            pygame.draw.line(drawing_surface, current_color, last_pos, (mouse_x, mouse_y), 3)  # 3 пх
                        last_pos = mouse_x, mouse_y

        screen.fill(WHITE)

        screen.blit(drawing_surface, (0, 0))

        # Кнопки
        draw_button(RED, 10, 10, 100, 40, 'Red')
        draw_button(GREEN, 120, 10, 100, 40, 'Green')
        draw_button(BLUE, 230, 10, 100, 40, 'Blue')
        draw_button(YELLOW, 340, 10, 100, 40, 'Yellow')
        draw_button(ORANGE, 450, 10, 100, 40, 'Orange')

        draw_button(WHITE, 560, 10, 100, 40, 'Erase')
        draw_button(GRAY, 670, 10, 100, 40, 'Rectangle')
        draw_button((100, 100, 255), 670, 60, 100, 40, 'Circle')
        draw_button(BLUE, 670, 110, 100, 40, 'Pencil')

        pygame.display.update()
        clock.tick(FPS)

# -------------------
# Начать 
# -------------------
if __name__ == "__main__":
    game_loop()
