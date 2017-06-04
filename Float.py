# coding=utf-8
import sys
import pygame
import random
import pygame.gfxdraw
from pygame.locals import *
from datetime import datetime
from Player import Player

__author__ = 'David'

# initialize the pygame library
pygame.init()

# initialize fonts
game_font = pygame.font.SysFont("monospace", 12)

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
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60

GRAVITY = 0.5

player_rect = Rect(platforms[0].left, platforms[0].top - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
player = Player(player_rect, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

# setup fps
FPS = 60
clock = pygame.time.Clock()

fall_speed = 0.

# TODO Create lamp list and use "collidelist" with player to detect collisions

lamps = []

# FUNCTIONS --------------------------------------------------------------------------

def check_exit():
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_0:
                global player
                player.set_rect(Rect(platforms[0].left, platforms[0].top - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT))
                player.fall_speed = 0

# MAIN -------------------------------------------------------------------------------
while True:

    check_exit()
    player.check_input()

    clock.tick(FPS)

    # check platform and floor collision
    player.check_bottom_collisions(platforms)

    # draw everything
    pygame.display.update()
    DISPLAY_SURFACE.fill((0, 0, 0))

    for platform in platforms:
        pygame.draw.rect(DISPLAY_SURFACE, 0xaaaaaa, platform, 0)

    pygame.draw.rect(DISPLAY_SURFACE, 0xccff00, player, 0)

    # render text
    text_state = game_font.render("Player state %s" % player.state, 1, (255, 255, 0))
    text_energy = game_font.render("ENERGY: %s" % player.floating_energy, 1, (255, 255, 0))
    DISPLAY_SURFACE.blit(text_state, (3, 10))
    DISPLAY_SURFACE.blit(text_energy, (150, 10))
