"""Tests for our `neo create` subcommand."""

import pytest
import os
from neo.libs import vm as vm_lib
from neo.libs import orchestration as orch


class TestCreate:
    @pytest.mark.run(order=1)
    def test_do_create(self):
        cwd = os.getcwd()
        deploy_init = orch.initialize(cwd + "/tests/neo.yml")
        orch.do_create(deploy_init)

        # check deployed vm
        vm_data = vm_lib.get_list()
        for vm in vm_data:
            if vm.name == 'unittest-vm':
                for network_name, network in vm.networks.items():
                    assert network_name == 'unittest-network'
