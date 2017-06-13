import pygame
from sprite_sheet import SpriteSheet


class Lamp:
    __SOUND_PICKUP = './assets/sound/lamp_pickup.wav'
    __IMAGE_PATH = './assets/graphics/lamp_sprites.png'
    LAMP_LIT = 0
    LAMP_UNLIT = 1
    __frames = SpriteSheet(__IMAGE_PATH, (25, 25)).frames
    sound_pickup = None

    current_order = 0

    def __init__(self, rect, order):
        self.surface = None
        self.rect = rect
        self.order = int(order)
        self.sound_pickup = self.sound_pickup = pygame.mixer.Sound(self.__SOUND_PICKUP)
        self.reset()

    def lit(self):
        self.surface = self.__frames[self.LAMP_LIT]

    def unlit(self):
        self.surface = self.__frames[self.LAMP_UNLIT]

    def is_lit(self):
        return self.order == Lamp.current_order

    def reset(self):
        if self.order == Lamp.current_order:
            self.lit()
        else:
            self.unlit()
