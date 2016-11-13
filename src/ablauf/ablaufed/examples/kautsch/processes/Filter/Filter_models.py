import ablauf
import ablauf.model

# Models
# =============================================================================
class InitModel(ablauf.model.DefaultModel):
    def __init__(self, process_name, controller_name):
        ablauf.model.DefaultModel.__init__(self, process_name, controller_name)

# <ab> start id:filter_form
# filter_form model
# =============================================================================
class filter_formModel(ablauf.model.DefaultModel):
    def __init__(self,process_name, controller_name):
        ablauf.model.DefaultModel.__init__(self, process_name, controller_name)

        self.dialog_width = 450
        self.dialog_height = 440
        self.selection_width = 500
        self.selection_height = 434
        self.name_selection_header_width = 90
        self.player_selection_header_width = 280
        self.controller_x_spacer = 10
        self.controller_y_spacer = 10
        self.game_text_x = 340
        self.selection_text_height = 30
        self.rendered = False
        self.name_selection_width = 110
        self.player_selection_width = 300
        self.footer_width_unselected = 100

# <ab> end id: filter_form
