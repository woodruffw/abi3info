#!/usr/bin/env python

# codegen.py: codegen for abi3info

import shutil
from pathlib import Path

import toml

assert shutil.which("black"), "codegen needs `black` for auto-formatting!"

_HERE = Path(__file__).resolve().parent

_STABLE_ABI_FILE = _HERE / "stable_abi.toml"
assert _STABLE_ABI_FILE.is_file(), "missing stable ABI data"

_STABLE_ABI_DATA = toml.loads(_STABLE_ABI_FILE.read_text())
for key in ("struct", "function", "data"):
    assert key in _STABLE_ABI_DATA, "stable ABI data doesn't look right (format changed?)"
    val = _STABLE_ABI_DATA[key]
    assert isinstance(val, dict), "stable ABI data doesn't look right (format changed?)"

print(list(_STABLE_ABI_DATA.keys()))
