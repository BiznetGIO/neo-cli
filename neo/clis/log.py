from neo.clis.base import Base
from neo.libs import vm as vm_lib
from neo.libs import orchestration as orch
from neo.libs import utils


class Log(Base):
    """
    usage:
        log vm [-l LIMIT]
        log vm
        log vm <VM_ID> [-l LIMIT]
        log vm <VM_ID>

    Options:
    -h --help                    Print usage
    -l limit --limit=LIMIT       Print outputs from  line  page [default: 30]
    """

    def execute(self):
        if self.args["vm"]:
            instance_id = self.args["<VM_ID>"]
            limit = self.args["--limit"]
            if not instance_id:
                default_file = orch.check_manifest_file()
                if default_file:
                    keys = utils.get_key(default_file)
                    instances = keys["stack"]["instances"]
                    if len(instances) > 0:
                        vms = vm_lib.get_list()
                        for vm in vms:
                            if vm.name == instances[0]:
                                instance_id = vm.id
                                break
                    else:
                        utils.log_err("VM not found")
                else:
                    utils.log_err("Can't find neo.yml manifest file!")
            else:
                vm_data = vm_lib.get_list()
                for vm in vm_data:
                    if (instance_id == vm.name) or (instance_id == vm.id):
                        instance_id = vm.id
            try:
                utils.log_info(vm_lib.get_console_logs(instance_id, length=limit))
            except Exception as err:
                utils.log_err(err.message)
        exit()
