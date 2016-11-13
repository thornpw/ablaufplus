import math
import ablauf


# Abstract classes
# ---------------------------------------------------------------------------------------------------------
class Grid(object):
    def __init__(self, data, parent):
        # name
        self.name = data["name"]

        # matrix
        # number of datasets that are not shown because of scrolling
        self.visible_rows_offset = 0
        self.visible_columns_offset = 0
        # page
        self.page = 0

        # parent. key, x, y
        self.parent = parent

        if self.parent is not None:
            self.path = parent.key
            self.key = self.path + "/" + self.name
            self.x = data["x"] + parent.x
            self.y = data["y"] + parent.y
        else:
            self.path = ""
            self.key = self.name
            self.x = data["x"]
            self.y = data["y"]

        # segments
        self.segments = []
        self.rows = data["rows"]
        self.visible_rows = data["visible_rows"]
        self.columns = data["columns"]
        self.visible_columns = data["visible_columns"]
        self.max_segments = self.columns * self.rows
        self.max_visible_segments = self.visible_columns * self.visible_rows

        # navigation meta data
        self.actual_segment = data["actual_segment"]

        self.navigation = {}
        if "navigation" in data:
            self.navigation = data["navigation"]

        # data
        self.data = None
        if "data" in data:
            self.data = data["data"]

    @property
    def actual_segment(self):
        return self._actual_segment

    @actual_segment.setter
    def actual_segment(self, value):
        self._actual_segment = value
        self.actual_segment_row = value / self.columns
        self.actual_segment_column = value % self.columns

    def change_actual_segment(self, value):
        self.actual_segment = self.actual_segment + value

    def setPagesAndSelectableSegments(self, number_of_segments=None):
        self.pages = int(math.ceil(number_of_segments / (self.columns * self.rows) + 1))


class Segment(object):
    def __init__(self, data, parent, x=0, y=0, column=0, row=0, columns=1):
        # name
        self.name = data["name"]
        # model
        self.model = {}
        if "model" in data:
            self.model = data["model"]

        # matrix
        self.row = row
        self.column = column
        self.segment_number = column + (parent.columns * row)

        # coordinates
        self.x = x
        self.y = y

        # parent, path, key
        self.parent = parent
        if self.parent is not None:
            self.path = parent.key
            self.key = self.path + "/" + self.name + "_" + str(self.row) + "_" + str(self.column)
        else:
            self.path = ""
            self.key = self.name

        # input mappings
        self.input_mappings = {}
        self.set_input_mappings(self.input_mappings, data["input_mappings"])

        # polling
        self.polling = None
        if "polling" in data:
            self.polling = data['polling']

        # selected
        self.selected = False

    def change_actual_path(self, new_path, model):
        model.actual_path = new_path
        model.actual_segment = model.segment_by_name[model.actual_path]

    def get_path_from_grid_key(self, key, model):
        _parts = key.split("/")

        # constuct path
        # first all grid names are concatenated together
        _path = ""
        for part in _parts:
            if _path != "":
                _path += "/" + part
            else:
                _path += part

        # the segment is concatenated with the row and column
        _path += "/" + part + "_" + str(model.grid_by_name[part].actual_segment_row) + "_" + str(model.grid_by_name[part].actual_segment_column)

        return _path

    @staticmethod
    def set_input_mappings(obj, inputmappings):
        obj["keyinputmappings"] = {}
        obj["padinputmappings"] = {}

        for _mapping in inputmappings:
            _key = ablauf.Automate.kernel.get_key_object(_mapping["Key"])
            obj["keyinputmappings"][str(_key)] = {"Name": _mapping["Pad"], "Controller": _mapping["Controller"], "Model": _mapping["Model"]}
            obj["padinputmappings"][str(_mapping["Pad"])] = {"Name": _mapping["Pad"], "Controller": _mapping["Controller"], "Model": _mapping["Model"]}


