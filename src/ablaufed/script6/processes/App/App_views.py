import pygame

import pygamekern
import pygamekern.utils
import ablauf


# Views
# =============================================================================
# <ab> start id:menu
# menu view
# =============================================================================
class menuView(ablauf.View):
    def __init__(self, name, model):
        ablauf.View.__init__(self, name, model)

        self.rendered = False
        pass

    # <ab> start container id: menu_dialog
    def render_menu_dialog(self, segment):
        pygamekern.utils.filled_rectangle(segment.x, segment.y, ablauf.Data.configuration["width"], ablauf.Data.configuration["height"], (0, 0, 0))

        if segment.key == self.model.actual_path:
            _color = self.model.color_selected
        else:
            _color = self.model.color_text

        pygamekern.utils.scalable_text(segment.name, segment.x, segment.y, None, 20, _color)

    # <ab> end container id: menu_dialog

    # <ab> start container id: start
    def render_start(self, segment):
        if segment.key == self.model.actual_path:
            _color = self.model.color_selected
        else:
            _color = self.model.color_text

        if "text" in segment.model and "data" in segment.model:
            _session_data = ""
            for _element in segment.model["data"]:
                _session_data += "ablauf.Data.session" + _element +","
            _session_data = _session_data[:-1]

            exec("_text = '{0}'.format({1})".format(segment.model["text"],_session_data))
        else:
            _text = segment.name

        pygamekern.utils.scalable_text(_text, segment.x, segment.y , None, 20, _color)

    # <ab> end container id: start

    # <ab> start container id: options
    def render_options(self, segment):
        if segment.key == self.model.actual_path:
            _color = self.model.color_selected
        else:
            _color = self.model.color_text

        if "text" in segment.model and "data" in segment.model:
            _session_data = ""
            for _element in segment.model["data"]:
                _session_data += "ablauf.Data.session" + _element +","
            _session_data = _session_data[:-1]

            exec("_text = '{0}'.format({1})".format(segment.model["text"],_session_data))
        else:
            _text = segment.name

        pygamekern.utils.scalable_text(_text, segment.x, segment.y , None, 20, _color)

    # <ab> end container id: options

    # <ab> start container id: credits
    def render_credits(self, segment):
        if segment.key == self.model.actual_path:
            _color = self.model.color_selected
        else:
            _color = self.model.color_text

        if "text" in segment.model and "data" in segment.model:
            _session_data = ""
            for _element in segment.model["data"]:
                _session_data += "ablauf.Data.session" + _element +","
            _session_data = _session_data[:-1]

            exec("_text = '{0}'.format({1})".format(segment.model["text"],_session_data))
        else:
            _text = segment.name

        pygamekern.utils.scalable_text(_text, segment.x, segment.y , None, 20, _color)

    # <ab> end container id: credits

    # <ab> start container id: players
    def render_players(self, segment):
        if segment.key == self.model.actual_path:
            _color = self.model.color_selected
        else:
            _color = self.model.color_text

        if "text" in segment.model and "data" in segment.model:
            _session_data = ""
            for _element in segment.model["data"]:
                _session_data += "ablauf.Data.session" + _element +","
            _session_data = _session_data[:-1]

            exec("_text = '{0}'.format({1})".format(segment.model["text"],_session_data))
        else:
            _text = segment.name

        pygamekern.utils.scalable_text(_text, segment.x, segment.y , None, 20, _color)

    # <ab> end container id: players

    # <ab> start container id: highscore
    def render_highscore(self, segment):
        if segment.key == self.model.actual_path:
            _color = self.model.color_selected
        else:
            _color = self.model.color_text

        if "text" in segment.model and "data" in segment.model:
            _session_data = ""
            for _element in segment.model["data"]:
                _session_data += "ablauf.Data.session" + _element +","
            _session_data = _session_data[:-1]

            exec("_text = '{0}'.format({1})".format(segment.model["text"],_session_data))
        else:
            _text = segment.name

        pygamekern.utils.scalable_text(_text, segment.x, segment.y , None, 20, _color)

    # <ab> end container id: highscore

    # <ab> start container id: quit
    def render_quit(self, segment):
        if segment.key == self.model.actual_path:
            _color = self.model.color_selected
        else:
            _color = self.model.color_text

        if "text" in segment.model and "data" in segment.model:
            _session_data = ""
            for _element in segment.model["data"]:
                _session_data += "ablauf.Data.session" + _element +","
            _session_data = _session_data[:-1]

            exec("_text = '{0}'.format({1})".format(segment.model["text"],_session_data))
        else:
            _text = segment.name

        pygamekern.utils.scalable_text(_text, segment.x, segment.y , None, 20, _color)

    # <ab> end container id: quit

    # <ab> next container id:menu

