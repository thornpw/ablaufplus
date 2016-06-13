import ablauf
import model

class InitModel(model.DefaultModel):
    def __init__(self, process_name, controller_name):
        model.DefaultModel.__init__(self, process_name, controller_name)


# Project base model
# =============================================================================
class SimplePyGameViewModel(model.DefaultModel):
    def __init__(self, process_name, controller_name):
        model.DefaultModel.__init__(self, process_name, controller_name)

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
        self.color_dialog = (0, 70, 0)
        self.color_controller = (0, 150, 0)
        self.color_selected = (0, 230, 0)

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
        self.color_dialog = (0, 70, 0)
        self.color_controller = (0, 150, 0)
        self.color_selected = (0, 230, 0)

        # text
        # ---------------------------------------------------------------------
        self.text_y_offset = 30
        self.text_size = 36


# Models
# =============================================================================
class MenuModel(SimplePyGameViewModel):
    def __init__(self,process_name, controller_name):
        SimplePyGameViewModel.__init__(self, process_name, controller_name)

        self.header_texts = ['Config', 'Leave']
        self.games_buttons_texts = ['Start', 'Close']
        self.games_width = 680
        self.games_buttons_width = 80
        self.games_height = 260
        self.games_picture_width = 320
        self.games_picture_height = 200
        self.games_picture_leftspace = 10
        self.games_picture_topspace = 10
        self.text_x_spacer = 10
        self.text_y_spacer = 2
        self.games_text_x = 340
        self.games_text_height = 30
        self.rendered = False