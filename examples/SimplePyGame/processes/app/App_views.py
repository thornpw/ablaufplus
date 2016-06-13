import pygame

import pygamekern
import pygamekern.utils
import ablauf


# Views
# =============================================================================
class MenuView(ablauf.View):
    def __init__(self, name, model):
        ablauf.View.__init__(self, name, model)

        self.rendered = False
        pass

    def render_game_info(self, segment):
        if not self.rendered:
            s = pygame.Surface((ablauf.Data.configuration["width"], ablauf.Data.configuration["height"]))  # the size of your rect
            s.fill((0, 23, 0))
            s.set_alpha(215)
            pygamekern.Kernel.screen.blit(s, (0, 0))

            pygamekern.utils.scalable_text(ablauf.Data.session["test"][0].name, 10, 10, None, 20, (0, 100, 0))

            self.rendered = True