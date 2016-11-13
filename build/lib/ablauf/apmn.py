import time
import ablauf
import ablauf.dot
import random


# helper classes
class AbstractChangeState(object):
    def __init__(self, destination, type=None):
        """
        Abstract class for classes that change the actual state

        :param destination:         the new state
        :type destination:          string
        """
        self.destination = destination
        self.process = None
        self.type = type


class Jump(AbstractChangeState):
    def __init__(self, destination):
        """
        Change the actual state without calling a function

        :param destination:         the new state
        :type destination:          string
         """
        AbstractChangeState.__init__(self, destination)


class Transit(AbstractChangeState):
    def __init__(self, destination, type):
        """
        Change the actual state and call a function in between

        :param destination:         the new state
        :type destination:          string
        :param type                 the type of the transition f.e. exit, yes, no
        :type type                  string
        """
        AbstractChangeState.__init__(self, destination, type)


# game process notation classes
class ExclusiveGateway(ablauf.APNState):
    def __init__(self, config):
        """
        A decision is taken and depending on the result, the state changes.

        :param name:                        the name of the State
        :type name:                         string
        :param yes_transition:              the transition if the result is true
        :type yes_transition                function
        :param no_transition:               the transition if the result if false
        :type no_transition                function
        """
        ablauf.APNState.__init__(self, config["name"])

        if "yes_transition" in config:
            _data = config["yes_transition"]

            if _data["type"] == "Transit":
                _yes_transition = Transit(_data["destination"], "yes")
            elif _data["type"] == "Jump":
                _yes_transition = Jump(_data["destination"])
        else:
            _yes_transition = None

        if "no_transition" in config:
            _data = config["no_transition"]

            if _data["type"] == "Transit":
                _no_transition = Transit(_data["destination"], "no")
            elif _data["type"] == "Jump":
                _no_transition = Jump(_data["destination"])
        else:
            _no_transition = None

        self.yes_transition = _yes_transition
        self.no_transition = _no_transition

        try:
            self.enter_function = self.enter_state
        except:
            self.enter_function = None
            ablauf.logger.debug("State: {0} has no enter function".format(self.name))

        try:
            self.leave_function = self.leave_state
        except:
            self.leave_function = None
            ablauf.logger.debug("State: {0} has no leave function".format(self.name))

        if isinstance(self.yes_transition, Transit):
            _transition_function = None
            try:
                exec ("_transition_function = self.transition_to_" + self.yes_transition.destination + "_" + self.yes_transition.type)
            except Exception as ex:
               pass

            self.add_transition(ablauf.Transition("yes_transition", self.yes_transition.destination, _transition_function))

        if isinstance(self.no_transition, Transit):
            try:
                exec ("_transition_function = self.transition_to_" + self.no_transition.destination + "_" + self.no_transition.type)
            except:
                _transition_function = None

            self.add_transition(ablauf.Transition("no_transition", self.no_transition.destination, _transition_function))

    def process(self):
        if self.task is not None:
            self.task()

        if self.test():
            if isinstance(self.yes_transition, Transit):
                ablauf.Automate.transit("yes_transition")
            elif isinstance(self.yes_transition, Jump):
                ablauf.Automate.jump(self.yes_transition.destination)
        else:
            if isinstance(self.no_transition, Transit):
                ablauf.Automate.transit("no_transition")
            elif isinstance(self.no_transition, Jump):
                ablauf.Automate.jump(self.no_transition.destination)


class Loop(ablauf.APNState):
    def __init__(self, config):
        """
        A function is processed as long as the test_expression is not reached.
        The enter function is only processed one time. When another state return to the Loop, it is not processed again until the loop is left.
        The leaving function is only called when the test_expression is reached.

        :param name:                        the name of the State
        :type name:                         string
        :param exit_transition:             the transition if the result if false
        :type exit_transition               function
        :param loop_transition:             the transition if the result is true
        :type loop_transition               function
        """
        ablauf.APNState.__init__(self, config["name"])

        if "exit_transition" in config:
            _data = config["exit_transition"]

            if _data["type"] == "Transit":
                _exit_transition = Transit(_data["destination"], "exit")
            elif _data["type"] == "Jump":
                _exit_transition = Jump(_data["destination"])
        else:
            _exit_transition = None

        if "loop_transition" in config:
            _data = config["loop_transition"]

            if _data["type"] == "Transit":
                _loop_transition = Transit(_data["destination"], "loop")
            elif _data["type"] == "Jump":
                _loop_transition = Jump(_data["destination"])
        else:
            _loop_transition = None

        self.test_expression = None
        try:
            exec ("self.test_expression = self.test")
