# **********************************************************************************************************************
# Imports
# **********************************************************************************************************************
# standard libs imports
# ----------------------------------------------------------------------------------------------------------------------
import os
import logging.config  # the logging configuration
import importlib
import json

# ablauf
# ----------------------------------------------------------------------------------------------------------------------
import dot

# sql alchemy
# ----------------------------------------------------------------------------------------------------------------------
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

# Initialize logging
# **************************************************************************
# load logger config
logging.config.fileConfig(os.path.join(os.getcwd(), "logging.conf"))
# create logger
logger = logging.getLogger('Ablauf')


# The Data class
# ===================================================================================================================
class Data(object):
    # Class variables
    # Not implemented via __metaclass__ because of second parameter (key)
    # ***************************************************************************************************************
    @property
    def configuration(cls, key):
        return cls.__configuration[key]

    @configuration.setter
    def configuraton(cls, key, value):
        cls.__configuration[key] = value

    @property
    def translations(cls, key):
        return cls.__translations[key]

    @translations.setter
    def translations(cls, key, value):
        cls.__translations[key] = value

    @property
    def session(cls, key):
        return cls.session[key]

    @session.setter
    def session(cls, key, value):
        cls.session[key] = value

    @property
    def db_objects(cls, key):
        return cls.db_objects[key]

    @db_objects.setter
    def db_objects(cls, key, value):
        cls.db_objects[key] = value

    _base = None
    _db_engine = None
    _db_session = None

    class __metaclass__(type):
        @property
        def base(cls):
            return cls._base

        @base.setter
        def base(cls, value):
            cls._base = value

        @property
        def db_engine(cls):
            return cls._db_engine

        @db_engine.setter
        def db_engine(cls, value):
            cls._db_engine = value

        @property
        def db_session(cls):
            return cls._db_session

        @db_session.setter
        def db_session(cls, value):
            cls._db_session = value


