import os
import bitmath
from .base import Base
from neo.libs import network as network_lib
from neo.libs import vm as vm_lib
from neo.libs import utils, image
from neo.libs import orchestration as orch
from tabulate import tabulate


class Ls(Base):
    """
usage:
        ls [-f PATH]
        ls stack
        ls vm
        ls network

List all stack

Options:
-h --help               Print usage
-f PATH --file=PATH     Set neo manifest file

Commands:
 stack                  List all Stacks
 vm                     List all virtual machines
 network                List all network

Run 'neo ls COMMAND --help' for more information on a command.
"""

    def execute(self):
        headers = ["ID", "Name", "Status", "Created", "Updated"]
        if self.args["stack"]:
            print(tabulate(orch.get_list(), headers=headers, tablefmt="grid"))
            exit()

        set_file = self.args["--file"]
        default_file = orch.check_manifest_file()

        if self.args["vm"]:
            data_instance = list()
            for instance in vm_lib.get_list():
                pre_instance = [instance.id, instance.name]
                pre_instance.append(image.detail(instance.image["id"]).name)
                flavors = vm_lib.detail_flavor(instance.flavor["id"])
                flavors_name = flavors.name
                flavors_vcpu = flavors.vcpus
                flavors_ram = bitmath.MiB(flavors.ram).to_GiB().best_prefix()
                pre_instance.append(flavors_name)
                pre_instance.append(flavors_ram)
                pre_instance.append(flavors_vcpu)

                # Address
                addr = list()
                addr_objs = utils.get_index(instance.addresses)
                if len(addr_objs) > 0:
                    for addr_obj in addr_objs:
                        addr.append("network : {}".format(addr_obj))
                        for addr_ip in instance.addresses[addr_obj]:
                            addr_meta = "{} IP : {}".format(
                                addr_ip["OS-EXT-IPS:type"], addr_ip["addr"])
                            addr.append(addr_meta)
                if len(addr) > 0:
                    pre_instance.append("\n".join(addr))
                else:
                    pre_instance.append("")

                pre_instance.append(instance.status)
                data_instance.append(pre_instance)

            if len(data_instance) == 0:
                utils.log_err("No Data...")
                print(self.__doc__)
                exit()
            print(
                tabulate(
                    data_instance,
                    headers=[
                        "ID", "Name", "Image", "Flavor", "RAM (GiB)", "vCPU",
                        "Addresses", "Status"
                    ],
                    tablefmt="grid"))
            exit()

        if self.args["network"]:
            data_network = [[
                network['id'], network['name'], network['status']
            ] for network in network_lib.get_list()]
            if len(data_network) == 0:
                utils.log_err("No Data...")
                print(self.__doc__)
                exit()
            print(
                tabulate(
                    data_network,
                    headers=["ID", "Name", "Status"],
                    tablefmt="grid"))
            exit()

        if set_file:
            if os.path.exists(set_file):
                default_file = "{}".format(set_file)
            else:
                utils.log_err("{} file is not exists!".format(set_file))
                print(self.__doc__)
                exit()

        if not default_file:
            utils.log_err("Oops!! Can't find neo.yml manifest file!")
            print(self.__doc__)
            exit()

        projects = utils.get_project(default_file)

        project_list = list()
        for project in projects:
            proj = orch.get_stack(project)
            if proj:
                project_list.append(proj)

        if len(project_list) > 0:
            print(tabulate(project_list, headers=headers, tablefmt="grid"))
        else:
            utils.log_err("No Data...")
            print(self.__doc__)
