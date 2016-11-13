import pygame

import os
import math

import ablauf.pygamekern
import ablauf.pygamekern.utils
import ablauf


# Views
# =============================================================================
# <ab> start id:library
# library view
# =============================================================================
class libraryView(ablauf.View):
    def __init__(self, name, model):
        ablauf.View.__init__(self, name, model)

        self.rendered = False
        pass

    # <ab> start container id: library_dialog
    def render_library_dialog(self, segment):
        #background
        ablauf.pygamekern.utils.filled_rectangle(segment.x, segment.y, ablauf.Data.configuration["width"], ablauf.Data.configuration["height"], (44, 62, 80))

        #options
        ablauf.pygamekern.utils.filled_rectangle(segment.x + 20, segment.y + 10, ablauf.Data.configuration["width"] - 112, 30, (52, 73, 94), 4, (44, 62, 80))
        ablauf.pygamekern.utils.scalable_text("Games library", segment.x + 30, segment.y + 14, None, 26, (255, 255, 255))

        #status
        ablauf.pygamekern.utils.filled_rectangle(segment.x + 20, segment.y + 770, ablauf.Data.configuration["width"] - 40, 30, (52, 73, 94), 4, (44, 62, 80))
        if ablauf.Data.session["game_count"] > 0:
            ablauf.pygamekern.utils.scalable_text("Page {0} of {1}".format(str(self.model.segment_by_name["library_dialog/game/game_0_0"].parent.page + 1), str(int(math.ceil(ablauf.Data.session["game_count"] / 9.0)))), segment.x + 30, segment.y + 774, None, 26, (255, 255, 255))
        else:
            ablauf.pygamekern.utils.scalable_text("Page 1 of 1", segment.x + 30, segment.y + 774, None, 26, (255, 255, 255))

    # <ab> end container id: library_dialog

    # <ab> start container id: config
    def render_config(self, segment):
        _x = segment.x
        _y = segment.y

        if segment.key == self.model.actual_path:
            _color = (255, 255, 255)
            _color_background = (127, 140, 141)
        else:
            _color = self.model.color_text
            _color_background = (52, 73, 94)


        ablauf.pygamekern.utils.filled_rectangle(segment.x, segment.y, 30, 30, _color_background, 4, (44, 62, 80))

        _path = os.path.join("gfx", "configuration.png");
        _surface = ablauf.pygamekern.utils.get_image(_path)
        if _surface is not None:
            ablauf.pygamekern.Kernel.screen.blit(_surface, (_x + 3, _y + 3))

    # <ab> end container id: config

    # <ab> start container id: quit
    def render_quit(self, segment):
        _x = segment.x
        _y = segment.y

        if segment.key == self.model.actual_path:
            _color = (255, 255, 255)
            _color_background = (127, 140, 141)
        else:
            _color = self.model.color_text
            _color_background = (52, 73, 94)


        ablauf.pygamekern.utils.filled_rectangle(segment.x, segment.y, 30, 30, _color_background, 4, (44, 62, 80))

        _path = os.path.join("gfx", "exit.png");
        _surface = ablauf.pygamekern.utils.get_image(_path)
        if _surface is not None:
            ablauf.pygamekern.Kernel.screen.blit(_surface, (_x + 3, _y + 3))

    # <ab> end container id: quit

    #  <ab> start container id: game
    def render_game(self, segment):
        if segment.segment_number < ablauf.Data.session["game"].__len__():
            _x = segment.x
            _y = segment.y

            if segment.key == self.model.actual_path:
                _color = (255, 255, 255)
                _color_background = (127, 140, 141)
            else:
                _color = self.model.color_text
                _color_background = (52, 73, 94)

            if "text" in segment.model:
                _session_data = ""
                if "data" in segment.model:
                    for _element in segment.model["data"]:
                        _session_data += "ablauf.Data.session" + _element + ","
                    _session_data = _session_data[:-1]

                exec ("_text = '{0}'.format({1})".format(segment.model["text"], _session_data))
            else:
                _text = segment.name

            ablauf.pygamekern.utils.filled_rectangle(segment.x, segment.y, 336, 230, _color_background, 4, (44, 62, 80))

            ablauf.pygamekern.utils.scalable_text(ablauf.Data.session["game"][segment.segment_number].name, segment.x + 8, segment.y + 4, None, 20, _color)

            if ablauf.Data.session["game"][segment.segment_number].id is not None:
                _path = os.path.join("gfx","game", str(ablauf.Data.session["game"][segment.segment_number].id));
                _surface = ablauf.pygamekern.utils.get_image(_path)
                if _surface is not None:
                    _surface = pygame.transform.scale(_surface, (320, 200))
                    ablauf.pygamekern.Kernel.screen.blit(_surface, (_x + 8, _y + 24))

                    # <ab> end container id: game

                    # <ab> next container id:library

# <ab> end id: library