#            exec ("self.test_expression = ablauf.Automate.custom_controllers[\"" + self.process_name + "\"].test_" + self.name)
        except:
            ablauf.logger.error("State: {0} has no test expression".format(self.name))
            raise Exception("Mandatory process controller function was not found")

        self.loop_transition = _loop_transition
        self.exit_transition = _exit_transition
        self.initialized = False
        self.finalize = False

        self.enter_function = self.init_iteration
        self.leave_function = self.exit_loop

        try:
            self.additional_enter_function = self.enter_state
        except:
            self.additional_enter_function = None
            ablauf.logger.debug("State: {0} has no enter function".format(self.name))

        try:
            self.effective_leave_function = self.leave_state
        except:
            self.effective_leave_function = None
            ablauf.logger.debug("State: {0} has no leave function".format(self.name))

        if isinstance(self.loop_transition, Transit):
            try:
                exec ("_transition_function = self.transition_to_" + self.loop_transition.destination + "_" + self.loop_transition.type)
            except:
                _transition_function = None

            self.add_transition(ablauf.Transition("loop_transition", self.loop_transition.destination, _transition_function))

        if isinstance(self.exit_transition, Transit):
            try:
                exec ("_transition_function = self.transition_to_" + self.exit_transition.destination + "_" + self.exit_transition.type)
            except:
                _transition_function = None

            self.add_transition(ablauf.Transition("exit_transition", self.exit_transition.destination, _transition_function))

    def init_iteration(self):
        if not self.initialized:
            if self.additional_enter_function is not None:
                self.additional_enter_function()

            self.initialized = True

    def exit_loop(self):
        if self.finalize is True:
            if self.effective_leave_function is not None:
                self.effective_leave_function()

            self.finalize = False

    def process(self):
        if self.task is not None:
            self.task()

        if not self.test_expression():
            if isinstance(self.loop_transition, Transit):
                ablauf.Automate.transit("loop_transition")
            elif isinstance(self.loop_transition, Jump):
                ablauf.Automate.jump(self.loop_transition.destination)
        else:
            self.initialized = False
            self.finalize = True

            if isinstance(self.exit_transition, Transit):
                ablauf.Automate.transit("exit_transition")
            elif isinstance(self.exit_transition, Jump):
                ablauf.Automate.jump(self.exit_transition.destination)


class MultiInstance(ablauf.APNState):
    def __init__(self, config):
        """
        A function is processed as many time as defined in the iterator function.
        The enter function is only processed one time. When another state return to the Loop, it is not processed again until the loop is left.
        The leaving function is only called when the end of the iteration is reached.

        :param name:                        the name of the State
        :type name:                         string
        :param exit_transition:             the transition if the result if false
        :type exit_transition               function
        :param loop_transition:             the transition if the result is true
        :type loop_transition               function
        """
        ablauf.APNState.__init__(self, config["name"])

        if "exit_transition" in config:
            _data = config["exit_transition"]

            if _data["type"] == "Transit":
                _exit_transition = Transit(_data["destination"], "exit")
            elif _data["type"] == "Jump":
                _exit_transition = Jump(_data["destination"])
        else:
            _exit_transition = None

        if "loop_transition" in config:
            _data = config["loop_transition"]

            if _data["type"] == "Transit":
                _loop_transition = Transit(_data["destination"], "loop")
            elif _data["type"] == "Jump":
                _loop_transition = Jump(_data["destination"])
        else:
            _loop_transition = None

        self.value = config["name"] + "_element"
        ablauf.Data.session[self.value] = None

        self.iterator = None

        self.loop_transition = _loop_transition
        self.exit_transition = _exit_transition
        self.initialized = False
        self.finalize = False

        self.enter_function = self.init_iteration
        self.leave_function = self.exit_loop

        try:
            self.additional_enter_function = self.enter_state
        except:
            self.additional_enter_function = None
            ablauf.logger.debug("State: {0} has no enter function".format(self.name))

        try:
            self.effective_leave_function = self.leave_state
        except:
            self.effective_leave_function = None
            ablauf.logger.debug("State: {0} has no leave function".format(self.name))

        if isinstance(self.loop_transition, Transit):
            try:
                exec ("_transition_function = self.transition_to_" + self.loop_transition.destination + "_" + self.loop_transition.type)
            except:
                _transition_function = None

            self.add_transition(ablauf.Transition("loop_transition", self.loop_transition.destination, _transition_function))

        if isinstance(self.exit_transition, Transit):
            _transition_function = None
            try:
                exec ("_transition_function = self.transition_to_" + self.exit_transition.destination + "_" + self.exit_transition.type)
            except Exception as ex:
                pass

            self.add_transition(ablauf.Transition("exit_transition", self.exit_transition.destination, _transition_function))

    def init_iteration(self):
        if not self.initialized:
            if self.additional_enter_function is not None:
                self.additional_enter_function()

            ablauf.Data.session[self.value] = None
            self.iterator = iter(self.iteration())
            self.initialized = True

    def exit_loop(self):
        if self.finalize is True:
            if self.effective_leave_function is not None:
                self.effective_leave_function()

            self.finalize = False

    def process(self):
        if self.task is not None:
            self.task()

        try:
            ablauf.Data.session[self.value] = self.iterator.next()

            if isinstance(self.loop_transition, Transit):
                ablauf.Automate.transit("loop_transition")
            elif isinstance(self.loop_transition, Jump):
                ablauf.Automate.jump(self.loop_transition.destination)

        except StopIteration:
            self.initialized = False
            self.finalize = True

            if isinstance(self.exit_transition, Transit):
                ablauf.Automate.transit("exit_transition")
            elif isinstance(self.exit_transition, Jump):
                ablauf.Automate.jump(self.exit_transition.destination)