# The Automate class
# ===================================================================================================================
class Automate(object):
    # Class variables
    # ***************************************************************************************************************
    _quit = False
    _actual_process_name = None
    _actual_process = None
    _processes = None
    _model = None
    _view = None
    _custom_views = None
    _custom_controllers = None
    _custom_model = None
    _actual_process_name_in_creation = None
    _actual_state_name_in_creation = None
    _kernel = None
    _input_handler = None

    class __metaclass__(type):
        @property
        def kernel(cls):
            return cls._kernel

        @kernel.setter
        def kernel(cls, value):
            cls._kernel = value

        @property
        def input_handler(cls):
            return cls._input_handler

        @input_handler.setter
        def input_handler(cls, value):
            cls._input_handler = value

        @property
        def quit(cls):
            return cls._quit

        @quit.setter
        def quit(cls, value):
            cls._quit = value

        @property
        def actual_process_name(cls):
            return cls._actual_process_name

        @actual_process_name.setter
        def actual_process_name(cls, value):
            cls._actual_process_name = value

        @property
        def processes(cls):
            return cls._processes

        @processes.setter
        def processes(cls, value):
            cls._processes = value

        @property
        def actual_process(cls):
            return cls._actual_process

        @actual_process.setter
        def actual_process(cls, value):
            cls._actual_process = value

        @property
        def model(cls):
            return cls._model

        @model.setter
        def model(cls, value):
            cls._model = value

        @property
        def view(cls):
            return cls._view

        @view.setter
        def view(cls, value):
            cls._view = value

        @property
        def custom_views(cls):
            return cls._custom_views

        @custom_views.setter
        def custom_views(cls, value):
            cls._custom_views = value

        @property
        def custom_controllers(cls):
            return cls._custom_controllers

        @custom_controllers.setter
        def custom_controllers(cls, value):
            cls._custom_controllers = value

        @property
        def custom_model(cls):
            return cls._custom_model

        @custom_model.setter
        def custom_model(cls, value):
            cls._custom_model = value

        @property
        def actual_process_name_in_creation(cls):
            return cls._actual_process_name_in_creation

        @actual_process_name_in_creation.setter
        def actual_process_name_in_creation(cls, value):
            cls._actual_process_name_in_creation = value

        @property
        def actual_state_name_in_creation(cls):
            return cls._actual_state_name_in_creation

        @actual_state_name_in_creation.setter
        def actual_state_name_in_creation(cls, value):
            cls._actual_state_name_in_creation = value

    __active = False

    @classmethod
    def set_root_process(cls,process_name, init_function=None):
        cls.actual_process_name = process_name
        cls.actual_process = cls.processes[process_name]

        if not init_function is None:
            cls.actual_process.states["start"].leave_function = init_function

        cls.actual_process.states["end"].enter_function = finish

    @classmethod
    def transit(cls,transition_name):
        """
        Use a given transition to change to another state

        :param transition_name: the name of the transition
        :type transition_name: string
        """
        source = cls.actual_process.actual_state
        transition = source.get_transition(transition_name)
        destination = cls.actual_process.states[transition.destination_name]

        # fire leave function
        if source.leave is not None:
            source.leave()

        logger.debug("|----------------- Transit to -----------------|:" + destination.name)
        transition.fire()

        # Set new Stage & View function
        cls.actual_process.actual_state = destination

        if destination.model is not None:
            cls.model = destination.model

        if destination.view is not None:
            cls.view = destination.view

        if destination.enter is not None:
            destination.enter()

    @classmethod
    def jump(cls,state_name):
        """
        Jump to given state

        :param state_name: the name of the new state
        :type state_name: string
        """
        source = cls.actual_process.actual_state
        destination = cls.actual_process.states[state_name]

        # fire leave function
        if source.leave is not None:
            source.leave()

        logger.debug("|=================== Jump to ==================|:" + destination.name)

        # Set new Stage & View function
        cls.actual_process.actual_state = destination

        if destination.model is not None:
            cls.model = destination.model

        if destination.view is not None:
            cls.view = destination.view

        if destination.enter is not None:
            destination.enter()

    @classmethod
    def start_subprocess(cls,name):
        logger.debug("|=================== Start subprocess ==================|:" + name)

        cls.processes[name].parent_process = cls.actual_process
        cls.actual_process_name = name
        cls.actual_process = cls.processes[name]

        destination = cls.actual_process.states[cls.actual_process.states["start"].transitions["GotoFirstState"].destination_name]

        logger.debug("|=================== Jump to ==================|:" + destination.name)

        # Set new Stage & View function
        cls.actual_process.actual_state = destination

        if destination.model is not None:
            cls.model = destination.model

        if destination.view is not None:
            cls.view = destination.view

        if destination.enter is not None:
            destination.enter()

    @classmethod
    def finish_subprocess(cls):
        logger.debug("|================= Finishing subprocess ================|")

        cls.actual_process_name = cls.actual_process.parent_process.name
        cls.actual_process = cls.actual_process.parent_process

        destination = cls.actual_process.actual_state

        # Set new Stage & View function
        cls.actual_process.actual_state = destination

        if destination.model is not None:
            cls.model = destination.model

        if destination.view is not None:
            cls.view = destination.view

        if destination.enter is not None:
            destination.enter()

        # if the program was aborted, recursiv end all subprocesses
        if cls.quit:
            cls.jump("end")

    @classmethod
    def runtime(cls):
        _reaction_time = Data.configuration["reaction_delay"]

        # Main loop
        while is_active():
            # synchronize
            cls.kernel.clock_sync(Data.configuration["fps"])

            # request rendering
            cls.kernel.Kernel.sync = True

            # get list of events
            _events = cls.kernel.get_events()

            # process events
            for event in _events:
                # test if program was aborted
                cls.kernel.test_if_aborted(event)

                # set actual event
                Data.session["actual_event"] = event

                # Handle input
                cls.actual_process.actual_state.handle_input(event)

            # test if input delay is finished
            if _reaction_time == 0:
                _reaction_time = Data.configuration["reaction_delay"]

                # controller polling if input handler supports this
                if cls.model.actual_segment.polling is not None:
                    # test if controller bits are set
                    cls.actual_process.actual_state.poll_controllers()
            else:
                _reaction_time -= 1

            # Process controller
            Automate.actual_process.actual_state.process()

            # test if view is in sync
            if cls.kernel.Kernel.sync:
                cls.kernel.Kernel.sync = False

                # call rendering view
                if cls.view is not None:
                    cls.view.render_segment(cls.view.model.dot)

            # Double buffering
            cls.kernel.screen_flip()


class Process(object):
    def __init__(self, name):
        self.name = name
        self.states = {}
        self.actual_state = None
        self.parent_process = None


