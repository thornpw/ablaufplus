import pygame

import os

import ablauf.pygamekern
import ablauf.pygamekern.utils
import ablauf


# Views
# =============================================================================
# <ab> start id:filter_form
# filter_form view
# =============================================================================
class filter_formView(ablauf.View):
    def __init__(self, name, model):
        ablauf.View.__init__(self, name, model)

        self.model.rendered = False
        pass

    # <ab> start container id: filter_dialog
    def render_filter_dialog(self, segment):
        if not self.model.rendered:
            s = pygame.Surface((ablauf.Data.configuration["width"], ablauf.Data.configuration["height"]))  # the size of your rect
            s.fill((0, 0, 0))
            s.set_alpha(215)
            ablauf.pygamekern.Kernel.screen.blit(s, (0, 0))

            self.model.rendered = True

    # <ab> end container id: filter_dialog

    # <ab> start container id: filter_dialog_box
    def render_filter_dialog_box(self, segment):
        _x = segment.x
        _y = segment.y

        ablauf.pygamekern.utils.filled_rectangle(_x, _y, self.model.selection_width, self.model.selection_height, (44, 62, 80), self.model.row_corner_deep)

        ablauf.pygamekern.utils.filled_rectangle(_x+10, _y+10, self.model.selection_width - 88, 30, (52, 73, 94), self.model.row_corner_deep, (44, 62, 80))

        ablauf.pygamekern.utils.scalable_text("Game filter", segment.x + 20, segment.y + 12, None, self.model.text_size, (255,255,255))


    # <ab> end container id: filter_dialog_box

    # <ab> start container id: filter_name
    def render_filter_name(self, segment):
        _x = segment.x
        _y = segment.y

        ablauf.pygamekern.utils.filled_rectangle(_x, _y, 80, 30, (52, 73, 94), self.model.row_corner_deep, (44, 62, 80))

        ablauf.pygamekern.utils.scalable_text("Name", segment.x+20,segment.y+8, None, 20, (255,255,255))

    # <ab> end container id: filter_name
    # <ab> start container id: filter_name_list
    def render_filter_name_list(self, segment):
        _x = segment.x
        _y = segment.y

        if segment.key == self.model.actual_path:
            _color = (255, 255, 255)
            _color_background = (127, 140, 141)
        else:
            _color = self.model.color_text
            _color_background = (52, 73, 94)

        _char = ablauf.Data.session["characters"][segment.segment_number + segment.parent.visible_rows_offset * segment.parent.columns + segment.parent.visible_columns_offset]
        if _char in ablauf.Data.session["name_filter"]:
            _color = (149,165,166)

        ablauf.pygamekern.utils.filled_rectangle(_x, _y +34 * segment.segment_number, 80, 30, _color_background, self.model.row_corner_deep, (44, 62, 80))
        ablauf.pygamekern.utils.scalable_text(ablauf.Data.session["characters"][segment.segment_number + segment.parent.visible_rows_offset * segment.parent.columns + segment.parent.visible_columns_offset], _x + 34,_y + 8 + (34 * segment.segment_number), None, 20, _color)

    # <ab> end container id: filter_name_list

    # <ab> start container id: filter_number_of_players
    def render_filter_number_of_players(self, segment):
        _x = segment.x
        _y = segment.y

        ablauf.pygamekern.utils.filled_rectangle(_x, _y, 380, 30, (52, 73, 94), self.model.row_corner_deep, (44, 62, 80))

        ablauf.pygamekern.utils.scalable_text("Players", segment.x+20,segment.y+8, None, 20, (255,255,255))

    # <ab> end container id: filter_number_of_players

    # <ab> start container id: filter_number_of_players_list
    def render_filter_number_of_players_list(self, segment):
        _x = segment.x
        _y = segment.y

        if segment.key == self.model.actual_path:
            _color = (255, 255, 255)
            _color_background = (127, 140, 141)
        else:
            _color = self.model.color_text
            _color_background = (52, 73, 94)

        _nop = ablauf.Data.session["tag_number_of_players"][segment.segment_number + segment.parent.visible_rows_offset * segment.parent.columns + segment.parent.visible_columns_offset]
        if _nop in ablauf.Data.session["number_of_players_filter"]:
            _color = (149,165,166)

        ablauf.pygamekern.utils.filled_rectangle(_x, _y +34 * segment.segment_number, 380, 30, _color_background, self.model.row_corner_deep, (44, 62, 80))
        ablauf.pygamekern.utils.scalable_text(ablauf.Data.session["tag_number_of_players"][segment.segment_number + segment.parent.visible_rows_offset * segment.parent.columns + segment.parent.visible_columns_offset].name, _x + 20,_y + 8 + (34 * segment.segment_number), None, 20, _color)

    # <ab> end container id: filter_number_of_players_list

    # <ab> start container id: filter_button_panel
    def render_filter_button_panel(self, segment):
        pass

    # <ab> end container id: filter_button_panel
    # <ab> start container id: filter_ok
    def render_filter_ok(self, segment):
        _x = segment.x
        _y = segment.y

        if segment.key == self.model.actual_path:
            _color = (255, 255, 255)
            _color_background = (127, 140, 141)
        else:
            _color = self.model.color_text
            _color_background = (52, 73, 94)

        ablauf.pygamekern.utils.filled_rectangle(_x, _y, 30, 30, _color_background, self.model.row_corner_deep, (44, 62, 80))

        _path = os.path.join("gfx", "ok.png")
        _surface = ablauf.pygamekern.utils.get_image(_path)
        if _surface is not None:
            ablauf.pygamekern.Kernel.screen.blit(_surface, (_x + 3, _y + 3))

    # <ab> end container id: filter_ok

    # <ab> start container id: filter_cancel
    def render_filter_cancel(self, segment):
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

    # <ab> end container id: filter_cancel

    # <ab> next container id:filter_form

# <ab> end id: filter_form

