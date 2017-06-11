import pygame


class Lamp:
    __IMAGE_PATH = './assets/graphics/lamp.png'
    current_lamp = 0
    surface = pygame.image.load(__IMAGE_PATH)

    def __init__(self, rect, order):
        self.rect = rect
        self.order = int(order)

    def pick_lamp(self, lamp):
        # TODO UPDATE SURFACE (LIT OR UNLIT)
        self.current_lamp += 1