class State(object):
    """
    A defined state in the life cycle of a program. Could have a enter and a leaving function defined.

    :param name: the name of the state
    :type name: string
    """

    def __init__(self, name, process_name, view=None, model=None):
        """
        A state inside the state engine.

        :param name: the name of the state
        :type name: string
        """
        self.name = name
        self.process_name = process_name
        self.view = view
        self.model = model
        self.transitions = {}
        self.enter_function = None
        self.leave_function = None

        self.add_state(self, process_name)

    def enter(self):
        """
        Call the enter function. This will happen automatically when a transition to the state happens
        """
        if self.enter_function is not None:
            self.enter_function()

    def leave(self):
        """
        Call the leave function. This will happen automatically when a transition is triggered
        """
        if self.leave_function is not None:
            self.leave_function()

    def add_transition(self, transition):
        """
        Add a transition to the state.

        :param transition: the transition to add
        :type transition: ablauf.Transition
        """

        self.transitions[transition.name] = transition

    def get_transition(self, transition_name):
        """
        Return the transition of the state with the given transition name

        :param transition_name: the name of the transition to get
        :type transition_name: string
        :return: the transition
        :rtype: ablauf.Transition
        """

        return self.transitions[transition_name]

    def handle_input(self):
        """
        This function will be overriden by the real implementations
        """
        pass

    def add_state(self,state, process_name):
        """
        Add a State to the list of states

        :param state: The new state that is added to the list of states
        :type state: ablauf.state
        """
        Automate.processes[process_name].states[state.name] = state


class APNState(State):
    def __init__(self, name):
        # set model
        self.model = None
        self.view = None

        #try:
        _process = Automate.actual_process_name_in_creation
        exec ("self.model = Automate.custom_models[Automate.actual_process_name_in_creation]." + name + "Model(\"" + _process + "\",\"" + name + "\")")
        #except Exception as ex:
        #    logger.debug("no model found in state: {0}: {1} ".format(name, str(ex.message)))

        # set view
        try:
            exec ("self.view = Automate.custom_views[Automate.actual_process_name_in_creation]." + name + "View(\"" + name + "\",self.model)")
        except Exception as ex:
            logger.debug("no view found in state: {0}: {1} ".format(name, str(ex.message)))

        # call parent
        State.__init__(self, name, Automate.actual_process_name_in_creation, self.view, self.model)

        # set controller
        try:
            exec ("self.controller = Automate.custom_controllers[Automate.actual_process_name_in_creation]." + name)
        except:
            self.controller = None
            logger.info("no controller found in state: {0}".format(name))

    def task(self):
        pass

    def poll_controllers(self):
        pass

    def handle_input(self,event):
        _model = Automate.model

        if not _model is None:
            # test if an action was triggered by a pad event
            _action = Automate._input_handler.get_action(event)
            if _action is not None:
                self.is_event_defined_in_segment(_action, _model.actual_segment, "padinputmappings")

            # test if an action was triggered by a key event
            if "key" in event.dict and event.type == Automate.kernel.Kernel.event_key_pressed:
                # look in segment key mappings
                self.is_event_defined_in_segment(event.key, _model.actual_segment, "keyinputmappings")

                # look in dialog key mappings
                if str(event.key) in Data.configuration["keyinputmappings"]:
                    exec ("Automate.custom_controllers['Global']." + Data.configuration["keyinputmappings"][str(event.key)]["Controller"] + "()")

        Automate.actual_process.actual_state.process()

    def is_event_defined_in_segment(self,action, segment, mapping):
        try:
            if str(action) in segment.input_mappings[mapping]:
                try:
                    exec ("segment." + segment.input_mappings[mapping][str(action)]["Controller"] + "(segment)")
                except Exception as ex:
                     exec ("Automate.custom_controllers['Global']." + segment.input_mappings[mapping][str(action)]["Controller"] + "(segment)")
            elif segment.parent.parent is not None:
                    self.is_event_defined_in_segment(action, segment.parent.parent.segments[segment.parent.parent.actual_segment], mapping)
        except Exception as ex:
            pass


class Transition(object):
    """
    A path from one state to another. It could have a transition function defined
    """

    def __init__(self, name, destination_name, function=None, event=None):
        """
        A transition inside the state engine.

        :param name:                Set the name of the new transition
        :type name:                 string
        :param destination_name:    name of the destination state
        :type destination_name:     string
        :param function:            The function that will be called when the transition is triggered
        :type function:             function
        :param event:               The event that will be called when the transition is triggered
        :type event:                function
        """
        self.name = name
        self.destination_name = destination_name
        self.function = function
        self.event = event

    def fire(self):
        """
        Calls the function of the transition

        """
        if self.function is not None:
            logger.debug("Firing transition function:" + str(self.function.__name__))
            self.function()


