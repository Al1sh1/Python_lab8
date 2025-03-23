import pygame
import random
import sys

pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple Pygame Racing Game")

clock = pygame.time.Clock()

player_car_image = pygame.image.load("player_car.png")
player_car_image = pygame.transform.scale(player_car_image, (40, 70))

enemy_car_image = pygame.image.load("enemy_car.png")
enemy_car_image = pygame.transform.scale(enemy_car_image, (40, 70))

coin_image = pygame.image.load("coin.png")
coin_image = pygame.transform.scale(coin_image, (30, 30))

background_image = pygame.image.load("background.png")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.SysFont(None, 36)
font_small = pygame.font.SysFont(None, 24)

def load_high_score():
    try:
        with open("high_score.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

def save_high_score(score):
    with open("high_score.txt", "w") as file:
        file.write(str(score))

class Car:
    def __init__(self, x, y, image, speed=5):
        self.x = x
        self.y = y
        self.image = image
        self.speed = speed
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self):
        self.rect.center = (self.x, self.y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class EnemyCar(Car):
    def move(self):
        self.y += self.speed
        self.update()

class Coin:
    def __init__(self, x, y, image, speed=5):
        self.x = x
        self.y = y
        self.image = image
        self.speed = speed
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def move(self):
        self.y += self.speed
        self.rect.center = (self.x, self.y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

def spawn_enemy(enemies):
    x = random.randint(40, SCREEN_WIDTH - 40)
    y = -50
    speed = random.randint(4, 8)
    enemy = EnemyCar(x, y, enemy_car_image, speed)
    enemies.append(enemy)

def spawn_coin(coins):
    x = random.randint(30, SCREEN_WIDTH - 30)
    y = -30
    speed = random.randint(4, 8)
    coin = Coin(x, y, coin_image, speed)
    coins.append(coin)

def game_loop():
    player = Car(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 70, player_car_image, speed=0)
    player_speed_x = 0

    enemies = []
    coins = []

    enemy_timer = 0
    coin_timer = 0
    ENEMY_SPAWN_INTERVAL = 30
    COIN_SPAWN_INTERVAL = 90

    score = 0
    high_score = load_high_score() 
    running = True
    game_over = False

    global_leader_score = 0

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_speed_x = -5
                elif event.key == pygame.K_RIGHT:
                    player_speed_x = 5
                elif event.key == pygame.K_r and game_over:
                    save_high_score(high_score)  
                    return

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player_speed_x < 0:
                    player_speed_x = 0
                elif event.key == pygame.K_RIGHT and player_speed_x > 0:
                    player_speed_x = 0

        if not game_over:
            player.x += player_speed_x

            if player.x < 20:
                player.x = 20
            if player.x > SCREEN_WIDTH - 20:
                player.x = SCREEN_WIDTH - 20

            player.update()

            enemy_timer += 1
            if enemy_timer >= ENEMY_SPAWN_INTERVAL:
                spawn_enemy(enemies)
                enemy_timer = 0

            coin_timer += 1
            if coin_timer >= COIN_SPAWN_INTERVAL:
                spawn_coin(coins)
                coin_timer = 0

            for enemy in enemies:
                enemy.move()
                if enemy.y > SCREEN_HEIGHT + 50:
                    score += 1
                    enemies.remove(enemy)

                if player.rect.colliderect(enemy.rect):
                    game_over = True

            for coin in coins:
                coin.move()
                if coin.y > SCREEN_HEIGHT + 30:
                    coins.remove(coin)

                if player.rect.colliderect(coin.rect):
                    score += 5
                    coins.remove(coin)

            if score > high_score:
                high_score = score  # Update high score during the game

        else:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            restart_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 50, 100, 40)

            if pygame.mouse.get_pressed()[0]:
                if restart_button_rect.collidepoint(mouse_x, mouse_y):
                    save_high_score(high_score)  # Save high score before restarting
                    return

        screen.blit(background_image, (0, 0))

        if not game_over:
            player.draw(screen)
            for enemy in enemies:
                enemy.draw(screen)
            for coin in coins:
                coin.draw(screen)

        draw_text(f"Score: {score}", font_small, (0, 0, 0), screen, 70, 20)
        draw_text(f"High: {high_score}", font_small, (0, 0, 0), screen, 70, 50)

        if game_over:
            draw_text("GAME OVER", font, (255, 0, 0), screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30)
            draw_text(f"Score: {score}", font, (0, 0, 0), screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

            restart_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 50, 100, 40)
            pygame.draw.rect(screen, (200, 200, 200), restart_button_rect)
            draw_text("Restart", font_small, (0, 0, 0), screen, restart_button_rect.centerx, restart_button_rect.centery)

        pygame.display.flip()

def main():
    while True:
        game_loop()

if __name__ == "__main__":
    main()