class Wait(ablauf.APNState):
    def __init__(self, config):
        """
        Wait for the given amount of milliseconds
        The enter function is only processed one time. When another state return to the Loop, it is not processed again until the loop is left.
        The leaving function is only called when the test_expression is reached.

        :param name:                        the name of the State
        :type name:                         string
        :param milliseconds:                the amount of milliseconds to wait
        :type milliseconds:                 int
        :param exit_transition:             the transition if the result if false
        :type exit_transition               function
        """
        ablauf.APNState.__init__(self, config["name"])

        if "exit_transition" in config:
            _data = config["exit_transition"]

            if _data["type"] == "Transit":
                try:
                    _event = _data["event"]
                except KeyError:
                    _event = None

                _transition = Transit(_data["destination"], "exit", _event)
            elif _data["type"] == "Jump":
                _transition = Jump(_data["destination"])
        else:
            _transition = None

        self.value = config["name"] + "_counter"
        ablauf.Data.session[self.value] = None

        self.iterator = None
        self.milliseconds = config["milliseconds"]
        self.exit_transition = _transition
        self.initialized = False
        self.finalize = False
        self.enter_function = self.init_iteration
        self.leave_function = self.exit_loop

        try:
            self.additional_enter_function = self.enter_state
        except:
            self.additional_enter_function = None
            ablauf.logger.debug("State: {0} has no enter function".format(self.name))

        try:
            self.effective_leave_function = self.leave_state
        except:
            self.effective_leave_function = None
            ablauf.logger.debug("State: {0} has no leave function".format(self.name))

        if isinstance(self.exit_transition, Transit):
            try:
                exec ("_transition_function = self.transition_to_" + self.exit_transition.destination + "_" + self.exit_transition.type)
            except:
                _transition_function = None

            self.add_transition(ablauf.Transition("exit_transition", self.exit_transition.destination, _transition_function))

    def init_iteration(self):
        if not self.initialized:
            if self.additional_enter_function is not None:
                self.additional_enter_function()

            ablauf.Data.session[self.value] = None
            _milliseconds = ablauf.Data.session[self.milliseconds]
            self.iterator = (i for i in range(_milliseconds))
            self.initialized = True

    def exit_loop(self):
        if self.finalize is True:
            if self.effective_leave_function is not None:
                self.effective_leave_function()

            self.finalize = False

    def process(self):
        if self.task is not None:
            self.task()

        time.sleep(0.1)

        try:
            ablauf.Data.session[self.value] = self.iterator.next()
        except StopIteration:
            self.initialized = False
            self.finalize = True

            if isinstance(self.exit_transition, Transit):
                ablauf.Automate.transit("exit_transition")
            elif isinstance(self.exit_transition, Jump):
                ablauf.Automate.jump(self.exit_transition.destination)


