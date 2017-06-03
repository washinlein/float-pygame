# coding=utf-8
import sys
import pygame
import random
import pygame.gfxdraw
from pygame.locals import *
from datetime import datetime

__author__ = 'David'

# initialize the pygame library
pygame.init()

# initialize font
game_font = pygame.font.SysFont("liberation mono", 20)

# set display mode
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600
DW_HALF = DISPLAY_WIDTH / 2
DH_HALF = DISPLAY_HEIGHT / 2
DISPLAY_AREA = DISPLAY_WIDTH * DISPLAY_HEIGHT
DISPLAY_SURFACE = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))

# initialize platforms
random.seed(datetime.now())

PLATFORM_HEIGHT = 25
platform = Rect(10, 30, 100, PLATFORM_HEIGHT)
platforms = [Rect(random.randint(0, DISPLAY_WIDTH - 100), y,
                  random.randint(100, 200), PLATFORM_HEIGHT) for y in
             range(PLATFORM_HEIGHT * 3, DISPLAY_HEIGHT - PLATFORM_HEIGHT, PLATFORM_HEIGHT * 3)]

# initialize player
PLAYER_WIDTH = 30
PLAYER_HEIGHT = 50
PLAYER_SPEED = 4

PLAYER_STATE_IDLE = 0
PLAYER_STATE_MOVE_LEFT = 1
PLAYER_STATE_MOVE_RIGHT = 2
PLAYER_STATE_FALLING = 3
PLAYER_STATE_FLOATING = 4
PLAYER_STATE_DEAD = 5

player_state_previous = PLAYER_STATE_IDLE
player_state = PLAYER_STATE_IDLE

player = Rect(platforms[0].left, platforms[0].top - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)

GRAVITY = 0.5

# setup fps
FPS = 60
clock = pygame.time.Clock()

fall_speed = 0.


# FUNCTIONS --------------------------------------------------------------------------


def check_player_input():
    global player_state
    global player_state_previous

    keys = pygame.key.get_pressed()

    player_state = PLAYER_STATE_IDLE

    if keys[pygame.K_LEFT]:

        player.left -= PLAYER_SPEED
        player_state_previous = player_state
        player_state = PLAYER_STATE_MOVE_LEFT

        if player.left < 0:
            player.left = 0
            player_state_previous = player_state
            player_state = PLAYER_STATE_IDLE

    if keys[pygame.K_RIGHT]:

        player.left += PLAYER_SPEED
        player_state_previous = player_state
        player_state = PLAYER_STATE_MOVE_RIGHT

        if player.left + PLAYER_WIDTH > DISPLAY_WIDTH:
            player.left = DISPLAY_WIDTH - PLAYER_WIDTH
            player_state_previous = player_state
            player_state = PLAYER_STATE_IDLE


def check_exit():
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_0:
                global player
                player = Rect(platforms[0].left, platforms[0].top - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
                global fall_speed
                fall_speed = 0


def check_bottom_collision():
    # floor collision
    if player.bottom + 1 >= DISPLAY_HEIGHT:
        player.bottom = DISPLAY_HEIGHT
        return True

    result = False

    for p in platforms:
        # only check near platforms
        if not (player.top > p.bottom) and p.top - player.bottom < PLATFORM_HEIGHT:
            # check if next player position will collide
            if player.bottom + fall_speed >= p.top > player.top and player.bottom + 1 < p.bottom:
                if not (player.right < p.left or player.left > p.left + p.width):
                    result = True
                    player.bottom = p.top
                break

    return result


# MAIN -------------------------------------------------------------------------------
while True:

    check_player_input()
    check_exit()

    clock.tick(FPS)

    # check bottom collision
    if check_bottom_collision():
        fall_speed = 0
    else:
        fall_speed += 1 * GRAVITY
        player_state_previous = player_state
        player_state = PLAYER_STATE_FALLING

    player.top += fall_speed

    # draw everything
    pygame.display.update()
    DISPLAY_SURFACE.fill((0, 0, 0))

    for platform in platforms:
        pygame.draw.rect(DISPLAY_SURFACE, 0xaaaaaa, platform, 0)

    pygame.draw.rect(DISPLAY_SURFACE, 0xccff00, player, 0)

    # render text
    text_state = game_font.render("Player state %s" % player_state, 1, (255, 255, 0))
    DISPLAY_SURFACE.blit(text_state, (3, 10))
