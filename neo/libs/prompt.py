import os
from neo.libs import utils
from neo.libs.lambdafunc import *


def get_stack():
    try:
        d_stack = utils.get_index(utils.repodata())
        f_stack = [
            {
                "type": "TitleSelectOne",
                "name": "Select Stack ",
                "key": "stack",
                "values": d_stack,
            }
        ]
        stack = utils.prompt_generator("", f_stack)
        return stack[f_stack[0]["key"]]
    except:
        return None


def get_project(templates):
    try:
        d_template = utils.get_index(utils.repodata()[templates])
        f_template = [
            {
                "type": "TitleSelectOne",
                "name": "-------------------",
                "key": "template",
                "values": d_template,
            }
        ]
        template = utils.prompt_generator("Select Templates ", f_template)
        return template[f_template[0]["key"]]
    except:
        return None


def setup_form(stack, project, parent=None):
    init = {
        "form": [],
        "depend": [],
        "number": [],
        "stack": stack,
        "project": project,
        "parent": parent,
    }

    if parent:
        init["parent"] = parent

    repo = utils.repodata()[stack][project]
    default_form_name = {"type": "TitleText", "name": "Name", "key": "name"}
    if utils.check_key(repo, "lists"):
        repo_lists = repo["lists"]
        """
            if type of 'repo_list' is list
        """
        if isinstance(repo_lists, list):
            init["form"].append(
                {
                    "type": "TitleSelect",
                    "name": "Name",
                    "key": "name",
                    "values": repo_lists,
                }
            )
        else:
            """
                if type of 'repo_list' is string
            """
            repo_lists = globals()[repo["lists"]]()
            if len(repo_lists) > 0:
                init["form"].append(
                    {
                        "type": "TitleSelect",
                        "name": "Name",
                        "key": "name",
                        "values": repo_lists,
                    }
                )
            else:
                init["form"].append(default_form_name)
    else:
        init["form"].append(default_form_name)

    if utils.check_key(repo, "parameters"):
        param = repo["parameters"]
        param_index = utils.get_index(param)
        for index in param_index:
            prop = param[index]
            if not utils.check_key(prop, "default"):
                if not utils.check_key(prop, "dependences"):
                    init["form"].append(
                        {"type": "TitleText", "name": prop["label"], "key": index}
                    )
                    if prop["type"] == "number":
                        init["number"].append(index)
                else:
                    depend = prop["dependences"]
                    if depend.split(":")[0] == "func":
                        func_name = depend.split(":")[1]
                        init["form"].append(
                            {
                                "type": "TitleSelectOne",
                                "name": prop["label"],
                                "key": index,
                                "scroll_exit": True,
                                "values": globals()[func_name](),
                                "max_height": 7,
                                "value": [0],
                            }
                        )
                    if depend.split(":")[0] == "repo":
                        repo_name = depend.split(":")[1]
                        init["depend"].append(
                            {"name": prop["label"], "key": index, "repo": repo_name}
                        )
    return init


def exec_form(stack, project):
    form = {}
    f_init = list()
    parent_form = setup_form(stack, project)
    f_init.append(parent_form)
    if len(parent_form["depend"]) > 0:
        for depend in parent_form["depend"]:
            repo = depend["repo"].split(".")
            depend_stack = repo[0]
            depend_project = repo[1]
            depend_parent = depend["key"]
            depend_form = setup_form(depend_stack, depend_project, parent=depend_parent)
            f_init.append(depend_form)
    form["init"] = list(reversed(f_init))
    return form


def dump(data):
    d_dump = {"deploy": []}
    d_depend = []
    for d_yml in data:
        if d_yml["just_child_val"]:
            d_depend.append({"key": d_yml["parent"], "val": d_yml["name"]})
        else:
            pre_yml = {d_yml["name"]: {"template": d_yml["template"]}}
            for k, v in d_yml.items():
                if k not in ["name", "template", "stack", "parent", "just_child_val"]:
                    if not utils.check_key(pre_yml[d_yml["name"]], "parameters"):
                        pre_yml[d_yml["name"]]["parameters"] = {k: v}
                    else:
                        pre_yml[d_yml["name"]]["parameters"].update({k: v})

            if not utils.check_key(d_dump, d_yml["stack"]):
                d_dump[d_yml["stack"]] = pre_yml
            else:
                d_dump[d_yml["stack"]].update(pre_yml)

            if d_yml["parent"]:
                d_depend.append({"key": d_yml["parent"], "val": d_yml["name"]})
            else:
                if len(d_depend) > 0:
                    for k_depend in d_depend:
                        pre_yml[d_yml["name"]]["parameters"].update(
                            {k_depend["key"]: k_depend["val"]}
                        )

            d_dump["deploy"].append("{}.{}".format(d_yml["stack"], d_yml["name"]))
    return d_dump


def init(stack=None, project=None):
    select_stack = stack
    if not select_stack:
        select_stack = get_stack()

    select_project = project
    if not select_project:
        select_project = get_project(select_stack)

    fields = exec_form(select_stack, select_project)

    data = list()

    for field in fields["init"]:
        validate = False
        while not validate:
            f_form = eval(str(field["form"]))
            name_type = f_form[0]
            """
                Generate form if just_child_val is False
            """
            if name_type["type"] == "TitleSelect":
                name_values = name_type["values"]
                form = utils.prompt_generator(
                    "Setup {}".format(field["project"]), [name_type]
                )
                if form["name"] in name_values:
                    form["just_child_val"] = True
                    validate = True
                else:
                    new_form = eval(str(field["form"]))
                    del new_form[0]
                    new_form_val = utils.prompt_generator(
                        "Setup {}".format(field["project"]), new_form
                    )
                    form.update(new_form_val)
                    form["just_child_val"] = False
            else:
                form = utils.prompt_generator(
                    "Setup {}".format(field["project"]), f_form
                )
                form["just_child_val"] = False

            if field["parent"]:
                form["parent"] = field["parent"]
            else:
                form["parent"] = None

            if not form["just_child_val"]:
                form["stack"] = field["stack"]
                form["template"] = field["project"]
                """ Check if data is null """
                null_data = 0
                for k_data, v_data in form.items():
                    if v_data == "":
                        null_data += 1
                    if len(field["number"]) > 0:
                        if k_data in field["number"]:
                            if utils.isint(v_data):
                                form[k_data] = int(v_data)
                            elif utils.isfloat(v_data):
                                form[k_data] = float(v_data)
                            else:
                                null_data += 1

                if null_data == 0:
                    validate = True

            if validate:
                data.append(form)

    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
    utils.yaml_create("neo.yml", dump(data))
    return utils.read_file("neo.yml")
