[![Build Status](https://travis-ci.org/trolldbois/python-clang.svg?branch=master)](https://travis-ci.org/trolldbois/python-clang)
[![pypi](https://img.shields.io/pypi/dm/clang.svg)](https://pypi.python.org/pypi/clang)
[![Coverage Status](https://coveralls.io/repos/trolldbois/python-clang/badge.svg)](https://coveralls.io/r/trolldbois/python-clang)

//===----------------------------------------------------------------------===//
// Clang Python Bindings
//===----------------------------------------------------------------------===//

This is the python bindings subdir of llvm clang repository.
https://github.com/llvm-mirror/clang/tree/master/bindings/python

This is a non-official fork. Mainly for Pypi packaging purposes.
The pypi package is not official either.

Test:
-----
You may need to alter LD_LIBRARY_PATH so that the Clang library can be
found. The unit tests are designed to be run with 'nosetests'. For example:
--
$ env PYTHONPATH=$(echo ~/llvm/tools/clang/bindings/python/) \
      LD_LIBRARY_PATH=$(llvm-config --libdir) \
  nosetests -v
tests.cindex.test_index.test_create ... ok
...


