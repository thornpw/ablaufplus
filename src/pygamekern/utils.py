import pygame
import pygamekern
import os


# **************************************************************
# Helper functions
# **************************************************************
# --------------------------------------------------------------
#  Draw a rectangle helper function
# --------------------------------------------------------------
def filled_rectangle(position_x, position_y, width, height, color, corner_deep=0, corner_color=(0, 0, 0)):
    _background = pygame.Surface((width, height))
    _background = _background.convert()
    _background.fill(color)

    _corner1 = None
    _corner2 = None
    _corner3 = None

    if corner_deep > 0:
        _corner1 = pygame.Surface((1, 1))
        _corner1 = _corner1.convert()
        _corner1.fill(corner_color)
        _corner2 = pygame.Surface((corner_deep, 1))
        _corner2 = _corner2.convert()
        _corner2.fill(corner_color)
        _corner3 = pygame.Surface((1, corner_deep))
        _corner3 = _corner3.convert()
        _corner3.fill(corner_color)

    pygamekern.Kernel.screen.blit(_background, (position_x, position_y))

    if corner_deep > 0:
        # top left corner
        pygamekern.Kernel.screen.blit(_corner1, (position_x + 1, position_y + 1))
        pygamekern.Kernel.screen.blit(_corner2, (position_x, position_y))
        pygamekern.Kernel.screen.blit(_corner3, (position_x, position_y))
        # top right corner
        pygamekern.Kernel.screen.blit(_corner1, (position_x + width - 2, position_y + 1))
        pygamekern.Kernel.screen.blit(_corner2, (position_x + width - corner_deep, position_y))
        pygamekern.Kernel.screen.blit(_corner3, (position_x + width - 1, position_y))
        # down left corner
        pygamekern.Kernel.screen.blit(_corner1, (position_x + 1, position_y + height - 2))
        pygamekern.Kernel.screen.blit(_corner2, (position_x, position_y + height - 1))
        pygamekern.Kernel.screen.blit(_corner3, (position_x, position_y + height - corner_deep))
        # down right corner
        pygamekern.Kernel.screen.blit(_corner1, (position_x + width - 2, position_y + height - 2))
        pygamekern.Kernel.screen.blit(_corner2, (position_x + width - corner_deep, position_y + height - 1))
        pygamekern.Kernel.screen.blit(_corner3, (position_x + width - 1, position_y + height - corner_deep))


def scalable_text(message, position_x, position_y, font=None, font_size=36, color=(0, 0, 0), background_width=None, background_height=None):
    _font = pygame.font.Font(font, font_size)
    _text = _font.render(message, 1, color)

    if background_width is None:
        _background_width = pygame.display.get_surface().get_rect().width
    else:
        _background_width = background_width

    if background_height is None:
        _background_height = pygame.display.get_surface().get_rect().height
    else:
        _background_height = background_height

    if position_x is None and position_y is None:
        _text_pos = _text.get_rect(centerx=_background_width / 2, centery=_background_height / 2)
    elif position_x is None:
        _text_pos = _text.get_rect(centerx=_background_width / 2)
        _text_pos[1] = position_y
    elif position_y is None:
        _text_pos = _text.get_rect(centery=_background_height / 2)
        _text_pos[0] = position_x
    else:
        _text_pos = (position_x, position_y)

    pygamekern.Kernel.screen.blit(_text, _text_pos)


def load_sound(name):
    class NoneSound:
        def play(self): pass

    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullname = os.path.join('media/sfx', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print 'Cannot load sound:', fullname
        raise SystemExit
    return sound