# <ab> end id: menu


# <ab> start id:options
# options view
# =============================================================================
class optionsView(ablauf.View):
    def __init__(self, name, model):
        ablauf.View.__init__(self, name, model)

        self.rendered = False
        pass

    # <ab> start container id: options_dialog
    def render_options_dialog(self, segment):
        pygamekern.utils.filled_rectangle(segment.x, segment.y, ablauf.Data.configuration["width"], ablauf.Data.configuration["height"], (0, 0, 0))

        if segment.key == self.model.actual_path:
            _color = self.model.color_selected
        else:
            _color = self.model.color_text

        pygamekern.utils.scalable_text(segment.name, segment.x, segment.y, None, 20, _color)

    # <ab> end container id: options_dialog

    # <ab> start container id: lives
    def render_lives(self, segment):
        if segment.key == self.model.actual_path:
            _color = self.model.color_selected
        else:
            _color = self.model.color_text

        pygamekern.utils.scalable_text(segment.name, segment.x, segment.y, None, 20, _color)
        pygamekern.utils.scalable_text(str(ablauf.Data.session["parameters"][segment.model["parameter"]]), segment.x + segment.model["parameter_x"], segment.x + segment.model["parameter_y"], None, 20, _color)

    # <ab> end container id: lives

    # <ab> start container id: exit
    def render_exit(self, segment):
        if segment.key == self.model.actual_path:
            _color = self.model.color_selected
        else:
            _color = self.model.color_text

        if "text" in segment.model and "data" in segment.model:
            _session_data = ""
            for _element in segment.model["data"]:
                _session_data += "ablauf.Data.session" + _element +","
            _session_data = _session_data[:-1]

            exec("_text = '{0}'.format({1})".format(segment.model["text"],_session_data))
        else:
            _text = segment.name

        pygamekern.utils.scalable_text(_text, segment.x, segment.y , None, 20, _color)

    # <ab> end container id: exit

    # <ab> next container id:options

# <ab> end id: options


# <ab> start id:credits
# credits view
# =============================================================================
class creditsView(ablauf.View):
    def __init__(self, name, model):
        ablauf.View.__init__(self, name, model)

        self.rendered = False
        pass

    # <ab> start container id: credits_dialog
    def render_credits_dialog(self, segment):
        pygamekern.utils.filled_rectangle(segment.x, segment.y, ablauf.Data.configuration["width"], ablauf.Data.configuration["height"], (0, 0, 0))

        if segment.key == self.model.actual_path:
            _color = self.model.color_selected
        else:
            _color = self.model.color_text

        pygamekern.utils.scalable_text(segment.name, segment.x, segment.y, None, 20, _color)

    # <ab> end container id: credits_dialog

    # <ab> start container id: exit
    def render_exit(self, segment):
        if segment.key == self.model.actual_path:
            _color = self.model.color_selected
        else:
            _color = self.model.color_text

        if "text" in segment.model and "data" in segment.model:
            _session_data = ""
            for _element in segment.model["data"]:
                _session_data += "ablauf.Data.session" + _element +","
            _session_data = _session_data[:-1]

            exec("_text = '{0}'.format({1})".format(segment.model["text"],_session_data))
        else:
            _text = segment.name

        pygamekern.utils.scalable_text(_text, segment.x, segment.y , None, 20, _color)

    # <ab> end container id: exit

    # <ab> next container id:credits

# <ab> end id: credits


