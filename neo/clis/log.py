from neo.clis.base import Base
from neo.libs import vm as vm_lib
from neo.libs import orchestration as orch
from neo.libs import utils

class Log(Base):
    """
    usage: 
        log vm
        log vm <VM_ID>

    Show Logs
    """


    def execute(self):
        if self.args["vm"]:
            instance_id = self.args["<VM_ID>"]
            if not instance_id:
                default_file = orch.check_manifest_file()
                if default_file:
                    keys = utils.get_key(default_file)
                    instances = keys['stack']['instances']
                    if len(instances)>0:
                        vms = vm_lib.get_list()
                        for vm in vms:
                            if vm.name == instances[0]:
                                instance_id = vm.id
                                break
                    else:
                       utils.log_err('VM not found')
                else:
                    utils.log_err("Can't find neo.yml manifest file!")
            try:
                utils.log_info(vm_lib.get_console_logs(instance_id))
            except Exception as err:
                utils.log_err(err.message)
        exit()
