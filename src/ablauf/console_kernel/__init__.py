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
    class __metaclass__(type):
        pass


def init():
    pass


def screen_flip():
    pass


def clock_sync(fps):
    pass


def get_events():
    return []


def get_key_object(key):
    return None


def test_if_aborted(event):
    pass
