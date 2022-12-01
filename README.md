abi3info
========

[![CI](https://github.com/woodruffw/abi3info/actions/workflows/ci.yml/badge.svg)](https://github.com/woodruffw/abi3info/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/abi3info.svg)](https://pypi.org/project/abi3info)

abi3info exposes information about CPython's "limited API" (including the
stable ABI, called `abi3`) as a Python library.

## Installation

abi3info is available via `pip`:

```console
$ pip install abi3info
```

## Usage

abi3info exposes limited API and stable ABI information in the form of a set
of top-level dictionaries, namely:

```python
import abi3info

abi3info.FEATURE_MACROS
abi3info.MACROS
abi3info.STRUCTS
abi3info.TYPEDEFS
abi3info.FUNCTIONS
abi3info.DATAS
```

Each of these is a mapping of a name (either as `str` or `Symbol`) to
a data model describing the kind of item (e.g. `FeatureMacro` or `Function`).

[See the generated documentation](https://woodruffw.github.io/abi3info) for
more details, including comprehensive type hints and explanations of each data
model.

[See also the `stable_abi.toml` file](./codegen/stable_abi.toml), taken from
the CPython sources, which describes each model and their semantics.

### Examples

Get information about a particular function:

```python
from abi3info import FUNCTIONS
from abi3info.models import Symbol

func = FUNCTIONS[Symbol("_Py_NegativeRefcount")]
print(func.symbol, func.added, func.ifdef, func.abi_only)
```

Get information about the feature macros that control the limited API:

```python
from abi3info import FEATURE_MACROS

print(fm for fm in FEATURE_MACROS.values())
```

## Licensing

abi3info is licensed under the MIT license.

abi3info is partially generated from metadata retrieved from the
[CPython sources](https://github.com/python/cpython/blob/main/Misc/stable_abi.toml),
which is licensed under the [PSF license](https://docs.python.org/3/license.html#psf-license).
