import pygame
import random

# Initialize pygame
pygame.init()

# Game Window
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🚀 Space Invaders")

# Load Background
background = pygame.image.load("background.jpg")

# Load Sounds
pygame.mixer.init()
pygame.mixer.music.load("background.wav")
pygame.mixer.music.play(-1)  # Loop music
bullet_sound = pygame.mixer.Sound("laser.wav")
explosion_sound = pygame.mixer.Sound("explosion.wav")

# Colors
WHITE = (255, 255, 255)

# Load Images
player_img = pygame.image.load("player.jpg")
enemy_img = pygame.image.load("enemy.jpg")
bullet_img = pygame.image.load("bullet.jpg")

# Player
player_x = WIDTH // 2 - 32
player_y = HEIGHT - 80
player_speed = 5

# Multiple Enemies
num_enemies = 6
enemies = []
for _ in range(num_enemies):
    enemies.append({
        "x": random.randint(50, WIDTH - 50),
        "y": random.randint(50, 150),
        "speed_x": 3,
        "speed_y": 40
    })

# Bullet
bullet_x = 0
bullet_y = player_y
bullet_speed = 7
bullet_state = "ready"  # "ready" means bullet not visible

# Score
score = 0
font = pygame.font.Font(None, 36)

# Game Over
game_over = False

# Game Loop
running = True
while running:
    screen.fill(WHITE)
    screen.blit(background, (0, 0))

    # Show Score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Player Controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - 64:
        player_x += player_speed
    if keys[pygame.K_SPACE] and bullet_state == "ready":
        bullet_x = player_x
        bullet_y = player_y
        bullet_state = "fire"
        bullet_sound.play()

    # Bullet Movement
    if bullet_state == "fire":
        screen.blit(bullet_img, (bullet_x + 16, bullet_y))
        bullet_y -= bullet_speed
        if bullet_y < 0:
            bullet_state = "ready"

    # Enemy Movement
    for enemy in enemies:
        enemy["x"] += enemy["speed_x"]
        if enemy["x"] <= 0 or enemy["x"] >= WIDTH - 64:
            enemy["speed_x"] *= -1
            enemy["y"] += enemy["speed_y"]

        # Collision Detection
        if bullet_state == "fire" and enemy["y"] < bullet_y < enemy["y"] + 64 and enemy["x"] < bullet_x < enemy["x"] + 64:
            explosion_sound.play()
            bullet_state = "ready"
            enemy["x"] = random.randint(50, WIDTH - 50)
            enemy["y"] = random.randint(50, 150)
            score += 10  # Increase Score

        # Draw Enemy
        screen.blit(enemy_img, (enemy["x"], enemy["y"]))

        # Check if Enemy Reached Bottom
        if enemy["y"] > HEIGHT - 100:
            game_over = True

    # Draw Player
    screen.blit(player_img, (player_x, player_y))

    # Game Over Condition
    if game_over:
        game_over_text = font.render("GAME OVER!", True, (255, 0, 0))
        screen.blit(game_over_text, (WIDTH // 2 - 80, HEIGHT // 2))
        pygame.mixer.music.stop()
        pygame.display.update()
        pygame.time.delay(3000)
        running = False

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

pygame.quit()
