#!/bin/sh

cd ~/compil/llvm/llvm/tools/clang/bindings/
git checkout master
COMMIT=`git log | head -n 1`
cd ~/compil/llvm/llvm/
REV=`svn info | grep Revision`
cd ~/compil/python-clang

git checkout master

cp -a ~/compil/llvm/llvm/tools/clang/bindings/python/clang .
cp -a ~/compil/llvm/llvm/tools/clang/bindings/python/examples .
cp -a ~/compil/llvm/llvm/tools/clang/bindings/python/tests .

git add clang examples tests
git commit -m "llvm-mirror/clang $COMMIT $REV"
git push
