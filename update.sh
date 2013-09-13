#!/bin/sh

cd ~/compil/llvm/llvm/clang/bindings/
COMMIT=`git log | head -n 1`

cd ~/compil/python-clang

cp -a ~/compil/llvm/llvm/clang/bindings/python/clang .
cp -a ~/compil/llvm/llvm/clang/bindings/python/examples .
cp -a ~/compil/llvm/llvm/clang/bindings/python/tests .

git add clang examples tests
git commit -m "$COMMIT"
git push
