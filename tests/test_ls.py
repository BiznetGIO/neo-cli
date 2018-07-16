"""Tests for `neo ls` subcommand."""

import pytest
from subprocess import PIPE, Popen as popen
from neo.clis import Ls


class TestLs:
    @pytest.mark.run(order=4)
    def test_ls(self):
        # proc = popen(a.execute(), stdout=PIPE)
        # outs = proc.communicate()[0]
        with pytest.raises(SystemExit):
            a = Ls({'<command>': 'ls'}, 'vm')
            popen(a.execute(), stdout=PIPE)
