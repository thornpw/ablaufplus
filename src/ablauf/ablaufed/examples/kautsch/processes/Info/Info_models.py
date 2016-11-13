import ablauf
import ablauf.model

# Models
# =============================================================================
class InitModel(ablauf.model.DefaultModel):
    def __init__(self, process_name, controller_name):
        ablauf.model.DefaultModel.__init__(self, process_name, controller_name)

# <ab> start id:info_form
# info_form model
# =============================================================================
class info_formModel(ablauf.model.DefaultModel):
    def __init__(self,process_name, controller_name):
        ablauf.model.DefaultModel.__init__(self, process_name, controller_name)

        self.game_width = 680
        self.game_height = 260

        self.game_text_x = 340

        self.rendered = False
# <ab> end id: info_form