class InclusiveGateway(ablauf.APNState):
    def __init__(self, config):
        ablauf.APNState.__init__(self, config["name"])

        _choices = []

        if "choices" in config:
            counter = 1
            for key, value in config["choices"].iteritems():
                if key == "Transit":
                    _transition = Transit(value, "choice")
                elif key == "Jump":
                    _transition = Jump(value)

                counter += 1
                _choices.append(_transition)

        if "default_transition" in config:
            _data = config["default_transition"]

            if _data["type"] == "Transit":
                _transition = Transit(_data["destination"], "default")
            elif _data["type"] == "Jump":
                _transition = Jump(_data["destination"])
        else:
            _transition = None

        self.name = config["name"]
        self.choices = _choices
        self.default_transition = _transition

        try:
            self.enter_function = self.enter_state
        except:
            self.enter_function = None
            ablauf.logger.debug("State: {0} has no enter function".format(self.name))

        try:
            self.leave_function = self.leave_state
        except:
            self.leave_function = None
            ablauf.logger.debug("State: {0} has no leave function".format(self.name))

        for _transition in self.choices:
            try:
                exec ("_transition_function = self.transition_to_" + _transition.destination + "_" + _transition.type)
            except:
                _transition_function = None

            self.add_transition(ablauf.Transition("goto_" + _transition.destination, _transition.destination, _transition_function))

        if isinstance(self.default_transition, Transit):
            try:
                exec ("_transition_function = self.transition_to_" + self.default_transition.destination + "_" + self.default_transition.type)
            except:
                _transition_function = None

            self.add_transition(ablauf.Transition("exit_transition", self.default_transition.destination, _transition_function))

    def process(self):
        if self.task is not None:
            self.task()

        _default = True

        for _transition in self.choices:
            try:
                _transition_test_function = False
                exec ("_transition_test_function = self.test_" + _transition.destination + "()")

                if _transition_test_function:
                    if isinstance(_transition, Transit):
                        ablauf.Automate.transit("goto_" + _transition.destination)
                    elif isinstance(_transition, Jump):
                        ablauf.Automate.jump(_transition.destination)

                    _default = False
                    break
            except Exception as ex:
                 pass

        if _default:
            if isinstance(self.default_transition, Transit):
                ablauf.Automate.transit("default_transition")
            elif isinstance(self.default_transition, Jump):
                ablauf.Automate.jump(self.default_transition.destination)


class Task(ablauf.APNState):
    def __init__(self, config):
        """
        Processes a function and then transit to another state

        :param name:                        the name of the State
        :type name:                         string
        :param exit_transition:             the transition after the task is processed
        :type exit_transition               function
        """
        ablauf.APNState.__init__(self, config["name"])

        if "exit_transition" in config:
            _data = config["exit_transition"]

            if _data["type"] == "Transit":
                _transition = Transit(_data["destination"], "exit")
            elif _data["type"] == "Jump":
                _transition = Jump(_data["destination"])
        else:
            _transition = None

        self.exit_transition = _transition

        try:
            self.enter_function = self.enter_state
        except:
            self.enter_function = None
            ablauf.logger.debug("State: {0} has no enter function".format(self.name))

        try:
            self.leave_function = self.leave_state
        except:
            self.leave_function = None
            ablauf.logger.debug("State: {0} has no leave function".format(self.name))

        if isinstance(self.exit_transition, Transit):
            try:
                exec ("_transition_function = self.transition_to_" + self.exit_transition.destination + "_" + self.exit_transition.type)
            except:
                _transition_function = None

            self.add_transition(ablauf.Transition("exit_transition", self.exit_transition.destination, _transition_function))

    def process(self):
        if self.task is not None:
            self.task()

        if isinstance(self.exit_transition, Transit):
            ablauf.Automate.transit("exit_transition")
        elif isinstance(self.exit_transition, Jump):
            ablauf.Automate.jump(self.exit_transition.destination)


