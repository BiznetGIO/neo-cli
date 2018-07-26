"""Tests for our `neo attach` subcommand."""

import pytest
import os
import time
from neo.libs import vm as vm_lib
from neo.clis import Attach
from io import StringIO
from contextlib import redirect_stdout
from subprocess import PIPE, Popen


class TestAttach:
    @pytest.mark.run(order=3)
    def test_attach_command(self):
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

        f = StringIO()
        with redirect_stdout(f):
            a = Attach({'<args>': ['-c', 'ls -a'],
                        '<command>': 'attach'}, '-c', 'ls -a')
            a.execute()
            out = f.getvalue()

        os.chdir(os.pardir)
        assert 'Success' in out

    def test_attach_vm(self):
        vm_data = vm_lib.get_list()
        for vm in vm_data:
            if vm.name == 'unittest-vm':
                vm_id = vm.id

        cmd = ['neo', 'attach', 'vm', vm_id]
        with open("stdout.txt", "wb") as out, open("stderr.txt", "wb") as err:
            Popen(cmd, stdout=out, stderr=err)
        time.sleep(8)
        out = open('stderr.txt', 'r').read()
        os.remove('stdout.txt')
        os.remove('stderr.txt')
        assert 'successful!' in out