# <ab> start id:players
# players view
# =============================================================================
class playersView(ablauf.View):
    def __init__(self, name, model):
        ablauf.View.__init__(self, name, model)

        self.rendered = False
        pass

    # <ab> start container id: players_dialog
    def render_players_dialog(self, segment):
        pygamekern.utils.filled_rectangle(segment.x, segment.y, ablauf.Data.configuration["width"], ablauf.Data.configuration["height"], (0, 0, 0))

        if segment.key == self.model.actual_path:
            _color = self.model.color_selected
        else:
            _color = self.model.color_text

        pygamekern.utils.scalable_text(segment.name, segment.x, segment.y, None, 20, _color)

    # <ab> end container id: players_dialog

    # <ab> start container id: player1
    def render_player1(self, segment):
        if segment.key == self.model.actual_path:
            _color = self.model.color_selected
        else:
            _color = self.model.color_text

        if "text" in segment.model and "data" in segment.model:
            _session_data = ""
            for _element in segment.model["data"]:
                _session_data += "ablauf.Data.session" + _element +","
            _session_data = _session_data[:-1]

            exec("_text = '{0}'.format({1})".format(segment.model["text"],_session_data))
        else:
            _text = segment.name

        pygamekern.utils.scalable_text(_text, segment.x, segment.y , None, 20, _color)

    # <ab> end container id: player1

    # <ab> start container id: player2
    def render_player2(self, segment):
        if segment.key == self.model.actual_path:
            _color = self.model.color_selected
        else:
            _color = self.model.color_text

        if "text" in segment.model and "data" in segment.model:
            _session_data = ""
            for _element in segment.model["data"]:
                _session_data += "ablauf.Data.session" + _element +","
            _session_data = _session_data[:-1]

            exec("_text = '{0}'.format({1})".format(segment.model["text"],_session_data))
        else:
            _text = segment.name

        pygamekern.utils.scalable_text(_text, segment.x, segment.y , None, 20, _color)

    # <ab> end container id: player2

    # <ab> start container id: player3
    def render_player3(self, segment):
        if segment.key == self.model.actual_path:
            _color = self.model.color_selected
        else:
            _color = self.model.color_text

        if "text" in segment.model and "data" in segment.model:
            _session_data = ""
            for _element in segment.model["data"]:
                _session_data += "ablauf.Data.session" + _element +","
            _session_data = _session_data[:-1]

            exec("_text = '{0}'.format({1})".format(segment.model["text"],_session_data))
        else:
            _text = segment.name

        pygamekern.utils.scalable_text(_text, segment.x, segment.y , None, 20, _color)

    # <ab> end container id: player3

    # <ab> start container id: player4
    def render_player4(self, segment):
        if segment.key == self.model.actual_path:
            _color = self.model.color_selected
        else:
            _color = self.model.color_text

        if "text" in segment.model and "data" in segment.model:
            _session_data = ""
            for _element in segment.model["data"]:
                _session_data += "ablauf.Data.session" + _element +","
            _session_data = _session_data[:-1]

            exec("_text = '{0}'.format({1})".format(segment.model["text"],_session_data))
        else:
            _text = segment.name

        pygamekern.utils.scalable_text(_text, segment.x, segment.y , None, 20, _color)

    # <ab> end container id: player4

    # <ab> start container id: player5
    def render_player5(self, segment):
        if segment.key == self.model.actual_path:
            _color = self.model.color_selected
        else:
            _color = self.model.color_text

        if "text" in segment.model and "data" in segment.model:
            _session_data = ""
            for _element in segment.model["data"]:
                _session_data += "ablauf.Data.session" + _element +","
            _session_data = _session_data[:-1]

            exec("_text = '{0}'.format({1})".format(segment.model["text"],_session_data))
        else:
            _text = segment.name

        pygamekern.utils.scalable_text(_text, segment.x, segment.y , None, 20, _color)

    # <ab> end container id: player5

    # <ab> start container id: player6
    def render_player6(self, segment):
        if segment.key == self.model.actual_path:
            _color = self.model.color_selected
        else:
            _color = self.model.color_text

        if "text" in segment.model and "data" in segment.model:
            _session_data = ""
            for _element in segment.model["data"]:
                _session_data += "ablauf.Data.session" + _element +","
            _session_data = _session_data[:-1]

            exec("_text = '{0}'.format({1})".format(segment.model["text"],_session_data))
        else:
            _text = segment.name

        pygamekern.utils.scalable_text(_text, segment.x, segment.y , None, 20, _color)

    # <ab> end container id: player6

    # <ab> start container id: player7
    def render_player7(self, segment):
        if segment.key == self.model.actual_path:
            _color = self.model.color_selected
        else:
            _color = self.model.color_text

        if "text" in segment.model and "data" in segment.model:
            _session_data = ""
            for _element in segment.model["data"]:
                _session_data += "ablauf.Data.session" + _element +","
            _session_data = _session_data[:-1]

            exec("_text = '{0}'.format({1})".format(segment.model["text"],_session_data))
        else:
            _text = segment.name

        pygamekern.utils.scalable_text(_text, segment.x, segment.y , None, 20, _color)

    # <ab> end container id: player7

    # <ab> start container id: player8
    def render_player8(self, segment):
        if segment.key == self.model.actual_path:
            _color = self.model.color_selected
        else:
            _color = self.model.color_text

        if "text" in segment.model and "data" in segment.model:
            _session_data = ""
            for _element in segment.model["data"]:
                _session_data += "ablauf.Data.session" + _element +","
            _session_data = _session_data[:-1]

            exec("_text = '{0}'.format({1})".format(segment.model["text"],_session_data))
        else:
            _text = segment.name

        pygamekern.utils.scalable_text(_text, segment.x, segment.y , None, 20, _color)

    # <ab> end container id: player8

    # <ab> start container id: exit
    def render_exit(self, segment):
        if segment.key == self.model.actual_path:
            _color = self.model.color_selected
        else:
            _color = self.model.color_text

        if "text" in segment.model and "data" in segment.model:
            _session_data = ""
            for _element in segment.model["data"]:
                _session_data += "ablauf.Data.session" + _element +","
            _session_data = _session_data[:-1]

            exec("_text = '{0}'.format({1})".format(segment.model["text"],_session_data))
        else:
            _text = segment.name

        pygamekern.utils.scalable_text(_text, segment.x, segment.y , None, 20, _color)

    # <ab> end container id: exit

    # <ab> next container id:players

