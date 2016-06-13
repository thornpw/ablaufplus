import ablauf
import ablauf.apmn


# State classes
# ============================================================================
# init task
# ****************************************************************************
class Init(ablauf.apmn.Task):
    def __init__(self, config):
        ablauf.apmn.Task.__init__(self, config)

    def task(self):
        pass

# <ab> start id:menu
# menu task
# ****************************************************************************
class menu(ablauf.apmn.UserTask):
    def __init__(self, config):
        ablauf.apmn.UserTask.__init__(self, config)

    def task(self):
        pass
# <ab> end id: menu

# <ab> start id:options
# options task
# ****************************************************************************
class options(ablauf.apmn.UserTask):
    def __init__(self, config):
        ablauf.apmn.UserTask.__init__(self, config)

    def task(self):
        pass
# <ab> end id: options

# <ab> start id:credits
# credits task
# ****************************************************************************
class credits(ablauf.apmn.UserTask):
    def __init__(self, config):
        ablauf.apmn.UserTask.__init__(self, config)

    def task(self):
        pass
# <ab> end id: credits

# <ab> start id:players
# players task
# ****************************************************************************
class players(ablauf.apmn.UserTask):
    def __init__(self, config):
        ablauf.apmn.UserTask.__init__(self, config)

    def task(self):
        pass
# <ab> end id: players

# <ab> start id:playername
# playername task
# ****************************************************************************
class playername(ablauf.apmn.UserTask):
    def __init__(self, config):
        ablauf.apmn.UserTask.__init__(self, config)

    def task(self):
        pass
# <ab> end id: playername


# <ab> start id:game_init
# game_init task
# ****************************************************************************
class game_init(ablauf.apmn.Game):
    def __init__(self, config):
        ablauf.apmn.Game.__init__(self, config)

    def task(self):
        pass
# <ab> end id: game_init


# <ab> start id:game
# game task
# ****************************************************************************
class game(ablauf.apmn.Task):
    def __init__(self, config):
        ablauf.apmn.Task.__init__(self, config)

    def task(self):
        pass
# <ab> end id: game

# <ab> start id:highscore
# highscore task
# ****************************************************************************
class highscore(ablauf.apmn.UserTask):
    def __init__(self, config):
        ablauf.apmn.UserTask.__init__(self, config)

    def task(self):
        pass
# <ab> end id: highscore
