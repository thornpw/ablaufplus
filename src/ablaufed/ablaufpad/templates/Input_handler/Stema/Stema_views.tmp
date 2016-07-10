import pygame
import os

import ablauf
import ablauf.dot
import pygamekern
import pygamekern.utils
import steuer


class IterateUnmappedControllersView(ablauf.View):
    def __init__(self, name, model):
        ablauf.View.__init__(self, name, model)

    def render(self):
        self.render_template()

    def render_controller(self, segment):
        pygamekern.utils.filled_rectangle(segment.x, segment.y, ablauf.Data.configuration["width"], ablauf.Data.configuration["height"], (0, 0, 0))

    def render_mapping(self, segment):
        # Header
        # ---------------------------------------------------------------------
        _y = self.model.row_y_offset + 0 * self.model.row_height
        _ty = self.model.row_text_y_offset + 0 * self.model.row_height

        pygamekern.utils.filled_rectangle(self.model.row_x_offset, _y, self.model.row_width, self.model.row_box_height, self.model.color_dialog, self.model.row_corner_deep)
        pygamekern.utils.scalable_text(ablauf.Data.translations["unknown_header"], None, _ty, None, self.model.text_size, self.model.color_text)

        # controller status
        # ---------------------------------------------------------------------
        _y = self.model.row_y_offset + 1 * self.model.row_height
        _ty = self.model.row_text_y_offset + 1 * self.model.row_height

        pygamekern.utils.filled_rectangle(self.model.row_x_offset, _y, self.model.row_width, self.model.row_box_height, self.model.color_selected, self.model.row_corner_deep)
        pygamekern.utils.filled_rectangle(self.model.row_x_offset, _y, self.model.row_width, self.model.row_box_height, self.model.color_controller, self.model.row_corner_deep)
        pygamekern.utils.scalable_text(ablauf.Data.translations["controller_status"], None, _ty, None, self.model.text_size, self.model.color_text)

        _y = self.model.row_y_offset + 2 * self.model.row_height
        _ty = self.model.row_text_y_offset + 2 * self.model.row_height

        pygamekern.utils.filled_rectangle(self.model.row_x_offset, _y, self.model.row_width, self.model.row_box_height, self.model.color_controller, self.model.row_corner_deep)

        _start_x = (ablauf.Data.configuration["width"] - (ablauf.Data.session["controllers_status"].__len__() * self.model.column_width)) / 2

        pygamekern.utils.filled_rectangle(_start_x - 1, _y, 1, self.model.row_box_height, self.model.color_background)
        pygamekern.utils.filled_rectangle(_start_x + (ablauf.Data.session["controllers_status"].__len__() * self.model.column_width), _y, 1, self.model.row_box_height, self.model.color_background)

        for _counter in range(0, ablauf.Data.session["controllers_status"].__len__()):
            _color = self.model.color_controller
            if ablauf.Data.session["controllers_status"][_counter] == 1:
                _color = self.model.color_selected

            pygamekern.utils.filled_rectangle(_start_x + 1 + _counter * self.model.column_width, _y, self.model.column_width - 2, self.model.row_box_height, _color)

            pygamekern.utils.filled_rectangle(_start_x + _counter * self.model.column_width, _y, 1, self.model.row_box_height, self.model.color_background)
            pygamekern.utils.filled_rectangle(_start_x + (self.model.column_width - 1) + _counter * self.model.column_width, _y, 1, self.model.row_box_height, self.model.color_background)

            _text_x_offset = (self.model.column_width - pygame.font.Font(None, self.model.text_size).size(str(_counter))[0]) / 2
            pygamekern.utils.scalable_text(str(_counter), _start_x + _text_x_offset + _counter * self.model.column_width, _ty, None, self.model.text_size, self.model.color_text)

        # actual controller
        # ---------------------------------------------------------------------
        _name = ""
        _y = self.model.row_y_offset + 3 * self.model.row_height
        _ty = self.model.row_text_y_offset + 3 * self.model.row_height

        if ablauf.Data.session["actual_controller"] is not None:
            _name = ablauf.Data.session["actual_controller"].name

        pygamekern.utils.filled_rectangle(self.model.row_x_offset, _y, self.model.row_width, self.model.row_box_height, self.model.color_controller, self.model.row_corner_deep)
        pygamekern.utils.scalable_text(ablauf.Data.translations["actual_controller"] + " : {0}".format(_name), None, _ty, None, self.model.text_size, self.model.color_text)

        # explanation
        # ---------------------------------------------------------------------
        _explanation_counter = 0
        for _text in ablauf.Data.translations["mapping_explanation"]:
            _ty = (self.model.row_text_y_offset + 4 * self.model.row_height) + _explanation_counter * self.model.text_y_offset
            pygamekern.utils.scalable_text(_text, None, _ty, None, self.model.text_size, self.model.color_text)
            _explanation_counter += 1

        # Action status
        # ---------------------------------------------------------------------
        _y = self.model.row_y_offset + 12 * self.model.row_height
        _ty = self.model.row_text_y_offset + 12 * self.model.row_height

        pygamekern.utils.filled_rectangle(self.model.row_x_offset, _y, self.model.row_width, self.model.row_box_height, self.model.color_controller, self.model.row_corner_deep)
        pygamekern.utils.scalable_text(ablauf.Data.translations["action_status"], None, _ty, None, self.model.text_size, self.model.color_text)

        _y = self.model.row_y_offset + 13 * self.model.row_height
        _ty = self.model.row_text_y_offset + 13 * self.model.row_height

        pygamekern.utils.filled_rectangle(self.model.row_x_offset, _y, self.model.row_width, self.model.row_box_height, self.model.color_controller, self.model.row_corner_deep)

        if steuer.Action.unconfigured_actions.__len__() > 0:
            _counter = 0
            _start_x = (ablauf.Data.configuration["width"] - (steuer.Action.actions.__len__() * self.model.column_width)) / 2

            pygamekern.utils.filled_rectangle(_start_x - 1, _y, 1, self.model.row_box_height, self.model.color_background)
            pygamekern.utils.filled_rectangle(_start_x + (steuer.Action.actions.__len__() * self.model.column_width), _y, 1, self.model.row_box_height, self.model.color_background)

            for elem in steuer.Action.unconfigured_actions:
                _color = self.model.color_controller
                if elem == ablauf.Data.session["actual_action"]:
                    _color = self.model.color_selected

                pygamekern.utils.filled_rectangle(_start_x + 1 + _counter * self.model.column_width, _y, self.model.column_width - 2, self.model.row_box_height, _color)

                pygamekern.utils.filled_rectangle(_start_x + _counter * self.model.column_width, _y, 1, self.model.row_box_height, self.model.color_background)
                pygamekern.utils.filled_rectangle(_start_x + self.model.column_width + _counter * self.model.column_width - 1, _y, 1, self.model.row_box_height, self.model.color_background)

                _text_x_offset = (self.model.column_width - pygame.font.Font(None, self.model.text_size).size(elem.short_name)[0]) / 2
                pygamekern.utils.scalable_text(elem.short_name, _start_x + _text_x_offset + _counter * self.model.column_width, _ty, None, self.model.text_size, self.model.color_text)
                _counter += 1

        # actual action
        # ---------------------------------------------------------------------
        _y = self.model.row_y_offset + 14 * self.model.row_height
        _ty = self.model.row_text_y_offset + 14 * self.model.row_height

        pygamekern.utils.filled_rectangle(self.model.row_x_offset, _y, self.model.row_width, self.model.row_box_height, self.model.color_controller, self.model.row_corner_deep)

        _actual_action = ""
        if ablauf.Data.session["actual_action"] is not None:
            _actual_action = ablauf.Data.session["actual_action"].long_name

        pygamekern.utils.scalable_text(ablauf.Data.translations["actual_action"] + " : {0}".format(_actual_action), None, _ty, None, self.model.text_size, self.model.color_text)

        # action to do
        # ---------------------------------------------------------------------
        _y = self.model.row_y_offset + 15 * self.model.row_height
        _ty = self.model.row_text_y_offset + 15 * self.model.row_height

        if ablauf.Data.session["is_waiting"] is False:
            pygamekern.utils.filled_rectangle(self.model.row_x_offset, _y, self.model.row_width, self.model.row_box_height, self.model.color_controller, self.model.row_corner_deep)
        else:
            if ablauf.Data.session["DelayMapping_element"] < ablauf.Data.session["DelaySteps"]:
                _width_elapsed = ((self.model.row_width / (ablauf.Data.session["DelaySteps"] - 1)) * (ablauf.Data.session["DelayMapping_element"] - 1))
                _width_waiting = self.model.row_width - _width_elapsed
            else:
                _width_elapsed = self.model.row_width
                _width_waiting = 0

            pygamekern.utils.filled_rectangle(self.model.row_x_offset, _y, _width_elapsed, self.model.row_box_height, self.model.color_controller, self.model.row_corner_deep)
            pygamekern.utils.filled_rectangle(self.model.row_x_offset + _width_elapsed, _y, _width_waiting, self.model.row_box_height, self.model.color_selected, self.model.row_corner_deep)

        if ablauf.Data.session["action_status"] is not None:
            pygamekern.utils.scalable_text(ablauf.Data.session["action_status"], None, _ty, None, self.model.text_size, self.model.color_text)

        # status footer
        # ---------------------------------------------------------------------
        _y = self.model.row_y_offset + 16 * self.model.row_height
        _ty = self.model.row_text_y_offset + 16 * self.model.row_height

        pygamekern.utils.filled_rectangle(self.model.row_x_offset, _y, self.model.row_width, self.model.row_box_height, self.model.color_dialog, self.model.row_corner_deep)
        if ablauf.Data.session["stema_status"] is not None:
            pygamekern.utils.scalable_text(ablauf.Data.session["stema_status"], None, _ty, None, self.model.text_size, self.model.color_text)