# <ab> end id: players


# <ab> start id:playername
# playername view
# =============================================================================
class playernameView(ablauf.View):
    def __init__(self, name, model):
        ablauf.View.__init__(self, name, model)

        self.rendered = False
        pass

    # <ab> start container id: playername_dialog
    def render_playername_dialog(self, segment):
        pygamekern.utils.filled_rectangle(segment.x, segment.y, ablauf.Data.configuration["width"], ablauf.Data.configuration["height"], (0, 0, 0))

        if segment.key == self.model.actual_path:
            _color = self.model.color_selected
        else:
            _color = self.model.color_text

        pygamekern.utils.scalable_text(segment.name, segment.x, segment.y, None, 20, _color)

    # <ab> end container id: playername_dialog

    # <ab> start container id: exit
    def render_exit(self, segment):
        if segment.key == self.model.actual_path:
            _color = self.model.color_selected
        else:
            _color = self.model.color_text

        if "text" in segment.model and "data" in segment.model:
            _session_data = ""
            for _element in segment.model["data"]:
                _session_data += "ablauf.Data.session" + _element +","
            _session_data = _session_data[:-1]

            exec("_text = '{0}'.format({1})".format(segment.model["text"],_session_data))
        else:
            _text = segment.name

        pygamekern.utils.scalable_text(_text, segment.x, segment.y , None, 20, _color)

    # <ab> end container id: exit

    # <ab> next container id:playername

# <ab> end id: playername


