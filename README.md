abi3info
========

[![CI](https://github.com/woodruffw/abi3info/actions/workflows/ci.yml/badge.svg)](https://github.com/woodruffw/abi3info/actions/workflows/ci.yml)

abi3info exposes information about CPython's "limited API" (including the
stable ABI, called `abi3`) as a Python library.

## Installation

abi3info is available via `pip`:

```console
$ pip install abi3info
```

## Licensing

abi3info is licensed under the MIT license.

abi3info is partially generated from metadata retrieved from the
[CPython sources](https://github.com/python/cpython/blob/main/Misc/stable_abi.toml),
which is licensed under the [PSF license](https://docs.python.org/3/license.html#psf-license).
