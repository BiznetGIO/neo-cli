"""Tests for our `neo create` subcommand."""

import pytest
import time
from neo.libs import vm as vm_lib
from neo.libs import orchestration as orch


class TestRemove:
    @pytest.mark.run(order=-2)
    def test_do_delete_vm(self):
        # wait until successfully created
        vm_status = ''
        while vm_status != 'ACTIVE':
            # get 'unittest-vm' id
            vm_data = vm_lib.get_list()
            for vm in vm_data:
                if vm.name == 'unittest-vm':
                    vm_status = vm.status
                    instance_id = vm.id
                    vm_name = vm.name
            time.sleep(2)
            print('waiting until vm activated ...')

        vm_lib.do_delete(instance_id)
        orch.do_delete(vm_name)
        orch.do_delete('unittest-network')
        orch.do_delete('unittest-key')
        print(vm_name + ' with id ' + instance_id + ' deleted')

        # wait until successfully deleted
        while 'unittest' in vm_data:
            vm_data = vm_lib.get_list()
            time.sleep(2)
            print('waiting until vm fully deleted ...')

        assert 'unittest-vm' not in vm_data
