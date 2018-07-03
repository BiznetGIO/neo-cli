"""Tests for our `neo login` subcommand."""

import pytest
import os
from neo.libs import login


class TestLogin:
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

    def test_do_logout(self):
        login.do_logout()
        output = login.check_session()
        assert output == False
