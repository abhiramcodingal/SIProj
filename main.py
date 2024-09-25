# Importing modules
import pygame
import random
import math

# Initializing the pygame
pygame.init()

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

# Control variable
done = False

# Creating the screen
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

# Loading images
bg = pygame.image.load("background.png")
icon = pygame.image.load("ufo.png")
player_img = pygame.image.load("player.png")
enemy_img = pygame.image.load("enemy.png")
bullet_img = pygame.image.load("bullet.png")

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
num_of_enemies = 7

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

while not done:
    clock = pygame.time.Clock()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    screen.blit(bg, (0, 0))
    pygame.display.flip()
    clock.tick(90)
pygame.quit()