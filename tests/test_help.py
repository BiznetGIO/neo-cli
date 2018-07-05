"""Tests for our main skele CLI module."""

import pytest
from subprocess import PIPE, Popen as popen
from neo import __version__ as VERSION


class TestHelp(object):
    def test_returns_usage_information(self):
        # take output from 'neo -h'. Then take the first word
        output = popen(['neo', '-h'], stdout=PIPE).communicate()[0]
        assert 'Usage:' in str(output)

        output = popen(['neo', '--help'], stdout=PIPE).communicate()[0]
        assert 'Usage:' in str(output)


class TestVersion(object):
    def test_returns_version_information(self):
        output = popen(['neo', '--version'], stdout=PIPE).communicate()[0]
        assert "{}\n".format(VERSION).encode() == output
