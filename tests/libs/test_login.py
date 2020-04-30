import pytest
import os

import neo.libs.login
from neo.libs import login


class TestLogin:
    def test_check_env(self, fs):
        home = os.path.expanduser("~")
        fs.create_file(f"{home}/.neo/config.toml")
        assert login.check_env()

    def fake_load_env_file(self):
        pass

    def fake_check_env(self):
        return True

    def test_get_env_values(self, monkeypatch):
        monkeypatch.setattr(neo.libs.login, "load_env_file", self.fake_load_env_file)
        monkeypatch.setattr(neo.libs.login, "check_env", self.fake_check_env)

        monkeypatch.setenv("OS_USERNAME", "jhon")
        monkeypatch.setenv("OS_PROJECT_ID", "g7ia30trlk")

        assert login.get_env_values() == {
            "username": "jhon",
            "password": None,
            "auth_url": None,
            "project_id": "g7ia30trlk",
            "user_domain_name": None,
        }

    def fake_get_env_values(self):
        env = {
            "username": "john",
            "password": "pass123",
            "auth_url": "https://foo.id:443/v1",
            "project_id": "g7ia30trlk",
            "user_domain_name": "foo.id",
        }
        return env

    def test_is_current_env(self, monkeypatch):
        monkeypatch.setattr(neo.libs.login, "get_env_values", self.fake_get_env_values)
        assert login.is_current_env("https://foo.id:443/v1", "foo.id", "john")

    def test_is_current_env_false(self, monkeypatch):
        monkeypatch.setattr(neo.libs.login, "get_env_values", self.fake_get_env_values)
        assert login.is_current_env("https://bar.id:443/v1", "bar.id", "merry") is False

    def fake_check_session(self):
        return True

    def test_do_logout(self, monkeypatch, fs):
        monkeypatch.setattr(neo.libs.login, "check_session", self.fake_check_session)

        home = os.path.expanduser("~")
        fs.create_file("/tmp/session.pkl")
        fs.create_file(home + "/.neo/config.toml")

        assert os.path.exists("/tmp/session.pkl")
        assert os.path.exists(home + "/.neo/config.toml")

        login.do_logout()

        assert os.path.exists("/tmp/session.pkl") is False
        assert os.path.exists(home + "/.neo/config.toml") is False

    def test_check_session(self, fs):
        fs.create_file("/tmp/session.pkl")
        assert login.check_session()