# Form controller
# ---------------------------------------------------------------------------------------------------------
class SelectionVertical(Segment):
    def __init__(self, data, parent, x=0, y=0, column=0, row=0):
        Segment.__init__(self, data, parent, x, y, column, row)

    def segment_left(self, segment):
        _model = ablauf.Automate.model
        if "left" in segment.parent.navigation:
            self.change_actual_path(self.get_path_from_grid_key(segment.parent.navigation["left"], _model), _model)

    def segment_right(self, segment):
        _model = ablauf.Automate.model
        if "right" in segment.parent.navigation:
            self.change_actual_path(self.get_path_from_grid_key(segment.parent.navigation["right"], _model), _model)

    def segment_up(self, segment):
        _model = ablauf.Automate.model
        if segment.segment_number >= segment.parent.columns:
            segment.parent.change_actual_segment(-segment.parent.columns)
            self.change_actual_path(self.get_path_from_grid_key(_model.actual_segment.parent.key, _model), _model)
        elif segment.parent.visible_rows_offset > 0:
            segment.parent.visible_rows_offset -= 1
        elif "up" in segment.parent.navigation:
            self.change_actual_path(self.get_path_from_grid_key(segment.parent.navigation["up"], _model), _model)

    def segment_down(self, segment):
        _model = ablauf.Automate.model
        if segment.segment_number < segment.parent.visible_rows - 1:
            if segment.segment_number + segment.parent.columns <= (ablauf.Data.session[segment.parent.data].__len__() - 1):
                segment.parent.change_actual_segment(segment.parent.columns)
                self.change_actual_path(self.get_path_from_grid_key(_model.actual_segment.parent.key, _model), _model)
        elif segment.parent.visible_rows_offset < segment.parent.rows - segment.parent.visible_rows:
            segment.parent.visible_rows_offset += 1
        else:
            if "down" in segment.parent.navigation:
                self.change_actual_path(self.get_path_from_grid_key(segment.parent.navigation["down"], _model), _model)

    def toggle(self, segment):
        if segment.selected:
            segment.selected = False
        else:
            segment.selected = True


class Jump(Segment):
    def __init__(self, data, parent, x=0, y=0, column=0, row=0):
        Segment.__init__(self, data, parent, x, y, column, row)

    def segment_left(self, segment):
        _model = ablauf.Automate.model
        if segment.segment_number > 0:
            segment.parent.change_actual_segment(-1)
            self.change_actual_path(self.get_path_from_grid_key(_model.actual_segment.parent.key, _model), _model)
        else:
            if "left" in segment.parent.navigation:
                self.change_actual_path(self.get_path_from_grid_key(segment.parent.navigation["left"], _model), _model)

    def segment_right(self, segment):
        _model = ablauf.Automate.model

        if segment.parent.data is not None and (segment.segment_number) >= (ablauf.Data.session[segment.parent.data].__len__() - 1):
            return
        if segment.segment_number < segment.parent.max_segments - 1:
            segment.parent.change_actual_segment(1)
            self.change_actual_path(self.get_path_from_grid_key(_model.actual_segment.parent.key, _model), _model)
        else:
            if "right" in segment.parent.navigation:
                self.change_actual_path(self.get_path_from_grid_key(segment.parent.navigation["right"], _model), _model)

    def segment_up(self, segment):
        _model = ablauf.Automate.model
        if segment.segment_number >= segment.parent.columns:
            segment.parent.change_actual_segment(-segment.parent.columns)
            self.change_actual_path(self.get_path_from_grid_key(_model.actual_segment.parent.key, _model), _model)
        else:
            if "up" in segment.parent.navigation:
                self.change_actual_path(self.get_path_from_grid_key(segment.parent.navigation["up"], _model), _model)

    def segment_down(self, segment):
        _model = ablauf.Automate.model
        if segment.segment_number < segment.parent.max_segments - segment.parent.columns:
            if segment.parent.data is not None and segment.segment_number + segment.parent.columns > (ablauf.Data.session[segment.parent.data].__len__() - 1):
                return
            segment.parent.change_actual_segment(segment.parent.columns)
            self.change_actual_path(self.get_path_from_grid_key(_model.actual_segment.parent.key, _model), _model)
        else:
            if "down" in segment.parent.navigation:
                self.change_actual_path(self.get_path_from_grid_key(segment.parent.navigation["down"], _model), _model)

    def button_down(self, segment):
        # handle mapping
        if "mapping" in segment.model:
            for mappings in segment.model["mapping"]:
                exec ("ablauf.Data.session{0} = {1}".format(mappings[0], mappings[1]))

        _model = ablauf.Automate.model
        _segment_model = segment.model
        ablauf.Automate.jump(segment.model["destinations"][0])


