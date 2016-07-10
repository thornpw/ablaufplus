import os
import json
import sys
from jinja2 import Environment, PackageLoader
from copy import deepcopy
import jsonmerge

env = Environment(loader=PackageLoader('ablaufpad', 'templates'))

ablauf_environment = {'current_project': None}


def delete_code(filename, name, mode=0):
    dest = open(filename + ".tmp", 'wb')
    with open(filename, 'rb') as file:
        for line in file:
            line_text = line[:-1]
            if mode == 0:
                if line_text[:16] == "# <ab> start id:" and name == line_text[16:]:
                    mode = 1
                else:
                    dest.write(line_text + "\n")
            elif mode == 1:
                if line_text[:14] == "# <ab> end id:":
                    mode = 2
            elif mode == 2:
                mode = 0

    file.close()
    dest.close()

    os.remove(filename)
    os.rename(filename + ".tmp", filename)


def add_container_code(filename, taskname, code):
    if os.path.exists(filename + ".tmp"):
        os.remove(filename + ".tmp")

    dest = open(filename + ".tmp", 'wb')

    with open(filename, 'rb') as file:
        for line in file:
            line_text = line[:-1]

            if line_text[0:29 + taskname.__len__()] == "    # <ab> next container id:{0}".format(taskname):
                dest.write(code)

            dest.write(line_text + "\n")

    file.close()
    dest.close()

    os.remove(filename)
    os.rename(filename + ".tmp", filename)


def add_code(filename, code):
    with open(filename, 'a') as file:
        file.write(code)
        file.close()


def save_filled_template(path, template):
    with open(path, "wb") as fh:
        fh.write(template)
        fh.close()


def save_filled_json_template(path, template, data):
    _json = json.loads(template)
    _data = json.loads(data)

    for element in _data:
        _json[element] = _data[element]

    with open(path, 'w') as outfile:
        json.dump(_json, outfile)
        outfile.close()


def add_json_data(path, object_name, iterations, data):
    """

    :param path:
    :param object_name:
    :param iterations:
    :param data:
    :return:
    """
    _temp_path = path + "_temp"

    # load data
    with open(path, "r") as _file:
        _json = json.load(_file)

    # do the iterations
    for abl_counter in range(0, iterations):
        # make deep copy of the data to _data
        _data = json.loads(data)

        # preprocessing
        if isinstance(_data, list):
            for _counter in range(0, _data.__len__()):
                if isinstance(_data[_counter], unicode):
                    if _data[_counter] == "#ABL_COUNTER#":
                        _data[_counter] = abl_counter
                    elif _data[_counter] == "#ABL_COUNTER1#":
                        _data[_counter] = abl_counter + 1

        if isinstance(_data, unicode):
            if _data == "#ABL_COUNTER#":
                _data = abl_counter
            if _data == "#ABL_COUNTER1#":
                _data = abl_counter + 1

        elif isinstance(_data, dict):
            for element in _data:
                if _data[element] == "#ABL_COUNTER#":
                    _data[element] = abl_counter
                if _data[element] == "#ABL_COUNTER1#":
                    _data[element] = abl_counter + 1

        if iterations == 1:
            if isinstance(_data, unicode):
                exec ("_json{0} = '{1}'".format(object_name, _data))
            else:
                exec ("_json{0} = {1}".format(object_name, _data))
        else:
            exec ("_json{0}.append({1})".format(object_name, _data))

    try:
        with open(_temp_path, 'w') as outfile:
            json.dump(_json, outfile)

        os.remove(path)
        os.rename(_temp_path, path)

    except Exception as ex:
        print("Something went wrong to save:{0}".format(path))


