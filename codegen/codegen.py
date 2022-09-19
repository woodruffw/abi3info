#!/usr/bin/env python

# codegen.py: codegen for abi3info

import os
import shutil
import subprocess
import sys
from hashlib import sha256
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

_STABLE_ABI_FILE = _HERE / "stable_abi.toml"
assert _STABLE_ABI_FILE.is_file(), "missing stable ABI data"

stable_abi_data = _STABLE_ABI_FILE.read_text()
new_checksum = sha256(stable_abi_data.encode()).hexdigest()

_STABLE_ABI_CHECKSUM_FILE = _STABLE_ABI_FILE.with_suffix(".sha256")
old_checksum = None
if _STABLE_ABI_CHECKSUM_FILE.is_file():
    old_checksum = _STABLE_ABI_CHECKSUM_FILE.read_text().rstrip()

if old_checksum == new_checksum and not os.getenv("FORCE_CODEGEN", False):
    print("codegen: exiting early because input has not changed")
    sys.exit(0)

_STABLE_ABI_CHECKSUM_FILE.write_text(new_checksum)

# TODO: Check here to see if _STABLE_ABI_FILE has changed or if we're forcing a run anyways.

_STABLE_ABI_DATA = toml.loads(stable_abi_data)
for key in ("struct", "function", "data"):
    assert key in _STABLE_ABI_DATA, "stable ABI data doesn't look right (format changed?)"
    val = _STABLE_ABI_DATA[key]
    assert isinstance(val, dict), "stable ABI data doesn't look right (format changed?)"

_INTERNAL = _ABI3INFO / "_internal.py"
_OUT = _INTERNAL.open(mode="w")

# All generated code goes into `abi3info/_internal.py`.
#
# The way we actually do the codegen is a little cheeky: rather than
# building up things like instantiations manually, we reuse each model's `repr()`.

print(
    """
'''
Generated definitions and data structures for abi3info.

This module should not be used directly; it is not a public API.
'''
""",
    file=_OUT,
)

print("from typing import Final", file=_OUT)
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
print(f"_FEATURE_MACROS: Final[dict[str, FeatureMacro]] = {feature_macros}", file=_OUT)

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
print(f"_STRUCTS: Final[dict[str, Struct]] = {structs}", file=_OUT)

functions = {
    Symbol(name): Function(
        Symbol(name),
        PyVersion.parse(body["added"]),
        feature_macros.get(body.get("ifdef")),
        body.get("abi_only", False),
    )
    for name, body in _STABLE_ABI_DATA["function"].items()
}
print(f"_FUNCTIONS: Final[dict[Symbol, Function]] = {functions}", file=_OUT)

macros = {}
for name, body in {**_STABLE_ABI_DATA["const"], **_STABLE_ABI_DATA["macro"]}.items():
    macros[name] = Macro(name, PyVersion.parse(body["added"]))
print(f"_MACROS: Final[dict[str, Macro]] = {macros}", file=_OUT)

datas = {
    Symbol(name): Data(
        Symbol(name),
        PyVersion.parse(body["added"]),
        feature_macros.get(body.get("ifdef")),
        body.get("abi_only", False),
    )
    for name, body in _STABLE_ABI_DATA["data"].items()
}
print(f"_DATAS: Final[dict[Symbol, Data]] = {datas}", file=_OUT)

typedefs = {
    name: Typedef(name, PyVersion.parse(body["added"]))
    for name, body in _STABLE_ABI_DATA["typedef"].items()
}
print(f"_TYPEDEFS: Final[dict[str, Typedef]] = {typedefs}", file=_OUT)

_OUT.close()

subprocess.run(["black", _INTERNAL])
