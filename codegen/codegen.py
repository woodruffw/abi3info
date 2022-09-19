#!/usr/bin/env python

# codegen.py: codegen for abi3info

import shutil
import subprocess
from pathlib import Path

import toml

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

# Sanity checks.
assert shutil.which("black"), "codegen needs `black` for auto-formatting!"

_HERE = Path(__file__).resolve().parent

_ABI3INFO = _HERE.parent / "abi3info"
assert _ABI3INFO.is_dir(), "missing abi3info module"

_INTERNAL = _ABI3INFO / "_internal.py"
_OUT = _INTERNAL.open(mode="w")

_STABLE_ABI_FILE = _HERE / "stable_abi.toml"
assert _STABLE_ABI_FILE.is_file(), "missing stable ABI data"

_STABLE_ABI_DATA = toml.loads(_STABLE_ABI_FILE.read_text())
for key in ("struct", "function", "data"):
    assert key in _STABLE_ABI_DATA, "stable ABI data doesn't look right (format changed?)"
    val = _STABLE_ABI_DATA[key]
    assert isinstance(val, dict), "stable ABI data doesn't look right (format changed?)"

# All generated code goes into `abi3info/_internal.py`.
#
# The way we actually do the codegen is a little cheeky: rather than
# building up things like instantiations manually, we reuse each model's `repr()`.

print("from typing import Dict, Final", file=_OUT)
print(file=_OUT)
print(
    "from abi3info.models import Data, FeatureMacro, FullStruct, Function, "
    "Macro, OpaqueStruct, PartialStruct, PyVersion, Struct, Symbol, Typedef",
    file=_OUT,
)

print("# this file was generated; do not modify it by hand!", file=_OUT)

feature_macros = {
    name: FeatureMacro(name, body["doc"], body.get("windows", False))
    for name, body in _STABLE_ABI_DATA["feature_macro"].items()
}
print(f"FEATURE_MACROS: Final[Dict[str, FeatureMacro]] = {feature_macros}", file=_OUT)

structs = {}
for name, body in _STABLE_ABI_DATA["struct"].items():
    match body["struct_abi_kind"]:
        case "opaque":
            struct = OpaqueStruct(name, PyVersion.parse(body["added"]))
        case "full-abi":
            struct = FullStruct(name, PyVersion.parse(body["added"]))
        case "members":
            struct = PartialStruct(name, PyVersion.parse(body["added"]), body["members"])
        case other:
            assert False, f"unexpected struct_abi_kind={other}"

    structs[struct.name] = struct
print(f"STRUCTS: Final[Dict[str, Struct]] = {structs}", file=_OUT)

functions = {
    Symbol(name): Function(
        Symbol(name),
        PyVersion.parse(body["added"]),
        feature_macros.get(body.get("ifdef")),
        body.get("abi_only", False),
    )
    for name, body in _STABLE_ABI_DATA["function"].items()
}
print(f"FUNCTIONS: Final[Dict[Symbol, Function]] = {functions}", file=_OUT)

macros = {}
for name, body in {**_STABLE_ABI_DATA["const"], **_STABLE_ABI_DATA["macro"]}.items():
    macros[name] = Macro(name, PyVersion.parse(body["added"]))
print(f"MACROS: Final[Dict[str, Macro]] = {macros}", file=_OUT)

datas = {
    Symbol(name): Data(
        Symbol(name),
        PyVersion.parse(body["added"]),
        feature_macros.get(body.get("ifdef")),
        body.get("abi_only", False),
    )
    for name, body in _STABLE_ABI_DATA["data"].items()
}
print(f"DATAS: Final[Dict[Symbol, Data]] = {datas}", file=_OUT)

typedefs = {
    name: Typedef(name, PyVersion.parse(body["added"]))
    for name, body in _STABLE_ABI_DATA["typedef"].items()
}
print(f"TYPEDEFS: Final[Dict[str, Typedef]] = {typedefs}", file=_OUT)

_OUT.close()

subprocess.run(["black", _INTERNAL])
