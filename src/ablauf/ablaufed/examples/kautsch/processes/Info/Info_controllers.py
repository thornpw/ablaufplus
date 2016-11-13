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

# <ab> start id:info_form
# info_form task
# ****************************************************************************
class info_form(ablauf.apmn.UserTask):
    def __init__(self, config):
        ablauf.apmn.UserTask.__init__(self, config)

    def task(self):
        pass

    def enter_state(self):
        self.model.rendered = False

# <ab> end id: info_form
