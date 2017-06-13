import pygame


class SpriteSheet:

    def __init__(self, path, dimensions):
        self.image_surface = pygame.image.load(path)
        self.frames = list()

        self.__sprite_width = dimensions[0]
        self.__sprite_height = dimensions[1]

        # load image frames
        for y in range(0, self.image_surface.get_height(), self.__sprite_height):
            for x in range(0, self.image_surface.get_width(), self.__sprite_width):
                r = pygame.Rect(x, y, self.__sprite_width, self.__sprite_height)
                tmp_surface = pygame.Surface((self.__sprite_width, self.__sprite_height), flags=pygame.HWSURFACE)
                tmp_surface.blit(self.image_surface, (0, 0), r)
                self.frames.append(tmp_surface)

