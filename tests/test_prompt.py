import pytest
from neo.libs import prompt


class TestPrompt:
    # TODO need login
    def test_get_flavor(self):
        assert 'SS2.1' in prompt.get_flavor()

    def test_get_img(self):
        assert 'Ubuntu' in str(prompt.get_img())