# <ab> start id:highscore
# highscore view
# =============================================================================
class highscoreView(ablauf.View):
    def __init__(self, name, model):
        ablauf.View.__init__(self, name, model)

        self.rendered = False
        pass

    # <ab> start container id: highscore_dialog
    def render_highscore_dialog(self, segment):
        pygamekern.utils.filled_rectangle(segment.x, segment.y, ablauf.Data.configuration["width"], ablauf.Data.configuration["height"], (0, 0, 0))

        if segment.key == self.model.actual_path:
            _color = self.model.color_selected
        else:
            _color = self.model.color_text

        pygamekern.utils.scalable_text(segment.name, segment.x, segment.y, None, 20, _color)

    # <ab> end container id: highscore_dialog

    # <ab> start container id: tournament
    def render_tournament(self, segment):
        if segment.key == self.model.actual_path:
            _color = self.model.color_selected
        else:
            _color = self.model.color_text

        #data
        xpositions_data = segment.model["x_data"]
        xpositions_data = xpositions_data.split("|")

        # header
        xpositions_header = segment.model["x_header"]
        xpositions_header = xpositions_header.split("|")

        _counter = 0
        for _header_part in segment.model["header"].split("|"):
            pygamekern.utils.scalable_text(_header_part, int(xpositions_header[_counter]), segment.model["y_header"] , None, 20, _color)
            _counter += 1

        if ("sort_column" in segment.model) and ("reverse" in segment.model):
            #_sorted = sorted( ablauf.Data.session[segment.model['data']], key=lambda score: int(score[segment.model['sort_column']]), reverse=True )
            _sorted = sorted( ablauf.Data.session[segment.model['data']], key=lambda score: int(score[segment.model['sort_column']]), reverse=segment.model['reverse'])
        else:
            _sorted =  ablauf.Data.session[segment.model['data']]

        # data
        _row_counter = 0
        for _row in _sorted:
            _column_counter = 0
            for _column in segment.model['columns'].split("|"):
                pygamekern.utils.scalable_text(str(_row[_column]), int(xpositions_data[_column_counter]), segment.model["y_data"] + (_row_counter * segment.model["y_offset"]) , None, 20, _color)
                _column_counter += 1
            _row_counter += 1

    # <ab> end container id: tournament

    # <ab> start container id: scores
    def render_scores(self, segment):
        if segment.key == self.model.actual_path:
            _color = self.model.color_selected
        else:
            _color = self.model.color_text

        #data
        xpositions_data = segment.model["x_data"]
        xpositions_data = xpositions_data.split("|")

        # header
        xpositions_header = segment.model["x_header"]
        xpositions_header = xpositions_header.split("|")

        _counter = 0
        for _header_part in segment.model["header"].split("|"):
            pygamekern.utils.scalable_text(_header_part, int(xpositions_header[_counter]), segment.model["y_header"] , None, 20, _color)
            _counter += 1

        if ("sort_column" in segment.model) and ("reverse" in segment.model):
            #_sorted = sorted( ablauf.Data.session[segment.model['data']], key=lambda score: int(score[segment.model['sort_column']]), reverse=True )
            _sorted = sorted( ablauf.Data.session[segment.model['data']], key=lambda score: int(score[segment.model['sort_column']]), reverse=segment.model['reverse'])
        else:
            _sorted =  ablauf.Data.session[segment.model['data']]

        # data
        _row_counter = 0
        for _row in _sorted:
            _column_counter = 0
            for _column in segment.model['columns'].split("|"):
                pygamekern.utils.scalable_text(str(_row[_column]), int(xpositions_data[_column_counter]), segment.model["y_data"] + (_row_counter * segment.model["y_offset"]) , None, 20, _color)
                _column_counter += 1
            _row_counter += 1

    # <ab> end container id: scores

    # <ab> start container id: exit
    def render_exit(self, segment):
        if segment.key == self.model.actual_path:
            _color = self.model.color_selected
        else:
            _color = self.model.color_text

        if "text" in segment.model and "data" in segment.model:
            _session_data = ""
            for _element in segment.model["data"]:
                _session_data += "ablauf.Data.session" + _element +","
            _session_data = _session_data[:-1]

            exec("_text = '{0}'.format({1})".format(segment.model["text"],_session_data))
        else:
            _text = segment.name

        pygamekern.utils.scalable_text(_text, segment.x, segment.y , None, 20, _color)

    # <ab> end container id: exit

    # <ab> next container id:highscore

# <ab> end id: highscore

