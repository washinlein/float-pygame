# coding=utf-8
import sys

import pygame
import pygame.gfxdraw
import tilerenderer

from pygame.locals import *
from player import Player
from lamp import Lamp

# initialize the pygame libraries
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
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
    # TODO : Avoid globals
    global player
    global lamps
    global player_rect

    player.set_rect(Rect(platforms[0].left, platforms[0].top - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT))
    player.fall_speed = 0
    player.reset_energy()
    Lamp.current_order = 0
    lamps = list(tile_renderer.get_lamps())
    player_rect = player.rect
    for lamp in lamps:
        lamp.reset()

# MAIN -------------------------------------------------------------------------------------
reset_room()

while True:
    # UPDATE -------------------------------------------------------------------------------
    check_exit()
    player.check_input()

    clock.tick(FPS)

    # check collision against platforms and floor
    player.check_platform_collisions(platforms)

    # check collisions against lamps
    index = player_rect.collidelist(lamps)
    if index != -1:
        if not lamps[index].is_lit():
            reset_room()
            continue

        lamps[index].sound_pickup.play()
        lamps.remove(lamps[index])
        Lamp.current_order += 1

    for l in lamps:
        if l.order == Lamp.current_order:
            l.lit()
            break

    # RENDER -------------------------------------------------------------------------------
    pygame.display.update()

    # draw Tiled map
    DISPLAY_SURFACE.blit(room_surface, (0, 0))

    # draw lamps
    for index in lamps:
        DISPLAY_SURFACE.blit(index.surface, index.rect)

    # draw player
    DISPLAY_SURFACE.blit(player.surface, (player_rect.left, player_rect.top))

    # render text
    text_state = game_font.render("Player state %s" % player.state, 1, (255, 255, 0))
    text_energy = game_font.render("ENERGY: %s" % player.floating_energy, 1, (255, 255, 0))
    DISPLAY_SURFACE.blit(text_state, (3, 10))
    DISPLAY_SURFACE.blit(text_energy, (150, 10))
