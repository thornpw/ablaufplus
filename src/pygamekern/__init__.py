__author__ = 'thorsten'

# imports
# =============================================================================
# standard
# *****************************************************************************
import types

# pygame
# *****************************************************************************
import pygame

# ablauf
# *****************************************************************************
import ablauf


class Kernel(types.ModuleType):
    __screen = None
    __clock = None
    __sync = False


    class __metaclass__(type):
        @property
        def screen(cls):
            return cls.__screen

        @screen.setter
        def screen(cls, value):
            cls.__screen = value

        @property
        def clock(cls):
            return cls.__clock

        @clock.setter
        def clock(cls, value):
            cls.__clock = value

        @property
        def sync(cls):
            return cls.__sync

        @sync.setter
        def sync(cls, value):
            cls.__sync = value


def init():
    # Pygame initialization
    pygame.init()
    pygame.joystick.init()

    # create a screen
    Kernel.screen = pygame.display.set_mode((ablauf.Data.configuration["width"], ablauf.Data.configuration["height"]))

    # set windows name
    pygame.display.set_caption(ablauf.Data.configuration["name"] + " " + ablauf.Data.configuration["version"] + " - " + ablauf.Data.configuration["author"] + " " + ablauf.Data.configuration["year_of_release"])

    # show or hide cursor
    pygame.mouse.set_visible(ablauf.Data.configuration["cursor_visible"])

    # set clock
    Kernel.clock = pygame.time.Clock()

    # init sync
    Kernel.sync = False

    # pygame constants
    Kernel.event_quit = pygame.QUIT
    Kernel.event_key_pressed = pygame.KEYDOWN
    Kernel.event_escape_pressed = pygame.K_ESCAPE


def screen_flip():
    pygame.display.flip()


def clock_sync(fps):
    Kernel.clock.tick(fps)


def get_events():
    _events = pygame.event.get()

    if _events.__len__() == 0:
        some_event = pygame.event.Event(pygame.USEREVENT + 2)
        _events = [some_event]

    return _events


def get_key_object(key):
    _key = None
    exec ("_key = pygame." + key)

    return _key


def test_if_aborted(event):
    # test if the program was aborted
    if event.type == pygame.QUIT:
        # windows closed
        ablauf.quit()

    elif event.type == pygame.KEYDOWN:
        # escape pressed
        if event.key == pygame.K_ESCAPE:
            ablauf.quit()
