# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
Tests the mod selection system
"""

import sys
import io
import pytest
from io import StringIO
from contextlib import redirect_stdout
from portmod.repo.atom import Atom, atom_sat
from portmod.query import query, query_main, query_depends, display_search_results
from .env import setup_env, tear_down_env


@pytest.fixture(scope="module", autouse=True)
def setup_repo():
    """
    Sets up test repo for querying
    """
    yield setup_env("test")
    tear_down_env()


def test_query():
    """
    Tests that we can query for exact matches in pybuild fields
    """
    results = query("LICENSE", "eula")
    assert any(atom_sat(mod.ATOM, Atom("test/test-eula-1.0")) for mod in results)


def test_insensitive_squelch():
    """
    Tests that we can query for case insensitive matches where there are separators
    in between keywords
    """
    results = query("DESC", "desc foo", insensitive=True, squelch_sep=True, strip=True)
    assert any(atom_sat(mod.ATOM, Atom("test/test-1.0")) for mod in results)


def test_depends():
    """
    Tests that we can query for mods that depend on a particular atom
    """
    results = query_depends(Atom("test/test"), all_mods=True)
    assert any(atom_sat(atom, Atom("test/test2-1.0")) for atom, _ in results)


def test_display_results():
    """
    Tests that display_search_results doesn't cause any exceptions
    and that all mods are included in the result
    """
    results = query("LICENSE", "")
    strfile = io.StringIO()
    display_search_results(results, file=strfile)
    string = strfile.getvalue()
    for mod in results:
        assert mod.ATOM.CMN in string


def test_main_depends():
    """Tests that the cli depends query interface functions sanely"""
    output = StringIO()
    with redirect_stdout(output):
        sys.argv = ["", "-a", "depends", "test/test5"]
        query_main()
        assert "test/test7" in output.getvalue()


def test_main_has():
    """Tests that the cli has query interface functions sanely"""
    output = StringIO()
    with redirect_stdout(output):
        sys.argv = ["", "-a", "has", "DATA_OVERRIDES"]
        query_main()
        assert "test/test6" in output.getvalue()


def test_main_hasuse():
    """Tests that the cli hasuse query interface functions sanely"""
    output = StringIO()
    with redirect_stdout(output):
        sys.argv = ["", "-a", "hasuse", "baf"]
        query_main()
        assert "test/test4" in output.getvalue()


def test_main_uses():
    """Tests that the cli uses query interface functions sanely"""
    output = StringIO()
    with redirect_stdout(output):
        sys.argv = ["", "uses", "test/test7"]
        query_main()
        string = output.getvalue()
        assert "foo" in string
        assert "test flag" in string


def test_main_meta():
    """Tests that the cli has query interface functions sanely"""
    output = StringIO()
    with redirect_stdout(output):
        sys.argv = ["", "meta", "test/test"]
        query_main()
        assert "someone <someone@example.org>" in output.getvalue()
