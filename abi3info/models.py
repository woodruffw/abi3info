"""
Data models for the CPython limited API and stable ABI.
"""

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
    """
    The symbol's underlying name. This may not correspond to an actual symbol
    in a binary without platform-specific normalization.
    """

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
        """
        Checks the equality of this `Symbol` against another.
        """
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
    """
    The major version.
    """

    minor: int
    """
    The minor version.
    """

    @classmethod
    def parse(cls, val: str) -> PyVersion:
        """
        Attempts to parse a `PyVersion` version from the given string.

        The string is expected to be in `major.minor` format. Other
        formats are not supported.
        """
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
    """
    The macro's name.
    """

    added: PyVersion
    """
    When this macro was added to the limited API.
    """


@dataclass(frozen=True, slots=True)
class OpaqueStruct:
    """
    Represents a struct defined by the limited API but considered "opaque"
    in the stable ABI, meaning that it is only referenced via pointers
    and not with respect to its members.
    """

    name: str
    """
    The struct's name.
    """

    added: PyVersion
    """
    When this struct was added to the limited API.
    """


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
    """
    The feature macro's name.
    """

    doc: str
    """
    A human-readable documentation string, explaining the feature macro's purpose.
    """

    windows: bool | Literal["maybe"]
    """
    The feature macro's applicability on Windows.

    The `"maybe"` literal indicates that the macro *can* be defined on Windows
    builds but is not necessarily defined, unlike `True`.
    """


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
    """
    The function's symbol.
    """

    added: PyVersion
    """
    When this function was added to the limited API and stable ABI.
    """

    ifdef: Optional[FeatureMacro]
    """
    The feature macro that controls this function's presence.

    If `None`, this function is always present.
    """

    abi_only: bool
    """
    Whether this function is present only in the stable ABI and **not** the limited API.
    """


@dataclass(frozen=True, slots=True)
class Data:
    """
    Represents an exported object in the limited API and/or stable ABI.

    This model is identical in behavior and semantics to `Function`, except
    that the object described is some kind of addressable data instead
    of a function.
    """

    symbol: Symbol
    """
    The data object's symbol.
    """

    added: PyVersion
    """
    When this data object was added to the limited API and stable ABI.
    """

    ifdef: Optional[FeatureMacro]
    """
    The feature macro that controls this data object's presence.

    If `None`, this data object is always present.
    """

    abi_only: bool
    """
    Whether this data object is present only in the stable ABI and **not** the limited API.
    """


@dataclass(frozen=True, slots=True)
class Typedef:
    """
    Represents a `typedef`'d type in the limited API.
    """

    name: str
    """
    The name of this typedef.
    """

    added: PyVersion
    """
    When this typedef was added to the limited API.
    """
