import pygame


class Player:
    """ Manages the player's behaviour """
    __STATE_IDLE = 0
    __STATE_MOVE_LEFT = 1
    __STATE_MOVE_RIGHT = 2
    __STATE_FALLING = 3
    __STATE_DEAD = 4

    __WIDTH = 35
    __HEIGHT = 50

    __GRAVITY = 0.5
    __SPEED = 4

    __MAX_FLOATING_ENERGY = 450
    __FLOATING_ENERGY_INC = 3
    __FLOATING_ENERGY_DEC = 5

    def __init__(self, rect, display_size):
        """
        :type rect: Rect
        :type display_size: 2-tuple
        """

        self.state_previous = self.__STATE_IDLE
        self.state = self.__STATE_IDLE
        self.floating = False
        self.floating_energy = self.__MAX_FLOATING_ENERGY
        self.width = self.__WIDTH
        self.height = self.__HEIGHT
        self.fall_speed = 0

        self.__display_width = display_size[0]
        self.__display_height = display_size[1]

        # used for collisions and player movement
        self.rect = rect

    def check_input(self):
        """ Checks input and update position """

        keys = pygame.key.get_pressed()

        self.state = self.__STATE_IDLE

        if keys[pygame.K_LEFT]:

            self.rect.left -= self.__SPEED
            self.__set_state(self.__STATE_MOVE_LEFT)

            if self.rect.left < 0:
                self.rect.left = 0
                self.__set_state(self.__STATE_IDLE)

        if keys[pygame.K_RIGHT]:

            self.rect.left += self.__SPEED
            self.__set_state(self.__STATE_MOVE_RIGHT)

            if self.rect.right > self.__display_width:
                self.rect.right = self.__display_width
                self.__set_state(self.__STATE_IDLE)

        self.floating = keys[pygame.K_SPACE]

    def check_bottom_collisions(self, solids):
        """ Check whether the player's rectangle bottom part
            collides against the given rectangles and returns
            True or False depending on the result.

        :type solids: Rect list -> boolean
        """
        if self.rect.bottom + 1 >= self.__display_height:
            self.rect.bottom = self.__display_height
            return True

        result = False

        for s in solids:
            # TODO - Check if Rect.colliderect using the bottom portion of the player's rect performs faster
            # only check near platforms
            if not (self.rect.top > s.bottom) and s.top - self.rect.bottom < s.height:
                # check if next player position collides
                if self.rect.top < s.top <= self.rect.bottom + self.fall_speed < s.bottom:
                    if not (self.rect.right < s.left or self.rect.left > s.right):
                        # this last condition prevents the player from getting again on top of the platform
                        # when quickly changing the movement direction immediately after falling off
                        if self.rect.bottom <= s.top:
                            result = True
                            self.rect.bottom = s.top
                    break

        if result:
            self.fall_speed = 0
        else:
            self.fall_speed += 1 * self.__GRAVITY
            self.__set_state(self.__STATE_FALLING)

        self.__update()

        return result

    def set_rect(self, rect):
        self.rect = rect

    def __update(self):
        if not self.floating:
            self.floating_energy += self.__FLOATING_ENERGY_INC
            if self.floating_energy > self.__MAX_FLOATING_ENERGY:
                self.floating_energy = self.__MAX_FLOATING_ENERGY
        elif self.state == self.__STATE_FALLING and self.floating_energy > 0:
            self.fall_speed = 1
            self.floating_energy -= self.__FLOATING_ENERGY_DEC
            if self.floating_energy < 0:
                self.floating_energy = 0

        self.rect.top += self.fall_speed

    def __set_state(self, state):
        """
        :type state: int
        """
        self.state_previous = self.state
        self.state = state
