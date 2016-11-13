import ablauf
import ablauf.apmn
import controller

# State classes
# ============================================================================
# init task
# ****************************************************************************
class Init(ablauf.apmn.Task):
    def __init__(self, config):
        ablauf.apmn.Task.__init__(self, config)

    def task(self):
        pass


# <ab> start id:Stema
# Stema task
# ****************************************************************************
class Stema(ablauf.apmn.SubProcess):
    def __init__(self, config):
        ablauf.apmn.SubProcess.__init__(self, config)

    def task(self):
        pass
# <ab> end id: Stema

# <ab> start id:library
# library task
# ****************************************************************************
class library(ablauf.apmn.UserTask):
    def __init__(self, config):
        ablauf.apmn.UserTask.__init__(self, config)

    def task(self):
        pass

    def enter_state(self):
        controller.game_reload(self.model.actual_segment)

    def leave_state(self):
        if ablauf.Data.session["game"].__len__() == 0:
            ablauf.Data.session["actual_game"] = None
        else:
            ablauf.Data.session["actual_game"] = ablauf.Data.session["game"][self.model.actual_segment.segment_number]

# <ab> end id: library


# <ab> start id:Info
# Info task
# ****************************************************************************
class Info(ablauf.apmn.SubProcess):
    def __init__(self, config):
        ablauf.apmn.SubProcess.__init__(self, config)

    def task(self):
        pass
# <ab> end id: Info


# <ab> start id:Filter
# Filter task
# ****************************************************************************
class Filter(ablauf.apmn.SubProcess):
    def __init__(self, config):
        ablauf.apmn.SubProcess.__init__(self, config)

    def task(self):
        pass
# <ab> end id: Filter
