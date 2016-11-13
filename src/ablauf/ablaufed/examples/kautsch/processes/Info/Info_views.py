import pygame

import os

import ablauf.pygamekern
import ablauf.pygamekern.utils
import ablauf


# Views
# =============================================================================
# <ab> start id:info_form
# info_form view
# =============================================================================
class info_formView(ablauf.View):
    def __init__(self, name, model):
        ablauf.View.__init__(self, name, model)

        self.model.rendered = False

    # <ab> start container id: info_dialog
    def render_info_dialog(self, segment):
        if not self.model.rendered:
            s = pygame.Surface((ablauf.Data.configuration["width"], ablauf.Data.configuration["height"]))  # the size of your rect
            s.fill((0, 0, 0))
            s.set_alpha(215)
            ablauf.pygamekern.Kernel.screen.blit(s, (0, 0))

            self.model.rendered = True

    # <ab> end container id: info_dialog

    # <ab> start container id: content
    def render_content(self, segment):
        if segment.segment_number < ablauf.Data.session["game"].__len__():
            _x = segment.x
            _y = segment.y

            ablauf.pygamekern.utils.filled_rectangle(_x, _y, self.model.game_width, self.model.game_height, (44, 62, 80), self.model.row_corner_deep)
            ablauf.pygamekern.utils.filled_rectangle(_x + 340, _y + 50, 330, 200, (52,73,94), self.model.row_corner_deep, (44,62,80))

            if segment.key in self.model.actual_path:
                _color = self.model.color_selected
            else:
                _color = self.model.color_text

            _game = ablauf.Data.session["actual_game"]

            if _game.id is not None:
                _path = os.path.join("gfx","game", str(_game.id))
                _surface = ablauf.pygamekern.utils.get_image(_path)
                if _surface is not None:
                    _surface = pygame.transform.scale(_surface, (320, 200))
                    ablauf.pygamekern.Kernel.screen.blit(_surface, (_x + 10, _y + 50))


            if not _game.name is None:
                ablauf.pygamekern.utils.scalable_text(_game.name, segment.x + self.model.game_text_x + 4 , segment.y + 52, None, self.model.text_size, _color)

    # <ab> end container id: content

    # <ab> start container id: info_button_panel
    def render_info_button_panel(self, segment):
        _x = segment.x
        _y = segment.y

        ablauf.pygamekern.utils.filled_rectangle(_x, _y, self.model.game_width - 88, 30, (52, 73, 94), self.model.row_corner_deep, (44, 62, 80))

        ablauf.pygamekern.utils.scalable_text("Game info", segment.x + 10, segment.y + 2, None, self.model.text_size, (255,255,255))


    # <ab> end container id: info_button_panel
    # <ab> start container id: info_ok
    def render_info_ok(self, segment):
        _x = segment.x
        _y = segment.y

        if segment.key == self.model.actual_path:
            _color = (255, 255, 255)
            _color_background = (127, 140, 141)
        else:
            _color = self.model.color_text
            _color_background = (52, 73, 94)

        ablauf.pygamekern.utils.filled_rectangle(_x, _y, 30, 30, _color_background, self.model.row_corner_deep, (44, 62, 80))

        _path = os.path.join("gfx", "play.png")
        _surface = ablauf.pygamekern.utils.get_image(_path)
        if _surface is not None:
            ablauf.pygamekern.Kernel.screen.blit(_surface, (_x + 3, _y + 3))

    # <ab> end container id: info_ok

    # <ab> start container id: info_cancel
    def render_info_cancel(self, segment):
        _x = segment.x
        _y = segment.y

        if segment.key == self.model.actual_path:
            _color = (255, 255, 255)
            _color_background = (127, 140, 141)
        else:
            _color = self.model.color_text
            _color_background = (52, 73, 94)

        ablauf.pygamekern.utils.filled_rectangle(_x, _y, 30, 30, _color_background, self.model.row_corner_deep, (44, 62, 80))

        _path = os.path.join("gfx", "cancel.png")
        _surface = ablauf.pygamekern.utils.get_image(_path)
        if _surface is not None:
            ablauf.pygamekern.Kernel.screen.blit(_surface, (_x + 3, _y + 3))

    # <ab> end container id: info_cancel

    # <ab> next container id:info_form

# <ab> end id: info_form

