import itertools

import pytest

from abi3info.models import (
    Data,
    FeatureMacro,
    FullStruct,
    Function,
    Macro,
    OpaqueStruct,
    PartialStruct,
    PyVersion,
    Symbol,
    Typedef,
)


class TestSymbol:
    def test_homoiconic(self):
        assert eval(repr(Symbol("foo"))) == Symbol("foo")

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

    def test_symbol_hashing_visibility_invariance(self):
        sym1 = Symbol("foo")
        sym2 = Symbol("foo", visibility="hidden")
        assert hash(sym1) == hash(sym2)


class TestPyVersion:
    def test_homoiconic(self):
        assert eval(repr(PyVersion(3, 10))) == PyVersion(3, 10)

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

    def test_decode_version(self):
        assert PyVersion.decode_version(0x030401A2) == PyVersion(3, 4)
        assert PyVersion.decode_version(0x0304FFFF) == PyVersion(3, 4)
        assert PyVersion.decode_version(0x0207FFFF) == PyVersion(2, 7)
        assert PyVersion.decode_version(0x030AFFFF) == PyVersion(3, 10)

        v3_12_0_a0 = (3 << 24) | (12 << 16)
        assert v3_12_0_a0 == 0x030C0000
        assert PyVersion.decode_version(v3_12_0_a0) == PyVersion(3, 12)

    def test_parse_dotted(self):
        assert PyVersion.parse_dotted("3.2") == PyVersion(3, 2)
        assert PyVersion.parse_dotted("4.0") == PyVersion(4, 0)

        with pytest.raises(ValueError):
            PyVersion.parse_dotted("3")

        with pytest.raises(ValueError):
            PyVersion.parse_dotted("3.2.1")

        with pytest.raises(ValueError):
            PyVersion.parse_dotted("3.")

    def test_parse_python_tag(self):
        assert PyVersion.parse_python_tag("cp32") == PyVersion(3, 2)
        assert PyVersion.parse_python_tag("cp310") == PyVersion(3, 10)
        assert PyVersion.parse_python_tag("cp40") == PyVersion(4, 0)

        with pytest.raises(ValueError):
            PyVersion.parse_python_tag("py27")

        with pytest.raises(ValueError):
            PyVersion.parse_python_tag("cp3")

        with pytest.raises(ValueError):
            PyVersion.parse_python_tag("cp10_11")

    def test_version_to_str(self):
        assert str(PyVersion(3, 2)) == "3.2"
        assert f"{PyVersion(3, 2)}" == "3.2"


class TestMacro:
    def test_homoiconic(self):
        assert eval(repr(Macro("foo", PyVersion(3, 10)))) == Macro("foo", PyVersion(3, 10))


class TestOpaqueStruct:
    def test_homoiconic(self):
        assert eval(repr(OpaqueStruct("foo", PyVersion(3, 10)))) == OpaqueStruct(
            "foo", PyVersion(3, 10)
        )


class TestPartialStruct:
    def test_homoiconic(self):
        for members in (None, ["bar"]):
            assert eval(repr(PartialStruct("foo", PyVersion(3, 10), members))) == PartialStruct(
                "foo", PyVersion(3, 10), members
            )


class TestFullStruct:
    def test_homoiconic(self):
        assert eval(repr(FullStruct("foo", PyVersion(3, 10)))) == FullStruct(
            "foo", PyVersion(3, 10)
        )


class TestFeatureMacro:
    def test_homoiconic(self):
        for windows in (True, False, "maybe"):
            assert eval(repr(FeatureMacro("foo", "some doc", windows))) == FeatureMacro(
                "foo", "some doc", windows
            )


class TestFunction:
    def test_homoiconic(self):
        for ifdef, abi_only in itertools.product(
            (None, FeatureMacro("foo", "some doc", True)), (True, False)
        ):
            assert eval(
                repr(Function(Symbol("foo"), PyVersion(3, 10), ifdef, abi_only))
            ) == Function(Symbol("foo"), PyVersion(3, 10), ifdef, abi_only)


class TestData:
    def test_homoiconic(self):
        for ifdef, abi_only in itertools.product(
            (None, FeatureMacro("foo", "some doc", True)), (True, False)
        ):
            assert eval(repr(Data(Symbol("foo"), PyVersion(3, 10), ifdef, abi_only))) == Data(
                Symbol("foo"), PyVersion(3, 10), ifdef, abi_only
            )


class TestTypedef:
    def test_homoiconic(self):
        assert eval(repr(Typedef("foo", PyVersion(3, 10)))) == Typedef("foo", PyVersion(3, 10))
