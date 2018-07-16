"""Tests for `neo ls` subcommand."""

import pytest
from subprocess import PIPE, Popen as popen
from neo.clis import Ls


class TestLs:
    @pytest.mark.run(order=4)
    def test_ls_vm(self):
        with pytest.raises(SystemExit):
            a = Ls({'<command>': 'ls'}, 'vm')
            popen(a.execute(), stdout=PIPE)

    def test_ls_stack(self):
        with pytest.raises(SystemExit):
            a = Ls({'<command>': 'ls'}, 'stack')
            popen(a.execute(), stdout=PIPE)

    def test_ls_net(self):
        with pytest.raises(SystemExit):
            a = Ls({'<command>': 'ls'}, 'network')
            popen(a.execute(), stdout=PIPE)

    def test_ls_output(self):
        # no exit(). but failed when calle without
        # raises(SystemExit)
        with pytest.raises(SystemExit):
            a = Ls({'<args>': ['-o', 'referensi-vm'], '<command>': 'ls'},
                   '-o', 'referensi-vm')
            popen(a.execute(), stdout=PIPE)