def create_process(project_path, process_name, firststate):
    # folder:   [process name]
    os.mkdir(os.path.join(project_path, "processes", process_name))
    # template: App_controllers.py
    template = env.get_template('App_controllers.tmp')
    template = template.render()
    save_filled_template(os.path.join(project_path, "processes", process_name, "App_controllers.py"), template)
    # template: App_models.py
    template = env.get_template('App_model.tmp')
    template = template.render()
    save_filled_template(os.path.join(project_path, "processes", process_name, "App_models.py"), template)
    # template: App_process.json
    template = env.get_template('App_process.tmp')
    template = template.render(first_state=firststate)
    save_filled_template(os.path.join(project_path, "processes", process_name, "App_process.json"), template)
    # template: App_views.py
    template = env.get_template('App_views.tmp')
    template = template.render()
    save_filled_template(os.path.join(project_path, "processes", process_name, "App_views.py"), template)
    # template: __init__.py
    template = env.get_template('empty.tmp')
    template = template.render()
    save_filled_template(os.path.join(project_path, "processes", process_name, "__init__.py"), template)

    # folder structures
    os.mkdir(os.path.join(project_path, "processes", process_name, "structure"))


def import_process(project_path, path, process_name):
    # folder:   [process name]
    os.mkdir(os.path.join(project_path, "processes", process_name))
    # template: [process name]_controllers.py
    template = env.get_template(path + '/' + process_name + '/' + process_name + '_controllers.tmp')
    template = template.render()
    save_filled_template(os.path.join(project_path, "processes", process_name, process_name + "_controllers.py"), template)
    # template: [process name]_models.py
    template = env.get_template(path + '/' + process_name + '/' + process_name + '_model.tmp')
    template = template.render()
    save_filled_template(os.path.join(project_path, "processes", process_name, process_name + "_models.py"), template)
    # template: [process name]_process.json
    template = env.get_template(path + '/' + process_name + '/' + process_name + '_process.tmp')
    template = template.render()
    save_filled_template(os.path.join(project_path, "processes", process_name, process_name + "_process.json"), template)
    # template: [process name]_views.py
    template = env.get_template(path + '/' + process_name + '/' + process_name + '_views.tmp')
    template = template.render()
    save_filled_template(os.path.join(project_path, "processes", process_name, process_name + "_views.py"), template)
    # template: __init__.py
    template = env.get_template('empty.tmp')
    template = template.render()
    save_filled_template(os.path.join(project_path, "processes", process_name, "__init__.py"), template)

    # folder structures
    os.mkdir(os.path.join(project_path, "processes", process_name, "structure"))
    # loop over files
    for subdir, dirs, files in os.walk(os.path.join("ablaufpad", "templates", "Input_handler", process_name, "structure")):
        for file in files:
            template = env.get_template("Input_handler/" + process_name + "/structure/" + file)
            template = template.render()
            filename = file.split(".")
            save_filled_template(os.path.join(project_path, "processes", process_name, "structure", filename[0] + ".json"), template)

    # merge configuration
    for subdir, dirs, files in os.walk(os.path.join("ablaufpad", "templates", "Input_handler", process_name, "configuration")):
        for file in files:
            _process_data = open(subdir + "/" + file).read()
            process_data = json.loads(_process_data)
            _data = open(os.path.join(project_path, "configuration", file)).read()
            data = json.loads(_data)
            result = jsonmerge.merge(data, process_data)

            with open(os.path.join(project_path, "configuration", file), 'w') as outfile:
                json.dump(result, outfile)


