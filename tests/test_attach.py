"""Tests for our `neo attach` subcommand."""

import pytest
import os, signal
from subprocess import PIPE, Popen as popen, TimeoutExpired
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
                    vm_id = vm.id
            print('vm still updating ...')

        proc = popen(['neo', 'attach', 'vm', vm_id ], stdout=PIPE)
        try:
            outs, errs = proc.communicate(timeout=10)
        except TimeoutExpired:
            # wait process. So it doesn't break terminal
            proc.send_signal(signal.SIGINT)
            proc.wait()
            outs, errs = proc.communicate()

        os.chdir(os.pardir)
        assert 'unittest@unittest-vm:~$' in str(outs)
