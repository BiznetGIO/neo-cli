import pytest
import os
from testfixtures import LogCapture
from neo.libs import utils
from neo.libs import orchestration as orch


class TestUtils:
    def test_question(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda x: "y")
        assert utils.question("this is test") == True

    def test_get_index(self):
        assert utils.get_index({1:"a", 2:"b"}) == [1, 2]

    def test_get_project(self):
        os.chdir("tests")
        default_file = orch.check_manifest_file()
        os.chdir(os.pardir)
        assert utils.get_project(default_file) == ['unittest-network', 'unittest-vm', 'unittest-key']

    def test_read_file(self):
        assert utils.read_file("tests/neo.yml")[:7] == 'deploy:'

    def test_is_init(self):
        assert utils.isint(1) == True

    def test_is_init(self):
        assert utils.isfloat(1) == True

    def test_list_dir(self):
        cwd = os.getcwd()
        assert 'cli.py' in str(utils.list_dir(cwd))

    def test_log_warn(self):
        with LogCapture() as log:
            utils.log_warn("test warn")
        assert 'test warn' in str(log.records)

    def test_log_err(self):
        with LogCapture() as log:
            utils.log_err("test errors")
        assert 'test errors' in str(log.records)

    def test_form_generator(self, monkeypatch):
        monkeypatch.setattr("neo.libs.utils.form_generator",
                            lambda x, y: ('foo', 'bar'))
        out = utils.form_generator('fofo', 'baz')
        assert out == ('foo', 'bar')

    def test_prompt_generator(self, monkeypatch):
        monkeypatch.setattr("neo.libs.utils.prompt_generator",
                            lambda x, y: ('', 'bar'))
        x = utils.prompt_generator('fofo', 'baz')
        assert x == ('', 'bar')

    def test_isfloat_eror(self):
        assert utils.isfloat('f') == False

    def test_isint_eror(self):
        assert utils.isint('f') == False
