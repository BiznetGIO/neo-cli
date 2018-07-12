"""Tests for `neo update` subcommand."""

import pytest
import os
import time
from neo.libs import vm as vm_lib
from neo.libs import orchestration as orch


class TestUpdate:
    @pytest.mark.run(order=2)
    def test_do_update(self):
        cwd = os.getcwd()

        # wait until last vm successfully created
        vm_status = ''
        while vm_status != 'ACTIVE':
            # get 'unittest-vm' id
            vm_data = vm_lib.get_list()
            for vm in vm_data:
                if vm.name == 'unittest-vm':
                    vm_status = vm.status
                    vm_name = vm.name
            time.sleep(2)
            print('waiting until vm activated ...')

        deploy_init = orch.initialize(cwd + "/tests/neo2.yml")
        orch.do_update(deploy_init)
        print(vm_name + ' updated')

        # check updated vm
        # wait until successfully updated
        updated_status = None
        while updated_status == None:
            vm_data = orch.get_list()
            for vm in vm_data:
                if "unittest-vm" in vm:
                    updated_status = vm[4]
            time.sleep(2)
            print('waiting until vm fully updated ...')

        assert updated_status != None
