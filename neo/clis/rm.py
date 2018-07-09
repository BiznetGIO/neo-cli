import os
from .base import Base
from neo.libs import network as network_lib
from neo.libs import vm as vm_lib
from neo.libs import utils
from neo.libs import orchestration as orch


class Rm(Base):
    """
usage:
    rm [-f PATH]
    rm vm <VM_ID>
    rm network <NETWORK_ID>
    rm stack <STACK_NAME>

Remove Stack, VM, or Network

Options:
-h --help                       Print usage
-f PATH --file=PATH             Set neo manifest file

Commands:
 vm VM_ID                       Remove virtual machines
 network NETWORK_ID             Remove network
 stack STACK_NAME               Remove stack

Run 'neo rm COMMAND --help' for more information on a command.
"""

    def execute(self):

        set_file = self.args["--file"]
        default_file = orch.check_manifest_file()

        if self.args["vm"]:
            instance_id = self.args["<VM_ID>"]
            try:
                answer = ""
                while answer not in ["y", "n"]:
                    answer = input(
                        "Are you sure to delete this virtual machines [y/n]? ")
                    .lower()

                if answer == "y":
                    vm_lib.do_delete(instance_id)
                    utils.log_info("VM has been deleted")
            except Exception as e:
                utils.log_err(e)
            else:
                pass
            finally:
                pass
            exit()

        if self.args["network"]:
            network_id = self.args["<NETWORK_ID>"]
            try:
                answer = ""
                while answer not in ["y", "n"]:
                    answer = input(
                        "Are you sure to delete this network [y/n]? ")
                    .lower()

                if answer == "y":
                    network_lib.do_delete(network_id)
                    utils.log_info("network has been deleted")
            except Exception as e:
                utils.log_err(e)
            else:
                pass
            finally:
                pass
            exit()

        if self.args["stack"]:
            stack_name = self.args["<STACK_NAME>"]
            try:
                answer = ""
                while answer not in ["y", "n"]:
                    answer = input(
                        "Are you sure to delete \"{}\" stack [y/n]? "
                        .format(stack_name)).lower()

                if answer == "y":
                    proj = orch.do_delete(stack_name)
                    if proj:
                        utils.log_info("Stack {} has been deleted".format(stack_name))
                    else:
                        utils.log_err("Stack {} is not exists".format(stack_name))
            except Exception as e:
                utils.log_err(e)
            else:
                pass
            finally:
                pass
            exit()

        if set_file:
            if os.path.exists(set_file):
                default_file = "{}".format(set_file)
            else:
                utils.log_err("{} file is not exists!".format(set_file))
                print(self.__doc__)
                exit()

        if not default_file:
            utils.log_err("Can't find neo.yml manifest file!")
            print(self.__doc__)
            exit()

        projects = utils.get_project(default_file)
        project_answer = ",".join(projects)
        answer = ""
        while answer not in ["y", "n"]:
            answer = input("Are you sure to delete {} [y/n]? "
                           .format(project_answer)).lower()

        if answer == "y":
            for project in projects:
                proj = orch.do_delete(project)
                if proj:
                    utils.log_info("Stack {} has been deleted".format(project))
                else:
                    utils.log_err("Stack {} is not exists".format(project))