class View(object):
    def __init__(self, name, model):
        # load structure
        # --------------------------------------------------------------------------------------------------------------
        self.name = name
        self.rendered = False
        self.model = model

    def render_segment(self,grid):
        """
        rekursive processing of the Dialog Object Tree (DOT).
        For each segment the render method will be called

        :param actual_segment: the segment to render
        :type actual_segment: ablauf.dot.segment
        """

        # render segments
        for segment in grid.segments:
            try:
                exec ("Automate.view.render_" + grid.name + "(segment)")
            except AttributeError as ex:
               pass

        # process children
        for chield_row in grid.children:
            for chield_column in chield_row:
                self.render_segment(chield_column)


class Model(object):
    def __init__(self, process_name, controller_name):
        self.actual_grid = None
        self.grid_by_name = {}
        self.actual_segment = None
        self.segment_by_name = {}
        self.dot = None

        if os.path.exists(os.path.join(os.getcwd(), "processes", process_name, "structure", controller_name + ".json")):
            with open(os.path.join(os.getcwd(), "processes", process_name, "structure", controller_name + ".json"), 'r') as f:
                _input = json.load(f)

            if "start_path" in _input:
                self.actual_path = _input['start_path']

            # create display object tree (dot)
            self.dot = self.create_grid(_input, None)

            # set actual grid and segment
            self.actual_segment = self.segment_by_name[self.actual_path]
            self.actual_grid = self.actual_segment.parent
        else:
            self.actual_segment = dot.Segment({"name":"dummy","input_mappings":[],"polling":[]},None)


    def create_grid(self, att, parent):
        """
        Create a grid structure used to bind input controls to it.
        """
        # create the grid object
        _grid = dot.Grid(att, parent)

        # put the name of the grid into a dictionary
        self.grid_by_name[_grid.name] = _grid

        # init chield row
        _row_grids = []
        _row_counter = 0

        # child grids are stored in the structure in the attribute "children". its a list (rows) of hashes (columns)
        for _row_grid in att["children"]:
            # init column grids
            _column_grids = []

            _column_counter = 0
            for _column_grid in _row_grid:
                # create child grid and append it to the list of column grids
                _column_grids.append(self.create_grid(_column_grid, _grid))
                _column_counter += 1

            # append column grids to the list of row grids
            _row_grids.append(_column_grids)
            _row_counter += 1

        # set grid structure
        _grid.children = _row_grids

        # grid = json element = grid for segments used for navigation between grids
        # segment = form display element

        # create segments
        # =======================================================================
        # Set form segment class. Default class is Segement
        if "class" in att:
            _class_name = att["class"]
        else:
            _class_name = "Segment"

        # vairable initialization
        _segment = None
        _segment_name = att["name"]
        _segment_y = _grid.y

        for _segment_row in range(0, att["visible_rows"]):
            _segment_x = _grid.x

            for _segment_column in range(0, att["columns"]):
                _segment_name = _grid.name + "_" + str(_segment_column) + "_" + str(_segment_row)

                exec ("_segment = dot." + _class_name + "(att, _grid,_segment_x,_segment_y,_segment_column,_segment_row)")

                self.segment_by_name[_segment.key] = _segment
                _grid.segments.append(_segment)

                _segment_x += att["x_offset"]
            _segment_y += att["y_offset"]

        # return grid
        # =======================================================================
        return _grid