class SubProcess(ablauf.APNState):
    def __init__(self, config):
        ablauf.APNState.__init__(self, config["name"])

        if "exit_transition" in config:
            _data = config["exit_transition"]

            if _data["type"] == "Transit":
                _transition = Transit(_data["destination"], "exit")
            elif _data["type"] == "Jump":
                _transition = Jump(_data["destination"])
        else:
            _transition = None

        self.exit_transition = _transition
        self.processed = False

        try:
            self.enter_function = self.enter_state
        except:
            self.enter_function = None
            ablauf.logger.debug("State: {0} has no enter function".format(self.name))

        try:
            self.leave_function = self.leave_state
        except:
            self.leave_function = None
            ablauf.logger.debug("State: {0} has no leave function".format(self.name))
        if isinstance(self.exit_transition, Transit):
            try:
                exec ("_transition_function = self.transition_to_" + self.exit_transition.destination + "_" + self.exit_transition.type)
            except:
                _transition_function = None

            self.add_transition(ablauf.Transition("exit_transition", self.exit_transition.destination, _transition_function))

    def process(self):
        if self.task is not None:
            self.task()

        if self.processed is False:
            self.processed = True
            ablauf.Automate.start_subprocess(self.name)
        else:
            self.processed = False
            if isinstance(self.exit_transition, Transit):
                ablauf.Automate.transit("exit_transition")
            elif isinstance(self.exit_transition, Jump):
                ablauf.Automate.jump(self.exit_transition.destination)


class UserTask(ablauf.APNState):
    def __init__(self, config):
        """
        Processes a dialog and then transit to another state

        :param name:                        the name of the State
        :type name:                         string
        :param exit_transition:             the transition after the task is processed
        :type exit_transition               function
        """
        ablauf.APNState.__init__(self, config["name"])

        # check transitions
        # --------------------------------------------------------------------------------------------------------------
        if "exit_transition" in config:
            _data = config["exit_transition"]

            if _data["type"] == "Transit":
                _transition = Transit(_data["destination"], "exit")
            elif _data["type"] == "Jump":
                _transition = Jump(_data["destination"])
        else:
            _transition = None

        self.exit = False
        self.exit_transition = _transition

        try:
            self.enter_function = self.enter_state
        except:
            self.enter_function = None
            ablauf.logger.debug("State: {0} has no enter function".format(self.name))

        try:
            self.leave_function = self.leave_state
        except:
            self.leave_function = None
            ablauf.logger.debug("State: {0} has no leave function".format(self.name))

        if isinstance(self.exit_transition, Transit):
            try:
                exec ("_transition_function = self.transition_to_" + self.exit_transition.destination + "_" + self.exit_transition.type)
            except:
                _transition_function = None

            self.add_transition(ablauf.Transition("exit_transition", self.exit_transition.destination, _transition_function))

    def process(self):
        if self.task is not None:
            self.task()

        if self.exit:
            if isinstance(self.exit_transition, Transit):
                ablauf.Automate.transit("exit_transition")
            elif isinstance(self.exit_transition, Jump):
                ablauf.Automate.jump(self.exit_transition.destination)

    def poll_controllers(self):
        for controller_number in range(0, ablauf.Automate.input_handler.get_count()):
            _bits = ablauf.Automate.input_handler.controllers[controller_number].bits

            for polling_test in ablauf.Automate.model.actual_segment.polling:
                _value = None
                exec ("_value=ablauf.Automate.input_handler." + str(polling_test["Action"]))

                if _bits & _value:
                    try:
                        exec ("ablauf.Automate.model.actual_segment." + polling_test["Controller"] + "(ablauf.Automate.model.actual_segment)")
                    except Exception as ex:
                        exec ("ablauf.Automate.custom_controllers['Global']." + polling_test["Controller"] + "(ablauf.Automate.model.actual_segment)")


