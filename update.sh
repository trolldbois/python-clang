#!/bin/bash
#
# Because the llvm-mirror/clang repo has no stand alone repo for python
# bindings, we have created https://github.com/trolldbois/python-clang .
# we can them push that package to Pypi https://pypi.python.org/pypi/clang .
# This repository really contains python setup.py and some fixes in 
# alternate branches
#
# The idea of this update.sh script is 
# Step a) to sync llvm, and the clang tool subfolder for the local repo
#  llvm master is required to compile clang master.
#
# Step b) python-clang update our local repo master branch 
#  with llvm-mirror/clang/bindings/python master files
#
# Step c) suggest to merge master with whatever local branch you are working on
#
#

# Tune this
LLVM_LOCAL_REPO=~/compil/new/llvm
PYTHON_CLANG_LOCAL_REPO=~/compil/new/python-clang

if [ ! -v LLVM_LOCAL_REPO -o ! -v PYTHON_CLANG_LOCAL_REPO ]; then
    echo "Please fix this script."
    exit 1
fi

# we do not intend to clone, push nor pull from that local repo 
SHALLOW_GIT="--depth=10"


LLVM_GIT_REPOSITORY_URL=https://github.com/llvm-mirror/llvm.git
CLANG_GIT_REPOSITORY_URL=https://github.com/llvm-mirror/clang.git
CLANG_LOCAL_REPO=$LLVM_LOCAL_REPO/tools/clang


CURCWD=`pwd`

# get llvm if required
if [ ! -d "$LLVM_LOCAL_REPO" ]; then
    echo "#############################################"
    echo "Cloning LLVM repo from $LLVM_GIT_REPOSITORY_URL"
    mkdir -p $LLVM_LOCAL_REPO
    echo git clone --recursive -b master --single-branch $SHALLOW_GIT $LLVM_GIT_REPOSITORY_URL $LLVM_LOCAL_REPO
    git clone --recursive -b master --single-branch $SHALLOW_GIT $LLVM_GIT_REPOSITORY_URL $LLVM_LOCAL_REPO
    if [ $? -ne 0 ]; then
        echo "Error while clone-ing llvm master - Aborting"
        exit 1
    fi
    echo "#############################################"
else
    # otherwise sync it
    echo "#############################################"
    echo "updating llvm local repository"
    cd $LLVM_LOCAL_REPO
    git checkout master
    if [ $? -ne 0 ]; then
        echo "Error while checking out llvm master - Aborting"
        exit 1
    fi
    echo "git pull $LLVM_GIT_REPOSITORY_URL master"
    git pull $LLVM_GIT_REPOSITORY_URL master
    if [ $? -ne 0 ]; then
        echo "Error while pull-ing llvm master - Aborting"
        exit 1
    fi
    echo "#############################################"
fi

cd $CURCWD

# get clang in llvm tools folder if required
if [ ! -d "$CLANG_LOCAL_REPO" ]; then
    echo "#############################################"
    echo "Cloning CLANG repo from $CLANG_GIT_REPOSITORY_URL"
    mkdir -p $CLANG_LOCAL_REPO
    echo git clone --recursive -b master --single-branch $SHALLOW_GIT $CLANG_GIT_REPOSITORY_URL $CLANG_LOCAL_REPO
    git clone --recursive -b master --single-branch $SHALLOW_GIT $CLANG_GIT_REPOSITORY_URL $CLANG_LOCAL_REPO
    if [ $? -ne 0 ]; then
        echo "Error while clone-ing clang master - Aborting"
        exit 1
    fi
    echo "#############################################"
else
    # otherwise sync it
    echo "#############################################"
    echo "updating clang local repository"
    cd $CLANG_LOCAL_REPO
    git checkout master
    if [ $? -ne 0 ]; then
        echo "Error while checking out clang master - Aborting"
        exit 1
    fi
    echo "git pull $CLANG_GIT_REPOSITORY_URL master"
    git pull $CLANG_GIT_REPOSITORY_URL master
    if [ $? -ne 0 ]; then
        echo "Error while pull-ing clang master - Aborting"
        exit 1
    fi
    echo "#############################################"
fi

# prepping the commit log for python-clang
cd $CLANG_LOCAL_REPO
COMMIT=`git rev-parse HEAD`

cd $PYTHON_CLANG_LOCAL_REPO
git checkout master
if [ $? -ne 0 ]; then
    echo "** Error while switching to python-clang master branch - Aborting"
    exit 1
fi

echo "Removing old files..."
rm -rf $PYTHON_CLANG_LOCAL_REPO/clang
rm -rf $PYTHON_CLANG_LOCAL_REPO/examples
rm -rf $PYTHON_CLANG_LOCAL_REPO/tests

echo ""
echo "Copying new files"
cp -a $CLANG_LOCAL_REPO/bindings/python/clang $PYTHON_CLANG_LOCAL_REPO/
cp -a $CLANG_LOCAL_REPO/bindings/python/examples $PYTHON_CLANG_LOCAL_REPO/
cp -a $CLANG_LOCAL_REPO/bindings/python/tests $PYTHON_CLANG_LOCAL_REPO/

git add clang examples tests -v
git commit -m "updated from https://github.com/llvm-mirror/clang.git - Last commit llvm-mirror/clang/commit/$COMMIT"
echo "#############################################"
# git push
