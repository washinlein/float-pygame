# coding=utf-8
import sys

import pygame
import pygame.gfxdraw
from pygame.locals import *

import tilerenderer
from player import Player

__author__ = 'David'

# initialize the pygame libraries
# sound first to avoid playback delay
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

# prepare room and platforms
tile_renderer = tilerenderer.TileRenderer("./assets/tmx/platforms_test.tmx")
room_surface = pygame.Surface(tile_renderer.size)
platforms = tile_renderer.get_platform_rects()

# initialize player
PLAYER_WIDTH = 30
PLAYER_HEIGHT = 50

# prepare room surface
tile_renderer.render_map(room_surface)

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
            # reset room
            if event.key == K_0:
                reset_room()


def reset_room():
    global player
    global lamps
    player.set_rect(Rect(platforms[0].left, platforms[0].top - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT))
    player.fall_speed = 0
    player.reset_energy()
    lamps = list(tile_renderer.get_lamps())

# MAIN -------------------------------------------------------------------------------------
lamps = list(tile_renderer.get_lamps())

while True:
    # UPDATE -------------------------------------------------------------------------------
    check_exit()
    player.check_input()

    clock.tick(FPS)

    # check collision against platforms and floor
    player.check_platform_collisions(platforms)

    # check collisions against lamps
    for lamp in lamps:
        if player.rect.colliderect(lamp):
            print("LAMP COLLISION!")
            lamps.remove(lamp)

    # RENDER -------------------------------------------------------------------------------
    pygame.display.update()

    # draw Tiled map
    DISPLAY_SURFACE.blit(room_surface, (0, 0))

    # draw lamps
    for lamp in lamps:
        DISPLAY_SURFACE.blit(lamp.surface, lamp.rect)

    # draw player
    DISPLAY_SURFACE.blit(player.surface, (player.rect.left, player.rect.top))

    # render text
    text_state = game_font.render("Player state %s" % player.state, 1, (255, 255, 0))
    text_energy = game_font.render("ENERGY: %s" % player.floating_energy, 1, (255, 255, 0))
    DISPLAY_SURFACE.blit(text_state, (3, 10))
    DISPLAY_SURFACE.blit(text_energy, (150, 10))
