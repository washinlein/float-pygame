import pygame

class Player:
    """ Manages the player's behaviour """
    STATE_IDLE = 0
    STATE_MOVE_LEFT = 1
    STATE_MOVE_RIGHT = 2
    STATE_FALLING = 3
    STATE_DEAD = 4

    __WIDTH = 35
    __HEIGHT = 50

    __GRAVITY = 0.5
    __SPEED = 4

    __MAX_FLOATING_ENERGY = 450
    __FLOATING_ENERGY_INC = 3
    __FLOATING_ENERGY_DEC = 5

    __IMAGE_PATH = './assets/graphics/player.png'

    # player sounds
    __SOUND_CONTACT = './assets/sound/platform_contact.wav'

    def __init__(self, rect, display_size):
        """
        :type rect: Rect
        :type display_size: 2-tuple
        """

        self.state_previous = self.STATE_IDLE
        self.state = self.STATE_IDLE
        self.floating = False
        self.floating_energy = self.__MAX_FLOATING_ENERGY
        self.width = self.__WIDTH
        self.height = self.__HEIGHT
        self.fall_speed = 0

        self.__display_width = display_size[0]
        self.__display_height = display_size[1]

        self.surface = pygame.image.load(self.__IMAGE_PATH)
        # used for collisions and player movement
        self.rect = rect

        # load sounds
        self.__sound_contact = pygame.mixer.Sound(self.__SOUND_CONTACT)
        # this ensures that the contact platform sound is played only on first collision
        self.__sound_contact_reset = False

    def check_input(self):
        """ Checks input and update position """

        keys = pygame.key.get_pressed()

        self.state = self.STATE_IDLE

        if keys[pygame.K_LEFT]:

            self.rect.left -= self.__SPEED
            self.__set_state(self.STATE_MOVE_LEFT)

            if self.rect.left < 0:
                self.rect.left = 0
                self.__set_state(self.STATE_IDLE)

        if keys[pygame.K_RIGHT]:

            self.rect.left += self.__SPEED
            self.__set_state(self.STATE_MOVE_RIGHT)

            if self.rect.right > self.__display_width:
                self.rect.right = self.__display_width
                self.__set_state(self.STATE_IDLE)

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
                            if self.__sound_contact_reset:
                                self.__sound_contact.play()
                                self.__sound_contact_reset = False
                    break

        if result:
            self.fall_speed = 0
        else:
            self.fall_speed += 1 * self.__GRAVITY
            self.__set_state(self.STATE_FALLING)
            self.__sound_contact_reset = True

        self.__update()

        return result

    def set_rect(self, rect):
        self.rect = rect

    def __update(self):
        if not self.floating:
            self.floating_energy += self.__FLOATING_ENERGY_INC
            if self.floating_energy > self.__MAX_FLOATING_ENERGY:
                self.floating_energy = self.__MAX_FLOATING_ENERGY
        elif self.state == self.STATE_FALLING and self.floating_energy > 0:
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
