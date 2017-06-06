import pygame

from pytmx.util_pygame import load_pygame
import pytmx


class TileRenderer(object):
    """ Render Tiled maps"""

    def __init__(self, filename):
        tile_map = load_pygame(filename)
        self.size = tile_map.width * tile_map.tilewidth, tile_map.height * tile_map.tileheight
        self.tmx_data = tile_map
        self.__platform_rects = []

    def render_map(self, surface):
        if self.tmx_data.background_color:
            surface.fill(pygame.Color(self.tmx_data.background_color))

        # iterate and draw layers
        for layer in self.tmx_data.visible_layers:

            if isinstance(layer, pytmx.TiledTileLayer):
                self.__render_tile_layer(surface, layer)

            elif isinstance(layer, pytmx.TiledObjectGroup):
                self.__render_object_layer(surface, layer)

            elif isinstance(layer, pytmx.TiledImageLayer):
                self.__render_image_layer(surface, layer)

    def __render_tile_layer(self, surface, layer):

        # deref heavily used references for speed
        tw = self.tmx_data.tilewidth
        th = self.tmx_data.tileheight
        surface_blit = surface.blit

        for x, y, image in layer.tiles():
            surface_blit(image, (x * tw, y * th))

    def __render_object_layer(self, surface, layer):

        # deref heavily used references for speed
        draw_rect = pygame.draw.rect
        draw_lines = pygame.draw.lines
        surface_blit = surface.blit

        rect_color = (255, 0, 0)
        poly_color = (0, 255, 0)

        for obj in layer:
            if hasattr(obj, 'points'):
                draw_lines(surface, poly_color, obj.closed, obj.points, 3)

            elif obj.image:
                surface_blit(obj.image, (obj.x, obj.y))

            else:
                # draw_rect(surface, rect_color, (obj.x, obj.y, obj.width, obj.height), 3)
                self.__platform_rects.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

    @staticmethod
    def __render_image_layer(surface, layer):
        if layer.image:
            surface.blit(layer.image, (0, 0))

    def get_platform_rects(self):
        return self.__platform_rects
