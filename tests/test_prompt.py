import pytest
import os
from testfixtures import LogCapture
from neo.libs import utils
from neo.libs import orchestration as orch
from neo.libs import login
from neo.libs import prompt

class TestPrompt:
    # TODO need login
    def test_get_flavor(self):
        assert 'SS2.1' in prompt.get_flavor()

    def test_get_img(self):
        assert 'Ubuntu' in str(prompt.get_img())
