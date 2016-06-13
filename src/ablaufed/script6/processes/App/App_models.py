import ablauf
import model

# Models
# =============================================================================
class InitModel(model.DefaultModel):
    def __init__(self, process_name, controller_name):
        model.DefaultModel.__init__(self, process_name, controller_name)

# <ab> start id:menu
# menu model
# =============================================================================
class menuModel(model.DefaultModel):
    def __init__(self,process_name, controller_name):
        model.DefaultModel.__init__(self, process_name, controller_name)
# <ab> end id: menu

# <ab> start id:options
# options model
# =============================================================================
class optionsModel(model.DefaultModel):
    def __init__(self,process_name, controller_name):
        model.DefaultModel.__init__(self, process_name, controller_name)
# <ab> end id: options

# <ab> start id:credits
# credits model
# =============================================================================
class creditsModel(model.DefaultModel):
    def __init__(self,process_name, controller_name):
        model.DefaultModel.__init__(self, process_name, controller_name)
# <ab> end id: credits

# <ab> start id:players
# players model
# =============================================================================
class playersModel(model.DefaultModel):
    def __init__(self,process_name, controller_name):
        model.DefaultModel.__init__(self, process_name, controller_name)
# <ab> end id: players

# <ab> start id:playername
# playername model
# =============================================================================
class playernameModel(model.DefaultModel):
    def __init__(self,process_name, controller_name):
        model.DefaultModel.__init__(self, process_name, controller_name)
# <ab> end id: playername

# <ab> start id:game_init
# game_init model
# =============================================================================
class game_initModel(model.DefaultModel):
    def __init__(self,process_name, controller_name):
        model.DefaultModel.__init__(self, process_name, controller_name)
# <ab> end id: game_init

# <ab> start id:game
# game model
# =============================================================================
class gameModel(model.DefaultModel):
    def __init__(self,process_name, controller_name):
        model.DefaultModel.__init__(self, process_name, controller_name)
# <ab> end id: game

# <ab> start id:highscore
# highscore model
# =============================================================================
class highscoreModel(model.DefaultModel):
    def __init__(self,process_name, controller_name):
        model.DefaultModel.__init__(self, process_name, controller_name)
# <ab> end id: highscore
