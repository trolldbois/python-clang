[![PyPI](https://img.shields.io/pypi/v/clang)](https://pypi.org/project/clang)
![Python](https://img.shields.io/pypi/pyversions/clang)
![Downloads](https://img.shields.io/pypi/dw/clang)
[![License](https://img.shields.io/pypi/l/clang)](https://github.com/trolldbois/clang/blob/master/LICENSE.TXT)

# Clang Python package for PyPI

This repository builds and releases the [clang package on pypi](https://pypi.org/project/clang/) .

The wheel is built from the LLVM libclang python binding source code directly. Thanks @nightlark for the 2025 refresh of the build process.

This package does not contain binary files for the libclang library, only the python bindings.


## Installation

You can install the package using pip:

```bash
pip install clang
```

Or for a specific version:

```bash
pip install clang==20
```

## License

This repository follows the [license agreement](https://github.com/llvm/llvm-project/blob/main/LICENSE.TXT) of the LLVM project, see Apache-2.0 WITH LLVM-exception.

## Release SOP

- GitHub Workflows will create new pull requests weekly when LLVM releases new major versions. You can always manually trigger the GitHub Actions.
- Merge the PR created by GH Action.
- Create a new release, with a new tag "v<version>". 
- The creation of the tag will trigger a push, which will trigger the release/pypi upload workflow, through Trusted Publishing
