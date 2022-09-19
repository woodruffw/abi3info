from __future__ import annotations

from dataclasses import dataclass
from typing import List, Literal, Optional


@dataclass(frozen=True, slots=True, eq=False, unsafe_hash=True)
class Symbol:
    """
    Represents a linker symbol, which may or may not point to some kind of object
    (function, struct, constant, etc.).

    The contained symbol is not "normalized" for any particular host;
    users of this class must choose the correct property (e.g. `Symbol.macos`)
    for their use case.
    """

    name: str

    @property
    def macos(self) -> str:
        """
        Returns a macOS-style symbol for the underlying symbol.
        """
        return f"_{self.name}"

    @property
    def linux(self) -> str:
        """
        Returns a Linux-style symbol for the underlying symbol.
        """
        return self.name

    # NOTE: Manually defined to make the typing stronger here;
    # the automatic __eq__ implementation from dataclasses allows comparison
    # against flexible types as long as they match the inner fields.
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Symbol):
            raise TypeError("Symbol instances can only be compared against other Symbol instances")

        return self.name == other.name


@dataclass(frozen=True, slots=True, order=True)
class PyVersion:
    """
    Represents a (major, minor) version of Python.

    Patch and other version metadata is not included.
    """

    major: int
    minor: int

    @classmethod
    def parse(cls, val: str) -> PyVersion:
        major, minor = val.split(".", 1)
        return cls(major=int(major), minor=int(minor))


@dataclass(frozen=True, slots=True)
class Macro:
    """
    Represents a C/C++ macro in the context of the limited API.

    The value of the macro is not given, as it is not guaranteed to be
    stable.

    This type corresponds to limited API features that are described as
    "const" and "macro".
    """

    name: str
    added: PyVersion


@dataclass(frozen=True, slots=True)
class OpaqueStruct:
    """
    Represents a struct defined by the limited API but considered "opaque"
    in the stable ABI, meaning that it is only referenced via pointers
    and not with respect to its members.
    """

    name: str
    added: PyVersion


@dataclass(frozen=True, slots=True)
class PartialStruct:
    """
    Represents a struct defined by the limited API but considered "partial"
    in the stable ABI, meaning that only the members listed are guaranteed
    not to change.
    """

    name: str
    added: PyVersion
    members: List[str]


@dataclass(frozen=True, slots=True)
class FullStruct:
    """
    Represents a struct defined by the limited API that is considered "full"
    in the stable ABI, meaning that its members and layout are guaranteed
    not to change.
    """

    name: str
    added: PyVersion


Struct = OpaqueStruct | PartialStruct | FullStruct


@dataclass(frozen=True, slots=True)
class FeatureMacro:
    """
    Represents a C/C++ macro that controls the availability of other
    components of the limited API and/or stable ABI.
    """

    name: str
    doc: str
    windows: bool | Literal["maybe"]


@dataclass(frozen=True, slots=True)
class Function:
    """
    Represents a function defined in the limited API and/or stable ABI.

    `ifdef` is an optional C/C++ macro that controls the function's availability
    in a particular CPython build.

    `abi_only` indicates that the function is only part of the stable ABI, and
    **not** the limited API. This generally happens when the function is
    private (i.e. starts with `_Py`) but is called via a public macro,
    or was once part of the limited API but is now only part of the stable ABI
    for compatibility purposes.
    """

    symbol: Symbol
    added: PyVersion
    ifdef: Optional[FeatureMacro]
    abi_only: bool


@dataclass(frozen=True, slots=True)
class Data:
    """
    Represents an exported object in the limited API and/or stable ABI.

    This model is identical in behavior and semantics to `Function`, except
    that the object described is some kind of addressable data instead
    of a function.
    """

    symbol: Symbol
    added: PyVersion
    ifdef: Optional[FeatureMacro]
    abi_only: bool


@dataclass(frozen=True, slots=True)
class Typedef:
    name: str
    added: PyVersion
