"""Tests for our `neo hello` subcommand."""
import os
from subprocess import PIPE, Popen as popen
from unittest import TestCase
from unittest.mock import patch
from neo.libs import login


class TestLogin(TestCase):
    @patch("getpass.getpass")
    @patch("builtins.input")
    def test_do_login(self, input, getpass):
        input.return_value = os.environ.get('OS_USERNAME')
        getpass.return_value = os.environ.get('OS_PASSWORD')
        output = login.do_login()
        self.assertTrue(output)
