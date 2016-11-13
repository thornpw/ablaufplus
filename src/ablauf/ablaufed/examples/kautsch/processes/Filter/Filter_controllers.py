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

# <ab> start id:filter_form
# filter_form task
# ****************************************************************************
class filter_form(ablauf.apmn.UserTask):
    def __init__(self, config):
        ablauf.apmn.UserTask.__init__(self, config)

    def task(self):
        pass

    def enter_state(self):
        self.model.rendered = False

        controller.tag_number_of_players_reload()

        # save selected state for cancel action
        # ---------------------------------------------------------------------
        ablauf.Data.session["old_selections"] = {"name_filter": [],"number_of_players_filter":[]}

        for elem in ablauf.Data.session["name_filter"]:
            ablauf.Data.session["old_selections"]["name_filter"].append(elem)

        for elem in ablauf.Data.session["number_of_players_filter"]:
            ablauf.Data.session["old_selections"]["number_of_players_filter"].append(elem)

# <ab> end id: filter_form
