"""Tests for our `neo attach` subcommand."""

import pytest
import os, signal
from subprocess import PIPE, Popen as popen, TimeoutExpired

class TestAttach:
    @pytest.mark.run(order=3)
    def test_attach(self):
        # neo.yml located inside tests dir
        os.chdir("tests")

        proc = popen(['neo', 'attach'], stdout=PIPE)
        try:
            outs, errs = proc.communicate(timeout=10)
        except TimeoutExpired:
            # wait process. So it doesn't break terminal
            proc.send_signal(signal.SIGINT)
            proc.wait()
            outs, errs = proc.communicate()

        os.chdir(os.pardir)
        assert 'unittest@unittest-vm:~$' in str(outs)