def parse_tokens(tokens, data):
    if tokens.__len__() > 1:
        # add
        # =====================================================================================================================
        if tokens[0] == "add":
            if tokens[1] == "json":
                # add a json object into a json file
                # -------------------------------------------------------------------------------------------------------------
                # syntax: add json [data_type] [object-name] [iterations]
                # -------------------------------------------------------------------------------------------------------------
                if tokens.__len__() == 5:
                    _data_type = tokens[2]
                    _object_name = str(tokens[3])
                    _iterations = int(tokens[4])

                    _path_to_data = os.path.join(ablauf_environment["current_project"], "configuration", _data_type + ".json")

                    if os.path.exists(_path_to_data):
                        add_json_data(_path_to_data, _object_name, _iterations, data)
                        print("JSON data added:{0}".format(_object_name))
                    else:
                        print("data file:{0} does not exists".format(_path_to_data))
                else:
                    print("wrong number of arguments:{0}. 2 arguments are exspected".format(tokens.__len__()))

            elif tokens[1] == "container":
                # add a container into a dot
                # -------------------------------------------------------------------------------------------------------------
                # syntax: add container subcontroller-name [existing workflow] user-task container-name [row] [column]
                # -------------------------------------------------------------------------------------------------------------
                if tokens.__len__() == 8:
                    _subcontroller_name = tokens[2]
                    _workflow = tokens[3]
                    _user_task = tokens[4]
                    _container_name = tokens[5]
                    _row = int(tokens[6])
                    _column = int(tokens[7])

                    if os.path.exists(os.path.join(ablauf_environment["current_project"], "processes", _workflow)):
                        _file = os.path.join(ablauf_environment["current_project"], "processes", _workflow, "structure", _user_task + ".json")
                        if os.path.exists(_file):
                            try:
                                subcontroller_template = env.get_template("subcontroller/dot/{0}_dot.tmp".format(_subcontroller_name))
                            except Exception as ex:
                                print("Sub controller:{0} does not exists".format(_subcontroller_name))
                            finally:
                                # dot
                                json_data = open(_file).read()
                                _temp_data = json.loads(json_data)
                                children = _temp_data["children"]
                                new_code = subcontroller_template.render(containername=_container_name)
                                new_code_json = json.loads(new_code)
                                _data_as_json = json.loads(data)

                                for element in _data_as_json:
                                    new_code_json[element] = _data_as_json[element]

                                if children.__len__() <= _row:
                                    # add new row and column. the column parameter will be interpreted as 0
                                    children.append([new_code_json])
                                else:
                                    # append new column
                                    children[_row].insert(_column, new_code_json)

                                try:
                                    os.rename(_file, _file + "_old")
                                    with open(_file, 'w') as outfile:
                                        json.dump(_temp_data, outfile)
                                        outfile.close()
                                    os.remove(_file + "_old")
                                except Exception as ex:
                                    print("Error during creation of file: {0}".format(_file))

                                # view
                                _file = os.path.join(ablauf_environment["current_project"], "processes", _workflow, "App_views.py")

                                template = env.get_template("subcontroller/views/{0}_view.tmp".format(_subcontroller_name))
                                new_code = template.render(containername=_container_name, row=_row, column=_column)

                                try:
                                    add_container_code(_file, _user_task, new_code)
                                except Exception as ex:
                                    print("Error during creation of file: {0}".format(_file))

                                print("container added successful:{0}".format(_container_name))
                        else:
                            print("User task:{0} does not exists".format(_user_task))
                    else:
                        print("Workflow:{0} does not exists".format(_workflow))
                else:
                    print("wrong number of arguments:{0}. 8 arguments are exspected".format(tokens.__len__()))

            elif tokens[1] == "controller":
                if tokens[2] == "task":
                    # add task controller
                    # -------------------------------------------------------------------------------------------------------------
                    # syntax: add controller task [existing workflow] [new task name] [Jump|Transit] [Destination]
                    # -------------------------------------------------------------------------------------------------------------
                    if tokens.__len__() == 7:
                        if os.path.exists(os.path.join(ablauf_environment["current_project"], "processes", tokens[3])):
                            template = env.get_template('add_game.tmp')
                            new_code = template.render(workflow=tokens[3], name=tokens[4], mode=tokens[5],destination=tokens[6])
                            add_code(os.path.join(ablauf_environment["current_project"], "processes", tokens[3],"App_controllers.py"), new_code)

                            # model
                            template = env.get_template('add_game_model.tmp')
                            new_code = template.render(taskname=tokens[4])
                            add_code(os.path.join(ablauf_environment["current_project"], "processes", tokens[3],"App_models.py"), new_code)

                            # apn
                            json_data = open(os.path.join(ablauf_environment["current_project"], "processes", tokens[3], "App_process.json")).read()

                            data = json.loads(json_data)
                            new_task = {'name': tokens[4], 'type': 'Task', 'exit_transition': {'type': tokens[5], 'destination': tokens[6]}}
                            data["states"].append(new_task)

                            with open(os.path.join(ablauf_environment["current_project"], "processes", tokens[3], "App_process.json"), 'w') as outfile:
                                json.dump(data, outfile)

                            print("task controller added successful")
                        else:
                            print("Workflow does not exists")
                    else:
                        print("wrong number of arguments")

                elif tokens[2] == "subprocess":
                    # add subprocess controller
                    # -------------------------------------------------------------------------------------------------------------
                    # syntax: add controller subprocess [existing workflow] [new task name] [Jump|Transit] [Destination]
                    # -------------------------------------------------------------------------------------------------------------
                    if tokens.__len__() == 7:
                        if os.path.exists(os.path.join(ablauf_environment["current_project"], "processes", tokens[3])):
                            # controller
                            template = env.get_template('add_subprocess.tmp')
                            new_code = template.render(workflow=tokens[3], name=tokens[4], mode=tokens[5], destination=tokens[6])
                            add_code(os.path.join(ablauf_environment["current_project"], "processes", tokens[3], "App_controllers.py"), new_code)

                            # model
                            template = env.get_template('add_subprocess_model.tmp')
                            new_code = template.render(taskname=tokens[4])
                            add_code(os.path.join(ablauf_environment["current_project"], "processes", tokens[3], "App_models.py"), new_code)

                            # apn
                            json_data = open(os.path.join(ablauf_environment["current_project"], "processes", tokens[3], "App_process.json")).read()
                            data = json.loads(json_data)
                            new_task = {'name': tokens[4], 'type': 'SubProcess', 'exit_transition': {'type': tokens[5], 'destination': tokens[6]}}
                            data["states"].append(new_task)

                            with open(os.path.join(ablauf_environment["current_project"], "processes", tokens[3], "App_process.json"), 'w') as outfile:
                                json.dump(data, outfile)

                            print("subprocess controller added successful")
                        else:
                            print("Workflow does not exists")
                    else:
                        print("wrong number of arguments")

                elif tokens[2] == "game":
                    # add task controller
                    # -------------------------------------------------------------------------------------------------------------
                    # syntax: add controller game [existing workflow] [new task name] [Jump|Transit] [Destination]
                    # -------------------------------------------------------------------------------------------------------------
                    if tokens.__len__() == 7:
                        if os.path.exists(os.path.join(ablauf_environment["current_project"], "processes", tokens[3])):
                            template = env.get_template('add_task.tmp')
                            new_code = template.render(workflow=tokens[3], name=tokens[4], mode=tokens[5],
                                                       destination=tokens[6])
                            add_code(os.path.join(ablauf_environment["current_project"], "processes", tokens[3],"App_controllers.py"), new_code)

                            # model
                            template = env.get_template('add_task_model.tmp')
                            new_code = template.render(taskname=tokens[4])
                            add_code(os.path.join(ablauf_environment["current_project"], "processes", tokens[3],"App_models.py"), new_code)

                            # apn
                            json_data = open(os.path.join(ablauf_environment["current_project"], "processes", tokens[3],"App_process.json")).read()

                            data = json.loads(json_data)
                            new_task = {'name': tokens[4], 'type': 'Game','exit_transition': {'type': tokens[5], 'destination': tokens[6]}}
                            data["states"].append(new_task)
                            with open(os.path.join(ablauf_environment["current_project"], "processes", tokens[3],"App_process.json"), 'w') as outfile:
                                json.dump(data, outfile)
                            print("game controller added successful")
                        else:
                            print("Workflow does not exists")
                    else:
                        print("wrong number of arguments")

                elif tokens[2] == "usertask":
                    # add task controller
                    # -------------------------------------------------------------------------------------------------------------
                    # syntax: add controller usertask [existing workflow] [new user task name] [root container name] [Jump|Transit] [Destination]
                    # -------------------------------------------------------------------------------------------------------------
                    if tokens.__len__() == 8:
                        if os.path.exists(os.path.join(ablauf_environment["current_project"], "processes", tokens[3])):
                            # controller
                            template = env.get_template('add_usertask.tmp')
                            new_code = template.render(workflow=tokens[3], name=tokens[4], mode=tokens[6], destination=tokens[7])
                            add_code(os.path.join(ablauf_environment["current_project"], "processes", tokens[3], "App_controllers.py"), new_code)

                            # model
                            template = env.get_template('add_usertask_model.tmp')
                            new_code = template.render(taskname=tokens[4])
                            add_code(os.path.join(ablauf_environment["current_project"], "processes", tokens[3], "App_models.py"), new_code)

                            # view
                            template = env.get_template('add_usertask_view.tmp')
                            new_code = template.render(taskname=tokens[4], containername=tokens[5])
                            add_code(os.path.join(ablauf_environment["current_project"], "processes", tokens[3], "App_views.py"), new_code)

                            # structure
                            template = env.get_template('dot.tmp')
                            template = template.render(containername=tokens[5])
                            save_filled_json_template(os.path.join(ablauf_environment["current_project"], "processes", tokens[3], "structure", tokens[4] + ".json"), template, data)

                            # apn
                            json_data = open(os.path.join(ablauf_environment["current_project"], "processes", tokens[3], "App_process.json")).read()
                            _json_data = json.loads(json_data)

                            new_task = {'name': tokens[4], 'type': 'Task','exit_transition': {'type': tokens[6], 'destination': tokens[7]}}
                            _json_data["states"].append(new_task)
                            with open(os.path.join(ablauf_environment["current_project"], "processes", tokens[3], "App_process.json"), 'w') as outfile:
                                json.dump(_json_data, outfile)

                            print("user task:{0} controller added successful".format(tokens[4]))
                        else:
                            print("Workflow does not exists")
                    else:
                        print("wrong number of arguments")
                elif tokens[2] == "inclusivegateway":
                    # add task controller
                    # -------------------------------------------------------------------------------------------------------------
                    # syntax: add controller inclusivegateway [existing workflow] [new task name] [(Jump|Transit,destination{;}*)] [Jump|Transit] [Deafult Destination]
                    # -------------------------------------------------------------------------------------------------------------
                    if tokens.__len__() == 8:
                        if os.path.exists(os.path.join(ablauf_environment["current_project"], "processes", tokens[3])):
                            _new_choices = tokens[5].split(";")
                            if _new_choices.__len__() > 0:
                                _exit = False

                                for choice in _new_choices:
                                    _tuple = choice.split(",")
                                    if _tuple.__len__() != 2:
                                        _exit = True
                                        break

                                if not _exit:
                                    # controller
                                    template = env.get_template('add_inclusivegateway.tmp')
                                    new_code = template.render(workflow=tokens[3], name=tokens[4], choices=tokens[5],mode=tokens[6], destination=tokens[7])
                                    add_code(os.path.join(ablauf_environment["current_project"], "processes", tokens[3],"App_controllers.py"), new_code)
                                    # apn
                                    json_data = open(os.path.join(ablauf_environment["current_project"], "processes", tokens[3],"App_process.json")).read()
                                    data = json.loads(json_data)

                                    _choices = {}
                                    for choice in _new_choices:
                                        _tuple = choice.split(",")
                                        _choices[_tuple[0]] = _tuple[1]

                                    _new_task = {'name': tokens[4], 'type': 'InclusiveGateway', 'choices': _choices,'default_transition': {'type': tokens[6], 'destination': tokens[7]}}
                                    data["states"].append(_new_task)
                                    with open(os.path.join(ablauf_environment["current_project"], "processes", tokens[3],"App_process.json"), 'w') as outfile:
                                        json.dump(data, outfile)

                                    print("inclusive gateway controller added successful")
                                else:
                                    print("Workflow does not exists")
                            else:
                                print("wrong choice")
                        else:
                            print("wrong choice pairs")
                    else:
                        print("wrong number of arguments")
                else:
                    print("can't add unknown controller type")
            else:
                print("can't add unknown object")

        # delete
        # =====================================================================================================================
        elif tokens[0] == "delete":
            if tokens[1] == "controller":
                # delete apn task
                # -------------------------------------------------------------------------------------------------------------
                # syntax: delete controller [existing workflow] [existing task name]
                # -------------------------------------------------------------------------------------------------------------
                if tokens.__len__() == 4:
                    if ablauf_environment["current_project"] is not None:
                        # controller
                        template = env.get_template('add_task.tmp')
                        new_code = template.render(name=tokens[3])
                        delete_code(os.path.join(ablauf_environment["current_project"], "processes", tokens[2],"App_controllers.py"), tokens[3])
                        # apn
                        json_data = open(os.path.join(ablauf_environment["current_project"], "processes", tokens[2],"App_process.json")).read()

                        data = json.loads(json_data)
                        task_to_delete = -1
                        found = False
                        for task in data["states"]:
                            task_to_delete += 1
                            if task["name"] == tokens[3]:
                                found = True
                                break;

                        if found:
                            del data["states"][task_to_delete]
                            with open(os.path.join(ablauf_environment["current_project"], "processes", tokens[2],"App_process.json"), 'w') as outfile:
                                json.dump(data, outfile)

                        print("controller deleted successful")
                    else:
                        print("no project connected")
                else:
                    print("wrong number of arguments")
            else:
                print("can't delete unknown object")

        # connect
        # =====================================================================================================================
        elif tokens[0] == "connect":
            if tokens[1] == "project":
                # connect project
                # -------------------------------------------------------------------------------------------------------------
                # syntax: connect project [existing project name]
                # -------------------------------------------------------------------------------------------------------------
                if tokens.__len__() == 3:
                    if os.path.exists((tokens[2])):
                        ablauf_environment["current_project"] = tokens[2]
                        print(tokens[2] + " successfully connected")
                    else:
                        print("Project could not be found")
                else:
                    print("wrong number of arguments")
            else:
                print("only a project could be connected")

        # create
        # =====================================================================================================================

        elif tokens[0] == "create":
            if tokens[1] == "project":
                # create project
                # -------------------------------------------------------------------------------------------------------------
                # syntax: create project [new project name] [kernel] [input_handler] [first state]
                # -------------------------------------------------------------------------------------------------------------
                if tokens.__len__() == 6:
                    _project_name = tokens[2]
                    _kernel = tokens[3]
                    _input_handler = tokens[4]
                    _first_state = tokens[5]

                    if 0 < _project_name.__len__() < 32:
                        if _kernel in ['pygamekern', 'console_kernel']:
                            if _input_handler in ['steuer', 'none_input_handler']:
                                if 0 < _first_state.__len__() < 32:
                                    # folder:   [project name]
                                    if not os.path.exists(_project_name):
                                        os.mkdir(_project_name)
                                        # template: __init__.py
                                        template = env.get_template('init.tmp')
                                        template = template.render()
                                        save_filled_template(os.path.join(_project_name, "__init__.py"), template)
                                        # template: logging.conf
                                        template = env.get_template('logging.tmp')
                                        template = template.render()
                                        save_filled_template(os.path.join(_project_name, "logging.conf"), template)
                                        # template: controller.py
                                        template = env.get_template('empty.tmp')
                                        template = template.render()
                                        save_filled_template(os.path.join(_project_name, "controller.py"), template)

                                        # folder:   configuration
                                        os.mkdir(os.path.join(_project_name, "configuration"))
                                        # template: configuration.json
                                        template = env.get_template('configuration.tmp')
                                        template = template.render(projectname=_project_name, kernel=_kernel,input_handler=_input_handler)
                                        save_filled_template(
                                            os.path.join(_project_name, "configuration", "configuration.json"),
                                            template)
                                        # template: session.json
                                        template = env.get_template('session.tmp')
                                        template = template.render()
                                        save_filled_template(
                                            os.path.join(_project_name, "configuration", "session.json"), template)
                                        # template:	translations.json
                                        template = env.get_template('translation.tmp')
                                        template = template.render()
                                        save_filled_template(
                                            os.path.join(_project_name, "configuration", "translations.json"), template)

                                        # folder:   processes
                                        os.mkdir(os.path.join(_project_name, "processes"))
                                        # template: __init__.py
                                        template = env.get_template('empty.tmp')
                                        template = template.render()
                                        save_filled_template(os.path.join(_project_name, "processes", "__init__.py"),
                                                             template)

                                        # App process
                                        create_process(_project_name, "App", _first_state)

                                        # Import processes
                                        import_process(_project_name, "Input_handler", "Stema")

                                        print("project successful created in {0}".format(
                                            os.path.join(os.getcwd(), _project_name)))
                                    else:
                                        print ("project already exists")
                                else:
                                    print("length of the first state must be between 1 and 32 characters")
                            else:
                                print("unknown input_handler")
                        else:
                            print("kernel unknown")
                    else:
                        print("length of projectname must be between 1 and 32 characters")
                else:
                    print("wrong number of arguments")
            elif tokens[1] == "process":
                if ablauf_environment["current_project"] is not None:
                    # create process
                    # -------------------------------------------------------------------------------------------------------------
                    # syntax: create process [new process name]
                    # -------------------------------------------------------------------------------------------------------------
                    if tokens.__len__() == 3:
                        if 0 < tokens[2].__len__() < 32:
                            create_process(ablauf_environment["current_project"], tokens[2])
                            print("process successful created")
                    else:
                        print("wrong number of arguments")
                else:
                    print("no project connected")
            else:
                print("can't create unknown object")
        else:
            print("unknown command")


