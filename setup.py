#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(name="clang",
    version="3.3",
    description="libclang python bindings",
    long_description=open("README.txt").read(),
    url="https://github.com/trolldbois/python-clang",
    download_url="https://github.com/trolldbois/python-clang/releases",
    license="License :: OSI Approved :: University of Illinois/NCSA Open Source License",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Software Development :: Compilers"
    ],
    keywords=["llvm","clang","libclang"],
    author="Loic Jaquemet", # meeeh... not.
    author_email="loic.jaquemet+python@gmail.com",
    packages = ["clang"],
    # use pip requirements.txt instead
    # install_requires = ["libclang"],
    # build_tests_requires = ["libclang"],
    test_suite= "test.alltests",
)


