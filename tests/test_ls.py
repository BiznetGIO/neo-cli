"""Tests for `neo ls` subcommand."""

import pytest
import os
from io import StringIO
from contextlib import redirect_stdout
from neo.clis import Ls


class TestLs:
    def test_ls_vm(self):
        with pytest.raises(SystemExit):
            a = Ls({'<command>': 'ls'}, 'vm')
            a.execute()

    def test_ls_stack(self):
        with pytest.raises(SystemExit):
            a = Ls({'<command>': 'ls'}, 'stack')
            a.execute()

    def test_ls_net(self):
        with pytest.raises(SystemExit):
            a = Ls({'<command>': 'ls'}, 'network')
            a.execute()

    def test_ls_output(self):
        # no exit(). but failed when calle without
        # raises(SystemExit)
        with pytest.raises(SystemExit):
            a = Ls({'<args>': ['-o', 'unittest-vm'], '<command>': 'ls'},
                   '-o', 'unittest-vm')
            a.execute()

    def test_ls(self):
        os.chdir("tests")
        f = StringIO()
        with redirect_stdout(f):
            a = Ls({'<args>': [], '<command>': 'ls'}, None)
            foo = a.execute()
        out = f.getvalue()
        os.chdir(os.pardir)
        assert 'unittest-vm' in out

    def test_ls_vm_exception(self, monkeypatch):
        with pytest.raises(SystemExit):
            def mockreturn():
                return []
            monkeypatch.setattr("neo.libs.vm.get_list", mockreturn)
            a = Ls({'<command>': 'ls'}, 'vm')
            a.execute()

    def test_ls_network_exception(self, monkeypatch):
        with pytest.raises(SystemExit):
            def mockreturn():
                return []
            monkeypatch.setattr("neo.libs.network.get_list", mockreturn)
            a = Ls({'<command>': 'ls'}, 'network')
            a.execute()

    def test_ls_output_exception(self, monkeypatch):
        with pytest.raises(SystemExit):
            def mockreturn():
                return []
            monkeypatch.setattr("neo.libs.utils.get_project", mockreturn)
            a = Ls({'<args>': ['-o', 'unittest-vm'], '<command>': 'ls'},
                   '-o', 'unittest-vm')
            a.execute()
