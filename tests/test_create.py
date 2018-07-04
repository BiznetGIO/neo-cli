"""Tests for our `neo create` subcommand."""

import pytest
from neo.libs import vm as vm_lib
from neo.libs import orchestration as orch


class TestCreate:
    def test_do_create(self):
        deploy_init = orch.initialize("neo.yml")
        orch.do_create(deploy_init)

        # check deployed vm
        vm_data = vm_lib.get_list()
        for vm in vm_data:
            if vm.name == 'unittest-vm':
                for network_name, network in vm.networks.items():
                    assert network_name == 'unittest-network'