if sys.argv.__len__() == 2:
    # script mode
    if os.path.exists(sys.argv[1]):
        with open(sys.argv[1], 'r') as file:
            for line in file:
                if line.__len__() > 0 and not line.startswith("#"):
                    line = line[0:-1]
                    if "'" in line:
                        _parts = line.split("'", 1)
                        if _parts.__len__() > 1:
                            _tokens = _parts[0].split(" ")
                            _tokens = _tokens[:-1]
                            _data = _parts[1][0:-1]
                            parse_tokens(_tokens, _data)
                            # if _parts.__len__() >  1:
                            #    _tokens = _parts[0].split(" ")
                            #    #_parts[1] = _parts[1].replace("\'","\"")
                            #    _parts[1] = _parts[1][:-1]
                            #    _data = json.loads(_parts[1])
                            #    parse_tokens(_tokens,_data)
                    else:
                        _tokens = line.split(" ")
                        _data = None
                        parse_tokens(_tokens, _data)
    else:
        print("scriptfile does not exists")

else:
    # interactive mode
    while True:
        tokens = raw_input("do:")
        if "'" in tokens:
            _parts = tokens.split("'", 1)
            if _parts.__len__() > 1:
                _tokens = _parts[0].split(" ")
                _tokens = _tokens[:-1]
                _data = _parts[1][0:-1]
                parse_tokens(_tokens, _data)
        else:
            _tokens = tokens.split(" ")
            _data = None
            parse_tokens(_tokens, _data)
