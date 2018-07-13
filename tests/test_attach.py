"""Tests for our `neo attach` subcommand."""

import pytest
import os
import time
from subprocess import PIPE, Popen as popen
from neo.libs import vm as vm_lib


class TestAttach:
    @pytest.mark.run(order=3)
    def test_attach(self):
        # neo.yml located inside tests dir
        os.chdir("tests")

        # wait until vm fully resized
        vm_status = ''
        while vm_status != 'ACTIVE':
            # get 'unittest-vm' id
            vm_data = vm_lib.get_list()
            for vm in vm_data:
                if vm.name == 'unittest-vm':
                    vm_status = vm.status
            time.sleep(4)
            print('vm still updating ...')

        outs = popen(['neo', 'attach', '-c "ls -a"'], stdout=PIPE).communicate()
        os.chdir(os.pardir)
        assert 'Success' in str(outs)