class OnInitializedView(ablauf.View):
    def __init__(self, name, model):
        ablauf.View.__init__(self, name, model)

    def render(self):
        self.render_template()

    def render_init_wait(self, segment):
        pygamekern.utils.filled_rectangle(segment.x, segment.y, ablauf.Data.configuration["width"], ablauf.Data.configuration["height"], (0, 0, 0))

    def render_delay(self, segment):
        _y = self.model.row_y_offset + 7.5 * self.model.row_height
        _ty = self.model.row_text_y_offset + 7.5 * self.model.row_height

        pygamekern.utils.filled_rectangle(self.model.row_x_offset, _y, self.model.row_width, self.model.row_box_height, self.model.color_dialog, self.model.row_corner_deep)
        pygamekern.utils.scalable_text(ablauf.Data.translations["steuer_initializing"], None, _ty, None, self.model.text_size, self.model.color_text)


class ExplainUnknownWaitView(ablauf.View):
    def __init__(self, name, model):
        ablauf.View.__init__(self, name, model)

    def render(self):
        self.render_template()

    def render_explain_wait(self, segment):
        pygamekern.utils.filled_rectangle(segment.x, segment.y, ablauf.Data.configuration["width"], ablauf.Data.configuration["height"], (0, 0, 0))

    def render_text(self, segment):
        # header
        # ---------------------------------------------------------------------
        _y = self.model.row_y_offset + 0 * self.model.row_height
        _ty = self.model.row_text_y_offset + 0 * self.model.row_height

        pygamekern.utils.filled_rectangle(self.model.row_x_offset, _y, self.model.row_width, self.model.row_box_height, self.model.color_dialog, self.model.row_corner_deep)
        pygamekern.utils.scalable_text(ablauf.Data.translations["controller_detection"], None, _ty, None, self.model.text_size, self.model.color_text)

        # explanation
        # ---------------------------------------------------------------------
        _explanation_counter = 0
        for _text in ablauf.Data.translations["string_unknown_explanation"]:
            _ty = (self.model.row_text_y_offset + 4 * self.model.row_height) + _explanation_counter * self.model.text_y_offset
            pygamekern.utils.scalable_text(_text, None, _ty, None, self.model.text_size, self.model.color_text)
            _explanation_counter += 1

        # status footer
        # ---------------------------------------------------------------------
        _y = self.model.row_y_offset + 16 * self.model.row_height
        _ty = self.model.row_text_y_offset + 16 * self.model.row_height

        pygamekern.utils.filled_rectangle(self.model.row_x_offset, _y, self.model.row_width, self.model.row_box_height, self.model.color_dialog, self.model.row_corner_deep)
        if ablauf.Data.session["stema_status"] is not None:
            pygamekern.utils.scalable_text(ablauf.Data.session["stema_status"], None, _ty, None, self.model.text_size, self.model.color_text)
