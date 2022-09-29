import pygame
import random
import math
from pygame import mixer

pygame.init()
screen = pygame.display.set_mode((800, 600))
# background = pygame.image.load("background.jpg")
# background sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# player

playerimg = pygame.image.load('player.png')
px = 365
py = 480
p_change = 0
#background image
#background = pygame.image.load('Untitled.png')
# enemy
enemyimg = []
ex = []
ey = []
e_change = []
ey_change = []
num_of_enemies = 4
for i in range(num_of_enemies):
    enemyimg.append(pygame.image.load('enemy.png'))
    ex.append(random.randint(0, 736))
    ey.append(random.randint(20, 200))
    e_change.append(0.3)
    ey_change.append(40)

bullet = pygame.image.load('bullet.png')
pygame.display.set_caption("shootergame")

by = 480
bx = 0
bullet_state = "ready"
b_change = -3
# score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 26)
scorex = 10
scorey = 10

over_font = pygame.font.Font("freesansbold.ttf", 40)


def game_over_text():
    game_over = over_font.render("GAME OVER ", True, (255, 255, 255))
    game_over2 = font.render("your score : " + str(score_value), True, (0, 0, 180))
    screen.blit(game_over, (250, 250))
    screen.blit(game_over2, (280, 300))


def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def collision(ex, ey, bx, by):
    hitbox = math.sqrt((math.pow(ex - bx, 2)) + (math.pow(ey - by, 2)))
    if hitbox < 20:
        return True
    else:
        return False


def spawn_enemy():
    ex[i] = random.randint(0, 736)
    ey[i] = random.randint(20, 200)


def player(x, y):
    screen.blit(playerimg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))


def fire(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet, (x + 22, y + 10))
    global by
    by += b_change


# Game loop
running = True
next_score = 10       # ...
basic_e_change = 0.3  # the game s tempo is decided in this 2 lines
basic_p_change = 0.5
while running:
    screen.fill((123, 63, 81))
    # background image
    #screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # TODO here u need to add speed improvement for the enemies to make the game harder over time
        if score_value > next_score:
            basic_e_change += 0.1  # create basic e change as the absolute value 3lawd l if lteht dyal borders
            basic_p_change += 0.05
            next_score = next_score + 15

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                p_change = -basic_p_change
            if event.key == pygame.K_RIGHT:
                p_change = basic_p_change
            if event.key == pygame.K_SPACE and bullet_state is "ready":
                bullet_sound = mixer.Sound("laser.wav")
                bullet_sound.play()
                bx = px
                fire(bx, by)
                by = 480
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                p_change = 0

    px += p_change
    # boundries
    if px <= 0:
        px = 0
    elif px >= 736:
        px = 736
    for i in range(num_of_enemies):
        if ey[i] > 480:
            for j in range(num_of_enemies):
                ey[j] = 2000
            game_over_text()
            break
        ex[i] += e_change[i]
        if ex[i] >= 736:
            e_change[i] = -basic_e_change
            ey[i] += ey_change[i]
        elif ex[i] <= 0:
            e_change[i] = basic_e_change
            ey[i] += ey_change[i]
        # collison events
        collison = collision(ex[i], ey[i], bx, by)
        if collison:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            by = 480
            bullet_state = "ready"
            spawn_enemy()
            score_value += 1
        enemy(ex[i], ey[i], i)
    # bullet mvt
    if bullet_state is "fire":
        fire(bx, by)
    if by <= -24:
        bullet_state = "ready"
    show_score(scorex, scorey)
    # test=100
    # for i in range(test):
    #    redanoob = font.render("malak died " + str(score_value)+" times", True, (255, 255, 255))
    #    screen.blit(redanoob,(450,10))
    player(px, py)

    pygame.display.update()