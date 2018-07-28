import pytest
from neo.libs import prompt


class TestPrompt:
    def test_prompt_get_stack(self, monkeypatch):
        def mockreturn():
            return 'foo'
        monkeypatch.setattr("neo.libs.prompt.get_stack", mockreturn)
        x = prompt.get_stack()
        assert x == 'foo'

    def test_prompt_get_project(self, monkeypatch):
        def mockreturn():
            return 'foo'
        monkeypatch.setattr("neo.libs.prompt.get_project", mockreturn)
        x = prompt.get_project()
        assert x == 'foo'

    def test_prompt_setup_form(self, monkeypatch):
        def mockreturn():
            return 'foo'
        monkeypatch.setattr("neo.libs.prompt.setup_form", mockreturn)
        x = prompt.setup_form()
        assert x == 'foo'

    def test_prompt_exec_form(self, monkeypatch):
        def mockreturn():
            return 'foo'
        monkeypatch.setattr("neo.libs.prompt.exec_form", mockreturn)
        x = prompt.exec_form()
        assert x == 'foo'

    def test_prompt_dump(self, monkeypatch):
        def mockreturn():
            return 'foo'
        monkeypatch.setattr("neo.libs.prompt.dump", mockreturn)
        x = prompt.dump()
        assert x == 'foo'

    def test_prompt_init(self, monkeypatch):
        def mockreturn():
            return 'foo'
        monkeypatch.setattr("neo.libs.prompt.init", mockreturn)
        x = prompt.init()
        assert x == 'foo'
