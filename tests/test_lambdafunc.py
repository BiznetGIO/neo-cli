import pytest
from neo.libs import lambdafunc


class TestLambdafunc:
    def test_get_flavor(self):
        assert 'SS2.1' in lambdafunc.get_flavor()

    def test_get_img(self):
        assert 'Ubuntu' in str(lambdafunc.get_img())
