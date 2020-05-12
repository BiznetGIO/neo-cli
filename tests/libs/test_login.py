import pytest
import os
import toml
from tempfile import gettempdir

import neo.libs.login
from neo.libs import login


class TestLogin:
    def test_check_env(self, fs):
        home = os.path.expanduser("~")
        fs.create_file(os.path.join(home, ".neo", "config.toml"))
        assert login.check_env()

    def fake_load_env_file(self):
        pass

    def fake_check_env(self):
        return True

    def dummy_config_toml(self):
        config = ""
        config += "[auth]\n"
        config += "os_username = 'john'\n"
        config += "os_password = 'pass123'\n"
        config += "\n"
        config += "[region.wjv]\n"
        config += "os_auth_url = 'https://foo.id:443/v1'\n"
        config += "os_project_id = 'g7ia30trlk'\n"
        config += "os_user_domain_name = 'foo.id'\n"
        config += "status = 'ACTIVE'\n"
        config += "[region.jkt]\n"
        config += "os_auth_url = 'https://bar.id:443/v1'\n"
        config += "os_project_id = 'iqn1a69tolj'\n"
        config += "os_user_domain_name = 'bar.id'\n"
        config += "status = 'IDLE'\n"
        config += "\n"
        return toml.loads(config)

    def test_get_env_values(self, monkeypatch):
        monkeypatch.setattr(neo.libs.login, "load_env_file", self.dummy_config_toml)
        monkeypatch.setattr(neo.libs.login, "check_env", self.fake_check_env)

        assert login.get_env_values()

    def fake_get_env_values(self):
        env = [
            {
                "username": "john",
                "password": "pass123",
                "region": "zone-1",
                "auth_url": "https://foo.id:443/v1",
                "project_id": "g7ia30trlk",
                "user_domain_name": "foo.id",
                "status": "ACTIVE",
            },
            {
                "username": "john",
                "password": "pass123",
                "region": "zone-2",
                "auth_url": "https://bar.id:443/v1",
                "project_id": "iqn1a69tolj",
                "user_domain_name": "bar.id",
                "status": "IDLE",
            },
        ]

        return env

    def test_is_current_env(self, monkeypatch):
        monkeypatch.setattr(neo.libs.login, "get_env_values", self.fake_get_env_values)
        assert login.is_current_env("https://foo.id:443/v1", "foo.id", "john")

    def test_is_current_env_false(self, monkeypatch):
        monkeypatch.setattr(neo.libs.login, "get_env_values", self.fake_get_env_values)
        assert login.is_current_env("https://bar.id:443/v1", "bar.id", "merry") is None

    def fake_check_session(self):
        return True

    def test_do_logout(self, monkeypatch, fs):
        monkeypatch.setattr(neo.libs.login, "check_session", self.fake_check_session)

        home = os.path.expanduser("~")
        tmp_dir = os.path.join(gettempdir(), ".neo")

        fs.create_file(tmp_dir + "/session.pkl")
        fs.create_file(os.path.join(home, ".neo", "config.toml"))

        assert os.path.exists(tmp_dir + "/session.pkl")
        assert os.path.exists(os.path.join(home, ".neo", "config.toml"))

        login.do_logout()

        assert os.path.exists(tmp_dir + "/session.pkl") is False
        assert os.path.exists(os.path.join(home, ".neo", "config.toml")) is False

    def test_check_session(self, fs):
        tmp_dir = os.path.join(gettempdir(), ".neo")
        fs.create_file(tmp_dir + "/session.pkl")
        assert login.check_session()
