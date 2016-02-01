from __future__ import unicode_literals

from clang.cindex import CompilationDatabase
from clang.cindex import CompilationDatabaseError
import os
import gc

kInputsDir = os.path.join(os.path.dirname(__file__), 'INPUTS')


def test_create_fail():
    """Check we fail loading a database with an assertion"""
    path = os.path.dirname(__file__)
    try:
        CompilationDatabase.fromDirectory(path)
    except CompilationDatabaseError as e:
        assert e.cdb_error == CompilationDatabaseError.ERROR_CANNOTLOADDATABASE
    else:
        assert False


def test_create():
    """Check we can load a compilation database"""
    CompilationDatabase.fromDirectory(kInputsDir)


def test_lookup_fail():
    """Check file lookup failure"""
    cdb = CompilationDatabase.fromDirectory(kInputsDir)
    assert cdb.getCompileCommands('file_do_not_exist.cpp') is None


def test_lookup_succeed():
    """Check we get some results if the file exists in the db"""
    cdb = CompilationDatabase.fromDirectory(kInputsDir)
    cmds = cdb.getCompileCommands('/home/john.doe/MyProject/project.cpp')
    assert len(cmds) != 0


def test_all_compilecommand():
    """Check we get all results from the db"""
    cdb = CompilationDatabase.fromDirectory(kInputsDir)
    cmds = cdb.getAllCompileCommands()
    assert len(cmds) == 3
    expected = [
        {
            'wd': b'/home/john.doe/MyProjectA',
            'line': [
                b'clang++',
                b'-o', b'project2.o',
                b'-c', b'/home/john.doe/MyProject/project2.cpp'
            ]
        },
        {
            'wd': b'/home/john.doe/MyProjectB',
            'line': [
                b'clang++',
                b'-DFEATURE=1',
                b'-o', b'project2-feature.o',
                b'-c', b'/home/john.doe/MyProject/project2.cpp'
            ]
        },
        {
            'wd': b'/home/john.doe/MyProject',
            'line': [
                b'clang++',
                b'-o', b'project.o',
                b'-c', b'/home/john.doe/MyProject/project.cpp'
            ]
        }
    ]
    for i in range(len(cmds)):
        assert cmds[i].directory == expected[i]['wd']
        for arg, exp in zip(cmds[i].arguments, expected[i]['line']):
            assert arg == exp


def test_1_compilecommand():
    """Check file with single compile command"""
    cdb = CompilationDatabase.fromDirectory(kInputsDir)
    cmds = cdb.getCompileCommands('/home/john.doe/MyProject/project.cpp')
    assert len(cmds) == 1
    assert cmds[0].directory == b'/home/john.doe/MyProject'
    expected = [
        b'clang++',
        b'-o', b'project.o',
        b'-c', b'/home/john.doe/MyProject/project.cpp'
    ]
    for arg, exp in zip(cmds[0].arguments, expected):
        assert arg == exp


def test_2_compilecommand():
    """Check file with 2 compile commands"""
    cdb = CompilationDatabase.fromDirectory(kInputsDir)
    cmds = cdb.getCompileCommands('/home/john.doe/MyProject/project2.cpp')
    assert len(cmds) == 2
    expected = [
        {
            'wd': b'/home/john.doe/MyProjectA',
            'line': [
                b'clang++',
                b'-o', b'project2.o',
                b'-c', b'/home/john.doe/MyProject/project2.cpp'
            ]
        },
        {
            'wd': b'/home/john.doe/MyProjectB',
            'line': [
                b'clang++',
                b'-DFEATURE=1',
                b'-o', b'project2-feature.o',
                b'-c', b'/home/john.doe/MyProject/project2.cpp'
            ]
        }
    ]
    for i in range(len(cmds)):
        assert cmds[i].directory == expected[i]['wd']
        for arg, exp in zip(cmds[i].arguments, expected[i]['line']):
            assert arg == exp


def test_compilecommand_iterator_stops():
    """Check that iterator stops after the correct number of elements"""
    cdb = CompilationDatabase.fromDirectory(kInputsDir)
    count = 0
    for cmd in cdb.getCompileCommands('/home/john.doe/MyProject/project2.cpp'):
        count += 1
        assert count <= 2


def test_compilationDB_references():
    """Ensure CompilationsCommands are independent of the database"""
    cdb = CompilationDatabase.fromDirectory(kInputsDir)
    cmds = cdb.getCompileCommands('/home/john.doe/MyProject/project.cpp')
    del cdb
    gc.collect()
    cmds[0].directory


def test_compilationCommands_references():
    """Ensure CompilationsCommand keeps a reference to CompilationCommands"""
    cdb = CompilationDatabase.fromDirectory(kInputsDir)
    cmds = cdb.getCompileCommands('/home/john.doe/MyProject/project.cpp')
    del cdb
    cmd0 = cmds[0]
    del cmds
    gc.collect()
    cmd0.directory
