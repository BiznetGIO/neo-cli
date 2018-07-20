"""Tests for `neo ls` subcommand."""

import pytest
import os
from io import StringIO
from contextlib import redirect_stdout
from neo.clis import Ls


class TestLs:
    @pytest.mark.run(order=4)
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
            a = Ls({'<args>': ['-o', 'referensi-vm'], '<command>': 'ls'},
                   '-o', 'referensi-vm')
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
