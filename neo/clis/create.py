import os
from .base import Base
from neo.libs import utils, ncurses, prompt
from neo.libs import orchestration as orch
from tabulate import tabulate


class Create(Base):
    """
usage:
        create [-i] [-f PATH]
        create [-t TEMPLATE] [-i]
        create kubernetes
        create vm

Create stack

Options:
-h --help                           Print usage
-f PATH --file=PATH                 Set neo manifest file
-t TEMPLATE --template TEMPLATE     Create neo.yml, TEMPLATE is ENUM(clusters,instances,networks)
-i --interactive                    Interactive form with ncurses mode

Commands:
  kubernetes                        Create kubernetes stack
  vm                                Create VM

Tips!
    neo create -t instances         create instances

Run 'neo create COMMAND --help' for more information on a command.
"""

    def execute(self):
        if self.args["--template"]:
            if self.args["--template"] in ("clusters", "instances", "networks"):
                tmpl = self.args["--template"]

                if self.args["--interactive"]:
                    ncurses.init(stack=tmpl)
                else:
                    prompt.init(stack=tmpl)
            exit()

        if self.args["kubernetes"]:
            if self.args["--interactive"]:
                print(ncurses.init(stack="clusters", project="kubernetes"))
            else:
                print(prompt.init(stack="clusters", project="kubernetes"))

        if self.args["vm"]:
            if self.args["--interactive"]:
                print(ncurses.init(stack="instances", project="vm"))
            else:
                print(prompt.init(stack="instances", project="vm"))

        headers = ["ID", "Name", "Status", "Created", "Updated"]

        set_file = self.args["--file"]
        default_file = orch.check_manifest_file()

        if set_file:
            if os.path.exists(set_file):
                default_file = set_file
            else:
                utils.log_err("{} file is not exists!".format(set_file))
                exit()

        if not default_file:
            utils.log_err("Can't find neo.yml manifest file!")
            q_stack = utils.question("Do you want to generate neo.yml manifest? ")

            if q_stack:
                if self.args["--interactive"]:
                    print(ncurses.init())
                else:
                    print(prompt.init())
                q_deploy = utils.question("Continue to deploy? ")
                if q_deploy:
                    default_file = "neo.yml"
                else:
                    exit()
            else:
                exit()
        else:
            q_deploy = utils.question("Continue to deploy? ")
            if q_deploy:
                default_file = "neo.yml"
            else:
                exit()

        deploy_init = orch.initialize(default_file)
        try:
            orch.do_create(deploy_init)
        except Exception as e:
            utils.log_err(e)
            utils.log_err("Deploying Stack failed...")
            exit()

        projects = utils.get_project(default_file)

        project_list = list()
        for project in projects:
            proj = orch.get_stack(project)
            if proj:
                project_list.append(proj)

        if len(project_list) > 0:
            print(tabulate(project_list, headers=headers, tablefmt="grid"))
