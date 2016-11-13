import ablauf
import ablauf.model

# Models
# =============================================================================
class InitModel(ablauf.model.DefaultModel):
    def __init__(self, process_name, controller_name):
        ablauf.model.DefaultModel.__init__(self, process_name, controller_name)

# <ab> start id:Stema
# Stema model
# =============================================================================
class StemaModel(ablauf.model.DefaultModel):
    def __init__(self,process_name, controller_name):
        ablauf.model.DefaultModel.__init__(self, process_name, controller_name)
# <ab> end id: Stema

# <ab> start id:library
# library model
# =============================================================================
class libraryModel(ablauf.model.DefaultModel):
    def __init__(self,process_name, controller_name):
        ablauf.model.DefaultModel.__init__(self, process_name, controller_name)

# <ab> end id: library

# <ab> start id:Info
# Info model
# =============================================================================
class InfoModel(ablauf.model.DefaultModel):
    def __init__(self,process_name, controller_name):
        ablauf.model.DefaultModel.__init__(self, process_name, controller_name)
# <ab> end id: Info

# <ab> start id:Filter
# Filter model
# =============================================================================
class FilterModel(ablauf.model.DefaultModel):
    def __init__(self,process_name, controller_name):
        ablauf.model.DefaultModel.__init__(self, process_name, controller_name)
# <ab> end id: Filter