# functions
# ******************************************************************************************************************
def init():
    """
    Initialize the state engine
    """
    Automate.processes = {}
    Automate.model = None
    Automate.view = None
    Automate.custom_views = {}
    Automate.custom_controllers = {}
    Automate.custom_models = {}

    # load configuration
    with open(os.getcwd() + '/configuration/configuration.json') as data_file:
        # load json file
        Data.configuration = json.load(data_file)

    # load kernel from configuration
    Automate.kernel = importlib.import_module(Data.configuration["kernel"])

    # load input_handler from configuration
    Automate.input_handler = importlib.import_module(Data.configuration["input_handler"])

    # set global input mapping
    dot.Segment.set_input_mappings(Data.configuration, Data.configuration["inputmappings"])

    # load translations
    with open(os.getcwd() + '/configuration/translations.json') as data_file:
        Data.translations = json.load(data_file)

    # initialize session
    with open(os.getcwd() + '/configuration/session.json') as data_file:
        Data.session = json.load(data_file)

    # initialize backend
    Data.db_objects = {}

    if "backend" in Data.configuration and Data.configuration["backend"]["use"]:
        # SQLAlchemy DB Connection
        Data.base = automap_base()
        if Data.configuration["backend"]["path"]["use_home_directory"]:
            Data.db_engine = create_engine('sqlite:////' + os.path.join(os.path.expanduser("~"), Data.configuration["backend"]["path"]["home_directory_path"], Data.configuration["backend"]["path"]["file_name"]), echo=False)
        else:
            Data.db_engine = create_engine('sqlite:////' + os.path.join(os.getcwd(), "backend", Data.configuration["backend"]["path"]["file_name"]), echo=False)

        # reflect the tables
        Data.base.prepare(Data.db_engine, reflect=True)

        # mapped classes are now created with names by default
        # matching that of the table name.
        for object in Data.configuration["backend"]["objects"]:
            exec ("Data.db_objects[object] = Data.base.classes." + object)

        Data.db_session = Session(Data.db_engine)

    # initialize custom controllers
    try:
        Automate.custom_controllers["Global"] = importlib.import_module("controller")
        logger.debug("[ok] global controllers loaded".format())
    except ImportError:
        logger.error("[ERROR!] Did not found global controllers".format())

    logger.debug("[ok] initialized Ablauf+")

    # load processes
    # ==============================================================================================================
    d = os.path.join(os.getcwd(), "processes")

    for _process_name in os.listdir(d):
        if os.path.isdir(os.path.join(os.getcwd(), "processes", _process_name)):
            Automate.actual_process_name_in_creation = _process_name

            if os.path.isdir(os.path.join(d, _process_name)):
                # Create processes
                # *****************************************************************************
                with open(os.path.join(d, _process_name, _process_name + "_process.json")) as data_file:
                    apn_json = json.load(data_file)

                Automate.processes[_process_name] = Process(_process_name)

                _Start = State("start", _process_name)
                _GoFirst = Transition("GotoFirstState", apn_json["states"][0]["name"], None)

                _Start.add_transition(_GoFirst)

                _End = State("end", _process_name)
                _End.enter_function = Automate.finish_subprocess

                # Loads the parts of a process
                # ************************************************************************************
                try:
                    Automate.custom_views[_process_name] = importlib.import_module("processes." + _process_name + "." + _process_name + "_views")
                    logger.debug("[ok] {0}_views loaded".format(_process_name))
                except ImportError as ex:
                    logger.error("[ERROR!] Did not found {0}_views".format(_process_name))

                try:
                    Automate.custom_controllers[_process_name] = importlib.import_module("processes." + _process_name + "." + _process_name + "_controllers")
                    logger.debug("[ok] {0}_controllers loaded".format(_process_name))
                except ImportError as ex:
                    logger.error("[ERROR!] Did not found {0}_controllers".format(_process_name))

                try:
                    Automate.custom_models[_process_name] = importlib.import_module("processes." + _process_name + "." + _process_name + "_models")
                    logger.debug("[ok] {0}_models loaded".format(_process_name))
                except ImportError as ex:
                    logger.error("[ERROR!] Did not found {0}_models".format(_process_name))

                # Import states from the states.json file
                # *************************************************************************************
                for state in apn_json["states"]:
                    logger.debug("----------------------------------------------- State:{0} ----------------------------------------------------------".format(state["name"]))
                    Automate.actual_state_name_in_creation = state["name"]

                    exec ("Automate.custom_controllers[_process_name]." + state["name"] + "(state)")

    # initialize kernel
    # ==============================================================================================================
    Automate.kernel.init()


    # initialize input handler
    # ==============================================================================================================
    Automate.input_handler.init()


def start(root_process_name="App", init_function=None):
    """
    starts the processing of the main loop

    :param init_function: the name of the function that is called during the transition from the Start state to the first state
    :type init_function: function
    """
    Automate.__active = True
    logger.debug("start Ablauf state engine")

    # set root process
    Automate.set_root_process(root_process_name, init_function)

    # set first state and transit to this stage
    Automate.actual_process.actual_state = Automate.actual_process.states["start"]
    Automate.transit("GotoFirstState")

    Automate.runtime()


def is_active():
    return Automate.__active


def quit():
    Automate.quit = True
    Automate.jump("end")


def finish():
    """
    Exit Ablauf
    """
    logger.debug("finishing Ablauf+")
    logger.debug("Ablauf+ main loop stopped")

    Automate.__active = False

    exit()
