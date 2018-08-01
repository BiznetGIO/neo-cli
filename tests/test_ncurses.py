import pytest
from neo.libs import ncurses


class TestCurses:
    def test_curses_get_stack(self, monkeypatch):
        def mockreturn():
            return 'foo'
        monkeypatch.setattr("neo.libs.ncurses.get_stack", mockreturn)
        x = ncurses.get_stack()
        assert x == 'foo'

    def test_curses_get_project(self, monkeypatch):
        def mockreturn():
            return 'foo'
        monkeypatch.setattr("neo.libs.ncurses.get_project", mockreturn)
        x = ncurses.get_project()
        assert x == 'foo'

    def test_curses_setup_form(self, monkeypatch):
        def mockreturn():
            return 'foo'
        monkeypatch.setattr("neo.libs.ncurses.setup_form", mockreturn)
        x = ncurses.setup_form()
        assert x == 'foo'

    def test_curses_exec_form(self, monkeypatch):
        def mockreturn():
            return 'foo'
        monkeypatch.setattr("neo.libs.ncurses.exec_form", mockreturn)
        x = ncurses.exec_form()
        assert x == 'foo'

    def test_curses_dump(self, monkeypatch):
        def mockreturn():
            return 'foo'
        monkeypatch.setattr("neo.libs.ncurses.dump", mockreturn)
        x = ncurses.dump()
        assert x == 'foo'

    def test_curses_init(self, monkeypatch):
        def mockreturn():
            return 'foo'
        monkeypatch.setattr("neo.libs.ncurses.init", mockreturn)
        x = ncurses.init()
        assert x == 'foo'
