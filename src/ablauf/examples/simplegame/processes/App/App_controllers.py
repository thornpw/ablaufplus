from random import randint

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
        print("Init processing")


# <ab> start id:Menu
# Menu task
# ****************************************************************************
class Menu(ablauf.apmn.Task):
    def __init__(self, config):
        ablauf.apmn.Task.__init__(self, config)

    def task(self):
        print("==============================")
        print("Simple game   Highscore:" + str(ablauf.Data.session["highscore"]))
        print("==============================")
        print("Options")
        print("******************************")
        print("0) Game")
        print("1) Exit")
        print("------------------------------")
        ablauf.Data.session["menu_choice"] = raw_input("your choice?")

# <ab> end id: Menu


# <ab> start id:Game
# Game task
# ****************************************************************************
class Game(ablauf.apmn.Task):
    def __init__(self, config):
        ablauf.apmn.Task.__init__(self, config)

    def task(self):
        ablauf.Data.session["score"] = randint(0, 1000)

    def transition_to_Highscore_exit(self):
        print(str(ablauf.Data.session["score"]))
        if ablauf.Data.session["highscore"] < ablauf.Data.session["score"]:
            ablauf.Data.session["highscore"] = ablauf.Data.session["score"]

# <ab> end id: Game


# <ab> start id:Highscore
# Highscore task
# ****************************************************************************
class Highscore(ablauf.apmn.Task):
    def __init__(self, config):
        ablauf.apmn.Task.__init__(self, config)

    def task(self):
        print("Highscore processing")
# <ab> end id: Highscore


# <ab> start id:Menu_choice
# Menu_choice task
# ****************************************************************************
class Menu_choice(ablauf.apmn.InclusiveGateway):
    def __init__(self, config):
        ablauf.apmn.InclusiveGateway.__init__(self, config)

    def task(self):
        pass

    def transition_to_Game_exit(self):
        ablauf.Data.session["score"] = 0

    def test_Game(self):
        return ablauf.Data.session['menu_choice'] == '0'

    def test_end(self):
        return ablauf.Data.session['menu_choice'] == '1'

# <ab> end id: Menu_choice
