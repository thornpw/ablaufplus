__author__ = 'thorsten'

import ablauf

# Abstract Models
# =============================================================================
class DefaultModel(ablauf.Model):
    def __init__(self, process_name, controller_name):
        ablauf.Model.__init__(self, process_name, controller_name)

        # render attributes
        # *********************************************************************
        # rows
        # ---------------------------------------------------------------------
        self.row_width = ablauf.Data.configuration["width"] - 8
        self.row_height = 35
        self.row_box_height = 30
        self.row_y_offset = 4
        self.row_x_offset = 4
        self.row_text_y_offset = 5
        self.row_corner_deep = 4

        # columns
        # ---------------------------------------------------------------------
        self.column_width = 40
        # color
        # ---------------------------------------------------------------------
        self.color_background = (0, 0, 0)
        self.color_text = (255, 255, 255)
        self.color_controller = (0, 150, 0)
        self.color_selected = (0, 230, 0)
        self.color_text_selected = (255,0,0)
        self.color_dialog = (0, 40, 0)
        self.color_selection = (0, 70, 0)
        self.color_header = (0, 150, 0)

        # text
        # ---------------------------------------------------------------------
        self.text_y_offset = 30
        self.text_size = 36  # render attributes
        # *********************************************************************
        # rows
        # ---------------------------------------------------------------------
        self.row_width = ablauf.Data.configuration["width"] - 8
        self.row_height = 35
        self.row_box_height = 30
        self.row_y_offset = 4
        self.row_x_offset = 4
        self.row_text_y_offset = 5
        self.row_corner_deep = 4

        # columns
        # ---------------------------------------------------------------------
        self.column_width = 40

        # color
        # ---------------------------------------------------------------------
        self.color_background = (0, 0, 0)
        self.color_text = (255, 255, 255)
        self.color_dialog = (0, 40, 0)
        self.color_controller = (0, 150, 0)
        self.color_selected = (0, 230, 0)

        # text
        # ---------------------------------------------------------------------
        self.text_y_offset = 30
        self.text_size = 36
