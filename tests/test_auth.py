"""Tests for our `neo login` subcommand."""

import pytest
import os
from neo.libs import login
from neo.libs import utils

class TestAuth:
    @pytest.mark.run(order=0)
    def test_do_login(self, monkeypatch):
        login.load_env_file()
        username = os.environ.get('OS_USERNAME')
        passwd = os.environ.get('OS_PASSWORD')
        # give value to input() prompt
        monkeypatch.setattr('builtins.input', lambda x: username)
        monkeypatch.setattr('getpass.getpass', lambda x: passwd)
        # return True is login succeed
        output = login.do_login()
        assert output == True

    @pytest.mark.run(order=-1)
    def test_do_logout(self):
        login.do_logout()
        # session removed if logout succeed
        output = login.check_session()
        assert output == False

    def test_env_file(self):
        assert login.check_env() == True

    def test_create_env_file(self):
        home = os.path.expanduser("~")
        env_file = "{}/.neo.env".format(home)
        env_file_tmp = "{}/.neo.tmp".format(home)

        # move already existing file
        os.rename(env_file, env_file_tmp)
        login.create_env_file("usertest", "passwd", "1")
        login.add_token("1abc")
        outs = utils.read_file(env_file)
        os.remove(env_file)
        os.rename(env_file_tmp, env_file)
        assert 'usertest' in outs
