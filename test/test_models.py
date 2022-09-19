import pytest

from abi3info.models import PyVersion, Symbol


class TestSymbol:
    def test_symbol_properties(self):
        sym = Symbol("foo")

        assert sym.name == "foo"
        assert sym.macos == "_foo"
        assert sym.linux == "foo"

    def test_symbol_equality(self):
        foo1, foo2 = Symbol("foo"), Symbol("foo")
        assert foo1 == foo2

        bar = Symbol("bar")
        assert foo1 != bar

        with pytest.raises(TypeError):
            assert foo1 == "foo"


class TestPyVersion:
    def test_comparison(self):
        older_minor, newer_minor = PyVersion(3, 2), PyVersion(3, 3)

        # Total comparison.
        assert older_minor != newer_minor
        assert older_minor < newer_minor
        assert older_minor <= newer_minor
        assert newer_minor != older_minor
        assert newer_minor > older_minor
        assert newer_minor >= older_minor

        # Self comparison.
        assert older_minor == older_minor
        assert older_minor >= older_minor
        assert older_minor <= older_minor

        older_major, newer_major = PyVersion(3, 10), PyVersion(4, 0)

        # Total comparison.
        assert older_major != newer_major
        assert older_major < newer_major
        assert older_major <= newer_major
        assert newer_major != older_major
        assert newer_major > older_major
        assert newer_major >= older_major

        # Self comparison.
        assert older_major == older_major
        assert older_major >= older_major
        assert older_major <= older_major