class FourWaySegment(Segment):
    def __init__(self, data, parent, x=0, y=0, column=0, row=0):
        Segment.__init__(self, data, parent, x, y, column, row)

    def segment_left(self, segment):
        _model = ablauf.Automate.model
        if segment.segment_number > 0:
            segment.parent.change_actual_segment(-1)
            self.change_actual_path(self.get_path_from_grid_key(_model.actual_segment.parent.key, _model), _model)
        else:
            if "left" in segment.parent.navigation:
                self.change_actual_path(self.get_path_from_grid_key(segment.parent.navigation["left"], _model), _model)

    def segment_right(self, segment):
        _model = ablauf.Automate.model

        if segment.parent.data is not None and (segment.segment_number) >= (ablauf.Data.session[segment.parent.data].__len__() - 1):
            return
        if segment.segment_number < segment.parent.max_segments - 1:
            segment.parent.change_actual_segment(1)
            self.change_actual_path(self.get_path_from_grid_key(_model.actual_segment.parent.key, _model), _model)
        else:
            if "right" in segment.parent.navigation:
                self.change_actual_path(self.get_path_from_grid_key(segment.parent.navigation["right"], _model), _model)

    def segment_up(self, segment):
        _model = ablauf.Automate.model
        if segment.segment_number >= segment.parent.columns:
            segment.parent.change_actual_segment(-segment.parent.columns)
            self.change_actual_path(self.get_path_from_grid_key(_model.actual_segment.parent.key, _model), _model)
        else:
            if "up" in segment.parent.navigation:
                self.change_actual_path(self.get_path_from_grid_key(segment.parent.navigation["up"], _model), _model)

    def segment_down(self, segment):
        _model = ablauf.Automate.model
        if segment.segment_number < segment.parent.visible_rows - 1:
            if segment.segment_number + segment.parent.columns <= (ablauf.Data.session[segment.parent.data].__len__() - 1):
                segment.parent.change_actual_segment(segment.parent.columns)
                self.change_actual_path(self.get_path_from_grid_key(_model.actual_segment.parent.key, _model), _model)
        elif segment.parent.visible_rows_offset < segment.parent.rows - segment.parent.visible_rows:
            segment.parent.visible_rows_offset += 1
        else:
            if "down" in segment.parent.navigation:
                self.change_actual_path(self.get_path_from_grid_key(segment.parent.navigation["down"], _model), _model)


class AddChar(FourWaySegment):
    def __init__(self, data, parent, x=0, y=0, column=0, row=0):
        Segment.__init__(self, data, parent, x, y, column, row)

    def button_down(self, segment):
        _model = ablauf.Automate.model
        ablauf.Data.session[segment.model["bind"]] += segment.model["char"]


class DelChar(FourWaySegment):
    def __init__(self, data, parent, x=0, y=0, column=0, row=0):
        FourWaySegment.__init__(self, data, parent, x, y, column, row)

    def button_down(self, segment):
        _model = ablauf.Automate.model
        if ablauf.Data.session[segment.model["bind"]].__len__() > 0:
            ablauf.Data.session[segment.model["bind"]] = ablauf.Data.session[segment.model["bind"]][:-1]


class Text(Segment):
    def __init__(self, data, parent, x=0, y=0, column=0, row=0):
        Segment.__init__(self, data, parent, x, y, column, row)


class NumberOption(Segment):
    def __init__(self, data, parent, x=0, y=0, column=0, row=0):
        Segment.__init__(self, data, parent, x, y, column, row)

    def segment_left(self, segment):
        _model = ablauf.Automate.model
        _value = ablauf.Data.session["parameters"][segment.model["parameter"]]
        if _value - segment.model["step"] >= 0:
            ablauf.Data.session["parameters"][segment.model["parameter"]] -= segment.model["step"]

    def segment_right(self, segment):
        _model = ablauf.Automate.model
        _value = ablauf.Data.session["parameters"][segment.model["parameter"]]
        if _value + segment.model["step"] <= segment.model["max"]:
            ablauf.Data.session["parameters"][segment.model["parameter"]] += segment.model["step"]

    def segment_up(self, segment):
        _model = ablauf.Automate.model
        if segment.segment_number >= segment.parent.columns:
            segment.parent.change_actual_segment(-segment.parent.columns)
            self.change_actual_path(self.get_path_from_grid_key(_model.actual_segment.parent.key, _model), _model)
        else:
            if "up" in segment.parent.navigation:
                self.change_actual_path(self.get_path_from_grid_key(segment.parent.navigation["up"], _model), _model)

    def segment_down(self, segment):
        _model = ablauf.Automate.model
        if segment.segment_number < segment.parent.max_segments - segment.parent.columns:
            if segment.segment_number + segment.parent.columns <= (ablauf.Data.session[segment.parent.data].__len__() - 1):
                segment.parent.change_actual_segment(segment.parent.columns)
                self.change_actual_path(self.get_path_from_grid_key(_model.actual_segment.parent.key, _model), _model)
        else:
            if "down" in segment.parent.navigation:
                self.change_actual_path(self.get_path_from_grid_key(segment.parent.navigation["down"], _model), _model)
