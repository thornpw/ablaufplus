from sqlalchemy import or_, and_
import subprocess
import shlex

import ablauf


def game_reload(segment):
    obj_class = "game"
    obj_class_count = "game_count"

    _model = ablauf.Automate.model
    ablauf.Data.session[obj_class] = []

    _object = ablauf.Data.db_objects[obj_class]

    _filter_name = get_name_filter()
    _filter_number_of_players = get_number_of_player_filter()

    ablauf.Data.session[obj_class_count] = ablauf.Data.db_session.query(_object).filter(and_(or_(_filter_name), or_(_filter_number_of_players))).order_by(_object.id).count()

    for elem in ablauf.Data.db_session.query(_object).filter(and_(or_(_filter_name), or_(_filter_number_of_players))).order_by(_object.id).limit(segment.parent.max_segments).offset((segment.parent.page * segment.parent.max_segments)):
        ablauf.Data.session[obj_class].append(elem)

    if (ablauf.Data.session[obj_class].__len__() - 1) < segment.parent.actual_segment:
        _new_segment = ablauf.Data.session[obj_class].__len__()
        if _new_segment > 0:
            _new_segment -= 1
        segment.parent.actual_segment = _new_segment
        segment.change_actual_path(ablauf.Automate.model.actual_segment.get_path_from_grid_key(ablauf.Automate.model.actual_segment.parent.key, ablauf.Automate.model), ablauf.Automate.model)


def tag_number_of_players_reload():
    ablauf.Data.session["tag_number_of_players"] = []

    _tagnames = ablauf.Data.db_objects["tagnames"]
    _tagcategory = ablauf.Data.db_objects["tagcategory"]
    for tagname, tagcategory in ablauf.Data.db_session.query(_tagnames, _tagcategory).join(_tagcategory).filter(_tagcategory.id == 1):
        ablauf.Data.session["tag_number_of_players"].append(tagname)


def get_name_filter():
    # ----------------------------------------------------------------
    # calculate selected characters that are part of the search string
    # ----------------------------------------------------------------
    # exmaple:
    # .query(CustomModels.Game).filter(and_( or_(getgameSearchString()), or(getgameSearchString()) )).order_by(CustomModels.Game.id).limit(_number_of_elements)
    _found = False

    for character in ablauf.Data.session["name_filter"]:
        if not _found:
            filters = ablauf.Data.db_objects["game"].name.like(character + '%')
        else:
            filters += ablauf.Data.db_objects["game"].name.like(character + '%')

        _found = True

    if _found is False:
        filters = ablauf.Data.db_objects["game"].name.like('%%')

    return filters


def get_number_of_player_filter():
    # ---------------------------------------------------------------
    # calculate number of players that are part of the search string
    # ---------------------------------------------------------------
    _found = False

    for tag in ablauf.Data.session["number_of_players_filter"]:
        if _found is False:
            filters = ablauf.Data.db_objects["game"].tags_collection.any(tagname_id = tag.id)
        else:
            filters += ablauf.Data.db_objects["game"].tags_collection.any(tagname_id = tag.id)

        _found = True

    if _found is False:
        filters = ablauf.Data.db_objects["game"].name.like ('%%')

    return filters


def game_page_down(segment):
    if segment.parent.page > 0:
        segment.parent.page -= 1
        game_reload(segment)


def game_page_up(segment):
    if ablauf.Data.session["game_count"] > (segment.parent.page + 1) * segment.parent.max_segments:
        segment.parent.page += 1
        game_reload(segment)


def change_name_filter(segment):
    _char = ablauf.Data.session["characters"][segment.segment_number + segment.parent.visible_rows_offset * segment.parent.columns + segment.parent.visible_columns_offset]
    if not _char in ablauf.Data.session["name_filter"]:
        ablauf.Data.session["name_filter"].append(_char)
    else:
        ablauf.Data.session["name_filter"].remove(_char)


def change_number_of_players_filter(segment):
    _nop = ablauf.Data.session["tag_number_of_players"][segment.segment_number + segment.parent.visible_rows_offset * segment.parent.columns + segment.parent.visible_columns_offset]
    if not _nop in ablauf.Data.session["number_of_players_filter"]:
        ablauf.Data.session["number_of_players_filter"].append(_nop)
    else:
        ablauf.Data.session["number_of_players_filter"].remove(_nop)


def show_info(segment):
    if ablauf.Data.session["game_count"] > 0:
        ablauf.Automate.jump("Info");

def filter_cancel(segment):
    ablauf.Data.session["name_filter"] = []
    ablauf.Data.session["number_of_players_filter"] = []

    for elem in ablauf.Data.session["old_selections"]["name_filter"]:
        ablauf.Data.session["name_filter"].append(elem)

    for elem in ablauf.Data.session["old_selections"]["number_of_players_filter"]:
        ablauf.Data.session["number_of_players_filter"].append(elem)

    ablauf.Automate.jump("end")


def start_game(segment):
        # start game
    _segment = ablauf.Automate.model.actual_segment
    _data = ablauf.Data.session["actual_game"]
    _dbemulators = ablauf.Data.db_objects["emulator"]
    _emulator = ablauf.Data.db_session.query(_dbemulators).filter(_dbemulators.system_id == _data.system.id).one()
    _executable = _emulator.executable
    _options = _emulator.emulatorconfiguration.configuration
    _game_files = ablauf.Data.db_objects["game_files"]
    _file = ablauf.Data.session["home"] + "/data/executables/" + ablauf.Data.db_session.query(_game_files).filter(_game_files.game_id == _data.id).one().file
    subprocess.call(shlex.split(_executable + " " + _options + " " + "\"" +_file + "\""))
