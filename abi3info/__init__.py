"""
The abi3info APIs.
"""

from __future__ import annotations

from typing import Final

from abi3info._internal import (
    _DATAS,
    _FEATURE_MACROS,
    _FUNCTIONS,
    _MACROS,
    _STRUCTS,
    _TYPEDEFS,
)
from abi3info.models import (
    Data,
    FeatureMacro,
    Function,
    Macro,
    Struct,
    Symbol,
    Typedef,
)

__version__ = "2025.11.18"
"""
The current version of abi3info.
"""

DATAS: Final[dict[Symbol, Data]] = _DATAS
"""
Data object members of the limited API and stable ABI.
"""

FEATURE_MACROS: Final[dict[str, FeatureMacro]] = _FEATURE_MACROS
"""
Feature macros that control the availability of limited API members.
"""

FUNCTIONS: Final[dict[Symbol, Function]] = _FUNCTIONS
"""
Function members of the limited API and stable ABI.
"""

MACROS: Final[dict[str, Macro]] = _MACROS
"""
Macro members of the limited API.
"""

STRUCTS: Final[dict[str, Struct]] = _STRUCTS
"""
Struct members of the limited API.
"""

TYPEDEFS: Final[dict[str, Typedef]] = _TYPEDEFS
"""
Typedef members of the limited API.
"""
