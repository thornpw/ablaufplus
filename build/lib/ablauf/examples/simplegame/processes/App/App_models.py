import ablauf.model

class InitModel(ablauf.model.DefaultModel):
    def __init__(self, process_name, controller_name):
        ablauf.model.DefaultModel.__init__(self, process_name, controller_name)
