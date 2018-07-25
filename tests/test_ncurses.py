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
