# Importing modules
import pygame
import random
import math
import winsound

# Initializing the pygame and mixer
pygame.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
PLAYER_START_X = 370
PLAYER_START_Y = 380
ENEMY_START_Y_MIN = 50
ENEMY_START_Y_MAX = 150
ENEMY_SPEED_X = 4
ENEMY_SPEED_Y = 40
BULLET_SPEED_Y = 10
COLLISION_DISTANCE = 27
BLACK = pygame.Color(0,0,0)

# Control variable
done = False

# Creating the screen
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

# Loading imagespygame.mixer.Sound
bg = pygame.image.load("background.png")
icon = pygame.image.load("ufo.png")
player_img = pygame.image.load("player.png")
enemy_img = pygame.image.load("enemy.png")
bullet_img = pygame.image.load("bullet.png")

# Loading sound(s)
bullmus = pygame.mixer.Sound("bullmus.wav")
gameover = pygame.mixer.Sound("gameover.wav")

# Setting caption and icon
pygame.display.set_caption("Space Invader")
pygame.display.set_icon(icon)

# Player x, y, x_change
player_x = PLAYER_START_X
player_y = PLAYER_START_Y
player_x_change = 0
def player(x, y):
    screen.blit(player_img, (x, y))

# Enemy track lists and number of enemies
enemy_image = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_of_enemies = 6

# Creating enemies
for _i in range(num_of_enemies):
    enemy_image.append(enemy_img)
    enemy_x.append(random.randint(0, SCREEN_WIDTH - 64))
    enemy_y.append(random.randint(ENEMY_START_Y_MIN, ENEMY_START_Y_MAX))
    enemy_x_change.append(ENEMY_SPEED_X)
    enemy_y_change.append(ENEMY_SPEED_Y)
def enemy(x, y, i):
    screen.blit(enemy_image[i], (x, y))

# Creating bullet
bullet_x = 0
bullet_y = PLAYER_START_Y
bullet_x_change = 0
bullet_y_change = BULLET_SPEED_Y
bullet_state = "ready"
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y + 10))

# Score text & function
score = 0
score_font = pygame.font.Font("freesansbold.ttf", 35)
txt_x = 10
txt_y = 10
def show_score(x, y):
    display_score = score_font.render("Score : " + str(score), True, (255,255,0))
    screen.blit(display_score, (x, y))

# Game over text & function
gameover_font = pygame.font.Font("freesansbold.ttf", 65)
def show_gameover(x, y):
    display_gameover = gameover_font.render("GAME OVER", True, (0,255,0))
    screen.blit(display_gameover, (x, y))

# Collision function
def isCollided(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((enemy_x - bullet_x) ** 2 + (enemy_y - bullet_y) ** 2)
    return distance < COLLISION_DISTANCE

# Game loop
while not done:
    # Configuring clock
    clock = pygame.time.Clock()
    
    # Screen configuring
    screen.fill(BLACK)
    screen.blit(bg, (0, 0))
    key = pygame.key.get_pressed()
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -5
            if event.key == pygame.K_RIGHT:
                player_x_change = 5
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                bullet_x = player_x
                fire_bullet(bullet_x, bullet_y)
            if event.type == pygame.KEYUP and event.key in [pygame.K_LEFT,pygame.K_RIGHT]:
                player_x_change = 0
    
    # Player movement
    player_x += player_x_change
    player_x = max(min(player_x, SCREEN_WIDTH - 64), 0)

    # Enemy movement
    for i in range(num_of_enemies):
        if enemy_y[i] > 340:
            for j in range(num_of_enemies):
                enemy_y[j] = 2000
            show_gameover(200, 250)
            pygame.mixer.Sound.play(gameover)
            break
        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 0 or enemy_x[i] >= SCREEN_WIDTH - 64:
            enemy_x_change[i] *= -1
            enemy_y[i] += enemy_y_change[i]
        if isCollided(enemy_x[i], enemy_y[i], bullet_x, bullet_y):
            bullet_y = PLAYER_START_Y
            bullet_state = "ready"
            score += 1
            pygame.mixer.Sound.play(bullmus)
            enemy_x[i] = random.randint(0, SCREEN_WIDTH - 64)
            enemy_y[i] = random.randint(ENEMY_START_Y_MIN, ENEMY_START_Y_MAX)
        enemy(enemy_x[i], enemy_y[i], i)

    # Bullet movement
    if bullet_y <= 0:
        bullet_y = PLAYER_START_Y
        bullet_state = "ready"
    elif bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change
    
    # Drawing player
    player(player_x, player_y)

    # Showing score
    show_score(10, 10)

    # Updating
    pygame.display.flip()

# Quitting pygame
pygame.quit()