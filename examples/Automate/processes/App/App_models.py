import ablauf
import model

# Models
# =============================================================================
class InitModel(model.DefaultModel):
    def __init__(self, process_name, controller_name):
        model.DefaultModel.__init__(self, process_name, controller_name)
