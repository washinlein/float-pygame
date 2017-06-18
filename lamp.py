import pygame
from sprite_sheet import SpriteSheet


class Lamp:
    __SOUND_PICKUP = './assets/sound/lamp_pickup.wav'
    __IMAGE_PATH = './assets/graphics/lamp_sprites.png'
    LAMP_LIT = 0
    LAMP_UNLIT = 1

    sound_pickup = None
    current_order = 0
    _current_index = 0

    def __init__(self, rect, order):
        self.surface = None
        self.rect = rect
        self.order = int(order)
        self.sound_pickup = self.sound_pickup = pygame.mixer.Sound(self.__SOUND_PICKUP)
        self.__frames = SpriteSheet(self.__IMAGE_PATH, (25, 25)).frames
        self.reset()
        self.index = Lamp._current_index
        Lamp._current_index += 1
        print "Index %s is order %s " % (self.index, self.order)
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