class Game(ablauf.APNState):
    def __init__(self, config):
        """
        Processes a function and then transit to another state

        :param name:                        the name of the State
        :type name:                         string
        :param exit_transition:             the transition after the task is processed
        :type exit_transition               function
        """
        ablauf.APNState.__init__(self, config["name"])

        if "exit_transition" in config:
            _data = config["exit_transition"]

            if _data["type"] == "Transit":
                _transition = Transit(_data["destination"], "exit")
            elif _data["type"] == "Jump":
                _transition = Jump(_data["destination"])
        else:
            _transition = None

        self.exit_transition = _transition

        try:
            self.enter_function = self.enter_state
        except:
            self.enter_function = None
            ablauf.logger.debug("State: {0} has no enter function".format(self.name))

        try:
            self.leave_function = self.leave_state
        except:
            self.leave_function = None
            ablauf.logger.debug("State: {0} has no leave function".format(self.name))

        if isinstance(self.exit_transition, Transit):
            try:
                exec ("_transition_function = self.transition_to_" + self.exit_transition.destination + "_" + self.exit_transition.type)
            except:
                _transition_function = None

            self.add_transition(ablauf.Transition("exit_transition", self.exit_transition.destination, _transition_function))

    def process(self):
        if self.task is not None:
            self.task()

        _number_of_players = ablauf.Data.session["parameters"]["number_of_players"]

        # tournament
        # ****************************************************************************************************
        # set values, get score from game
        for player in range(0,_number_of_players):
            _score = ablauf.Data.session["player_scores"][player]
            _id = ablauf.Data.session["player_names"][player]

            ablauf.Data.session["tournament"][player]['last_place'] = ablauf.Data.session["tournament"][player]['place']
            ablauf.Data.session["tournament"][player]['score_place'] = 0
            ablauf.Data.session["tournament"][player]['score'] = _score
            ablauf.Data.session["tournament"][player]['ID'] = _id

        # calculate place in the actual round
        for player in range(0,_number_of_players-1):
            _score = str(ablauf.Data.session["tournament"][player]['score'])

            for _other_player in range(player+1,ablauf.Data.session["parameters"]["number_of_players"]):
                _other_player_score = str(ablauf.Data.session["tournament"][_other_player]['score'])
                if(int(_score) < int(_other_player_score)):
                    ablauf.Data.session["tournament"][player]['score_place'] += 1
                else:
                    ablauf.Data.session["tournament"][_other_player]['score_place'] += 1

        # add points, set score_place and places
        for player in range(0,_number_of_players):
            ablauf.Data.session["tournament"][player]['points'] += ablauf.Data.session["place_points"][ablauf.Data.session["tournament"][player]['score_place']]
            ablauf.Data.session["tournament"][player]['place'] = 1
            ablauf.Data.session["tournament"][player]['score_place'] += 1
            ablauf.Data.session["tournament"][player][str(ablauf.Data.session["tournament"][player]['score_place'])] += 1

        # calculate place in the table
        for player in range(0,_number_of_players-1):
            _score = str(ablauf.Data.session["tournament"][player]['points'])

            for _other_player in range(player+1,ablauf.Data.session["parameters"]["number_of_players"]):
                _other_player_score = str(ablauf.Data.session["tournament"][_other_player]['points'])
                if(int(_score) < int(_other_player_score)):
                    ablauf.Data.session["tournament"][player]['place'] += 1
                else:
                    ablauf.Data.session["tournament"][_other_player]['place'] += 1

        for player in range(0,_number_of_players):
            _last_place = ablauf.Data.session["tournament"][player]['last_place']
            _place = ablauf.Data.session["tournament"][player]['place']

            if _last_place == _place or _last_place == 0:
                ablauf.Data.session["tournament"][player]['updown'] = "-"
            elif _last_place > _place:
                ablauf.Data.session["tournament"][player]['updown'] = "^"
            elif _last_place < _place:
                ablauf.Data.session["tournament"][player]['updown'] = "v"

        # highscores
        # ****************************************************************************************************
        # set values, get score from game
        _number_of_scores = ablauf.Data.session["highscores"].__len__()

        for player in range(0,_number_of_players):
            _score = ablauf.Data.session["player_scores"][player]
            _id = ablauf.Data.session["player_names"][player]
            _lowest_score = ablauf.Data.session["highscores"][_number_of_scores-1]['score']

            if _score > _lowest_score:
                ablauf.Data.session["highscores"][_number_of_scores-1]['score'] = _score
                ablauf.Data.session["highscores"][_number_of_scores-1]['ID'] = _id

                # bubble in the score
                for score in range(_number_of_scores-2,-1,-1):
                    _score = ablauf.Data.session["highscores"][score]['score']
                    _other_score = ablauf.Data.session["highscores"][score + 1]['score']
                    _id = ablauf.Data.session["highscores"][score]['ID']
                    _other_id = ablauf.Data.session["highscores"][score + 1]['ID']

                    if(int(_score) < int(_other_score)):
                        ablauf.Data.session["highscores"][score]['ID'] = _other_id
                        ablauf.Data.session["highscores"][score + 1]['ID'] = _id
                        ablauf.Data.session["highscores"][score]['score'] = _other_score
                        ablauf.Data.session["highscores"][score + 1]['score'] = _score

        if isinstance(self.exit_transition, Transit):
            ablauf.Automate.transit("exit_transition")
        elif isinstance(self.exit_transition, Jump):
            ablauf.Automate.jump(self.exit_transition.destination)