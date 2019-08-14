import os
import time
import socket
import tempfile
import subprocess
from .base import Base
from neo.libs import vm as vm_lib
from neo.libs import utils
from neo.libs import orchestration as orch


class Attach(Base):
    """
usage:
        attach [-f PATH] [-c COMMAND] [-t HOST]
        attach ssh <USER@HOSTS>
        attach vm <VM_ID>

Attach local standard input, output, and error streams to a running machine

Options:
-c COMMAND --command=COMMAND          Send command
-h --help                             Print usage
-f PATH --file=PATH                   Set neo manifest file
-k KEY_FILE --key=KEY_FILE            Setup keyfile to ssh service
-t HOST --tunneling=HOST              SSH Tunneling (eg. -t 8001:127.0.0.1:8001)

Commands:
  vm <VM_ID>                          Attach to Virtual Machine
  ssh <USER@HOSTS>                    Attach to machine by ssh

Run 'neo attach COMMAND --help' for more information on a command.
"""

    def execute(self):
        """
            Remote client over SSH
        """

        if self.args["ssh"]:
            cridential = self.args["<USER@HOSTS>"].split("@")
            if len(cridential) != 2:
                print(self.__doc__)
                exit(0)

            user = cridential[0]
            hostname = cridential[1]
            utils.ssh_shell(hostname, user)
            exit(0)

        """
            Remote VM over SSH
        """
        if self.args["vm"]:
            vm_id = self.args["<VM_ID>"]
            """
                cek vm metadata from stack
            """
            utils.log_info("Check your key pairs")
            vm_detail = vm_lib.detail(vm_id).to_dict()
            key_pair_temp = tempfile.NamedTemporaryFile(delete=True)

            try:
                key_name = vm_detail["key_name"]
                out = orch.get_private_key(key_name)
                if out:
                    with open(key_pair_temp.name, "w") as pkey:
                        pkey.write(out)
                        os.chmod(key_pair_temp.name, 0o600)
                        utils.log_info("Done...")
                else:
                    utils.log_err("Can't find key pairs on your Virtual Machine!")
                    exit()

            except Exception as e:
                utils.log_err("Can't find key pairs on your Virtual Machine!")
                exit()

            # Address
            addr = list()
            addr_objs = utils.get_index(vm_detail["addresses"])
            if len(addr_objs) > 0:
                for addr_obj in addr_objs:
                    for addr_ip in vm_detail["addresses"][addr_obj]:
                        if addr_ip["OS-EXT-IPS:type"] == "floating":
                            addr_meta = addr_ip["addr"]
                            addr.append(addr_meta)

            if not (len(addr) > 0):
                utils.log_err("Can't find floating IP Address!")
                exit()

            utils.log_info("Check username")
            user = orch.get_metadata(vm_detail["name"], "user")
            if not user:
                user = ""
                while user == "":
                    user = input("Username : ")

            utils.log_info("Login with {}".format(user))
            utils.ssh_shell(addr[0], user, key_file=key_pair_temp.name)
            exit(0)

        """
            Remote by manifest file neo.yaml
        """
        set_file = self.args["--file"]
        default_file = orch.check_manifest_file()
        deploy_file = ".deploy/deploy.yml"

        if set_file:
            if os.path.exists(set_file):
                default_file = set_file
            else:
                utils.log_err("{} file is not exists!".format(set_file))
                exit()

        if not default_file:
            utils.log_err("Can't find neo.yml manifest file!")
            exit()

        if os.path.exists(deploy_file):
            deploy_init = utils.yaml_parser(deploy_file)
            deploy_init = [
                d_init
                for d_init in deploy_init
                if d_init["stack"] in ["instances", "clusters", "databases"]
            ]
        else:
            deploy_init = orch.initialize(default_file)
            deploy_init = [
                d_init
                for d_init in deploy_init
                if d_init["stack"] in ["instances", "clusters", "databases"]
            ]

        meta = None
        if len(deploy_init) == 1:
            meta = deploy_init[0]

        if len(deploy_init) > 1:
            meta_project = [pra_meta["project"] for pra_meta in deploy_init]
            meta_field = [
                {
                    "type": "TitleSelectOne",
                    "name": "Select Project",
                    "key": "project",
                    "values": meta_project,
                }
            ]
            meta_field = utils.prompt_generator("Select project...", meta_field)
            meta = [
                pra_meta
                for pra_meta in deploy_init
                if pra_meta in [meta_field["project"]]
            ][0]

        if meta:
            project_name = meta["project"]
            project_dir = meta["dir"]
            private_key_file = "{}/private_key.pem".format(project_dir)
            project_hostname = None
            project_user = None

            if not os.path.exists(private_key_file):
                utils.log_info("Generate {} private key...".format(project_name))
                wait_key = True
                while wait_key:
                    out = orch.get_pkey_from_stack(project_name)
                    if out:
                        with open(private_key_file, "w") as pkey:
                            pkey.write(out)
                            os.chmod(private_key_file, 0o600)
                            utils.log_info("Done...")
                        wait_key = False
                    else:
                        pkeys = orch.get_private_key(project_name)
                        if pkeys:
                            with open(private_key_file, "w") as pkey:
                                pkey.write(pkeys)
                                os.chmod(private_key_file, 0o600)
                                utils.log_info("Done...")
                            wait_key = False
                        else:
                            time.sleep(5)

            if os.path.exists(private_key_file):
                if not project_hostname:
                    project_hostname = orch.get_metadata(project_name, "controller")
                    project_user = orch.get_metadata(project_name, "user")

                do_ssh = True
                print("Try to connect...", end="")
                while do_ssh:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    result = sock.connect_ex((project_hostname, 22))
                    if result == 0:
                        print("\nSuccess...")
                        time.sleep(3)
                        do_ssh = False
                    else:
                        print(".", end="")
                        time.sleep(3)
                        do_ssh = True

                if self.args["--command"]:
                    try:
                        utils.ssh_out_stream(
                            project_hostname,
                            project_user,
                            self.args["--command"],
                            key_file=private_key_file,
                        )
                    except KeyboardInterrupt:
                        exit()
                elif self.args["--tunneling"]:
                    try:
                        tunnel_args = " ".join(
                            [
                                "-L {}".format(t_arg)
                                for t_arg in self.args["--tunneling"].split(",")
                            ]
                        )
                        commands = "ssh -i {} {} {}@{}".format(
                            private_key_file,
                            tunnel_args,
                            project_user,
                            project_hostname,
                        ).split(" ")
                        subprocess.call(commands)
                    except KeyboardInterrupt:
                        exit()
                else:
                    try:
                        utils.ssh_shell(
                            project_hostname, project_user, key_file=private_key_file
                        )
                    except KeyboardInterrupt:
                        exit()
