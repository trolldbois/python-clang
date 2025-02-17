# Clang Python package for PyPI

This is the python bindings subdir of llvm clang repository.
https://github.com/llvm/llvm-project/tree/main/clang/bindings/python

The debian packages are pulled from llvm repo, extracted and pushed to pypi.

## Installation

You can install the package using pip:

```bash
pip install clang
```

Or for a specific version:

```bash
pip install clang==19
```

## License

This repository follows the [license agreement](https://github.com/llvm/llvm-project/blob/main/LICENSE.TXT) of the LLVM project, see Apache-2.0 WITH LLVM-exception.

## Release SOP

- GitHub Workflows will create new pull requests when LLVM releases new versions.
- Merge the PR
- Create a new release, with a new tag "v<version>". 
- The creation of the tag will trigger a push, which will trigger the release/pypi upload workflow, through Trusted Publishing
