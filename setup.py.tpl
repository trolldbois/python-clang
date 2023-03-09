#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

long_description="""This is the python bindings subdir of llvm clang repository.
https://github.com/llvm/llvm-project/tree/main/clang/bindings/python

This is a non-official packaging directly from the debian packages for the purpose of pypi package.
"""

setup(
    name="clang",
    version="%VERSION%",
    description="libclang python bindings",
    long_description=long_description,
    url="http://clang.llvm.org/",
    download_url="http://llvm.org/releases/download.html",
    license="Apache-2.0 with LLVM exception",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Software Development :: Compilers",
        "Programming Language :: Python :: %PYTHON_VERSION%",
    ],
    keywords=["llvm", "clang", "libclang"],
    author="LLVM team - pypi upload by Loic Jaquemet",
    zip_safe=False,
    packages=["clang"],
    # if use nose.collector, many plugins not is avaliable
    # see: http://nose.readthedocs.org/en/latest/setuptools_integration.html
    #test_suite="nose.collector",
    #tests_require=['nose']
)
