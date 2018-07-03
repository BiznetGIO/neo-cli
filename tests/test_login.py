"""Tests for our `neo login` subcommand."""

import pytest
import os
from neo.libs import login


class TestLogin:
    def test_login(self, monkeypatch):
        login.load_env_file()
        username = os.environ.get('OS_USERNAME')
        passwd = os.environ.get('OS_PASSWORD')

        monkeypatch.setattr('builtins.input', lambda x: username)
        monkeypatch.setattr('getpass.getpass', lambda x: passwd)
        output = login.do_login()
        assert output == True
