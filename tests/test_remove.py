"""Tests for our `neo create` subcommand."""

import pytest
from neo.libs import vm as vm_lib

class TestRemove:
    @pytest.mark.run(order=2)
    def test_do_delete(self):
        # get 'unittest-vm' id
        vm_data = vm_lib.get_list()
        for vm in vm_data:
            if vm.name == 'unittest-vm':
                instance_id = vm.id
                vm_lib.do_delete(instance_id)

        # get fresh list
        vm_data_new = vm_lib.get_list()
        for vm_new in vm_data_new:
            assert 'unittest-vm' not in vm_new.name
