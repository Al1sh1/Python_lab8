import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# -------------------
# Global Configuration
# -------------------
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
FPS = 30

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake")

# Snake properties
SNAKE_SIZE = 10
SNAKE_SPEED = 10

# Initialize clock
clock = pygame.time.Clock()

# Font for displaying score and level
font = pygame.font.SysFont("Comicsans", 24)
font_small = pygame.font.SysFont("Comicsans", 16)  # Smaller font for instructions

# -------------------
# Functions
# -------------------
def draw_text(text, font, color, surface, x, y):
    """Helper function to draw text on the screen"""
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

def generate_food(snake_body):
    """Generate a random food position that does not overlap with snake"""
    food_x = random.randint(0, (SCREEN_WIDTH - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
    food_y = random.randint(0, (SCREEN_HEIGHT - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
    while (food_x, food_y) in snake_body:  # Avoid food on the snake
        food_x = random.randint(0, (SCREEN_WIDTH - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
        food_y = random.randint(0, (SCREEN_HEIGHT - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
    return food_x, food_y

def game_loop():
    """Main game loop"""
    # Initial snake position and body
    snake_x = SCREEN_WIDTH // 2
    snake_y = SCREEN_HEIGHT // 2
    snake_body = [(snake_x, snake_y)]
    snake_direction = "RIGHT"

    # Food position
    food_x, food_y = generate_food(snake_body)

    # Game variables
    score = 0
    level = 1
    speed = SNAKE_SPEED
    running = True

    while running:
        clock.tick(speed)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and snake_direction != "RIGHT":
                    snake_direction = "LEFT"
                elif event.key == pygame.K_RIGHT and snake_direction != "LEFT":
                    snake_direction = "RIGHT"
                elif event.key == pygame.K_UP and snake_direction != "DOWN":
                    snake_direction = "UP"
                elif event.key == pygame.K_DOWN and snake_direction != "UP":
                    snake_direction = "DOWN"

        # Move the snake
        if snake_direction == "LEFT":
            snake_x -= SNAKE_SIZE
        elif snake_direction == "RIGHT":
            snake_x += SNAKE_SIZE
        elif snake_direction == "UP":
            snake_y -= SNAKE_SIZE
        elif snake_direction == "DOWN":
            snake_y += SNAKE_SIZE

        # Add new head to snake body
        new_head = (snake_x, snake_y)
        snake_body.insert(0, new_head)

        # Check for food collision
        if snake_x == food_x and snake_y == food_y:
            score += 1
            if score % 3 == 0:  # Increase level every 3 food items
                level += 1
                speed += 3  # Increase speed when level increases
            food_x, food_y = generate_food(snake_body)  # Generate new food
        else:
            snake_body.pop()  # Remove the tail if no food eaten

        # Check for wall collision
        if snake_x < 0 or snake_x >= SCREEN_WIDTH or snake_y < 0 or snake_y >= SCREEN_HEIGHT:
            running = False

        # Check for self collision
        if (snake_x, snake_y) in snake_body[1:]:
            running = False

        # Drawing
        screen.fill(BLACK)

        # Draw snake
        for segment in snake_body:
            pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE))

        # Draw food
        pygame.draw.rect(screen, RED, pygame.Rect(food_x, food_y, SNAKE_SIZE, SNAKE_SIZE))

        # Draw score and level
        draw_text(f"Score: {score}", font, WHITE, screen, 70, 20)
        draw_text(f"Level: {level}", font, WHITE, screen, SCREEN_WIDTH - 70, 20)

        pygame.display.update()

    # Game Over screen
    screen.fill(BLACK)
    draw_text("GAME OVER", font, RED, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
    draw_text(f"Final Score: {score}", font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    draw_text("Press Q to Quit or R to Restart", font_small, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.5)
    pygame.display.update()

    # Wait for restart or quit
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_r:
                    game_loop()  # Restart the game

# -------------------
# Start the Game
# -------------------
if __name__ == "__main__":
    game_loop()
