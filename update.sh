#!/bin/bash

CLANG_GIT_MIRROR_REPOSITORY_URL=https://github.com/llvm-mirror/clang.git


PYTHON_CLANG_FOLDER=`pwd`

CLANG_TMP_BASE_FOLDER=/tmp/clang_git
CLANG_FOLDER_NAME=clang
CLANG_GIT_MIRROR_FOLDER=$CLANG_TMP_BASE_FOLDER/$CLANG_FOLDER_NAME

#
#CLANG_GIT_MIRROR_FOLDER=/home/myuser/Desktop/clang_git


if [ -d "$CLANG_GIT_MIRROR_FOLDER" ]; then
  echo
  cd $CLANG_GIT_MIRROR_FOLDER
  REMOTE_REPO=`git remote -v | awk '{print $1}' | head -n 1`
  REMOTE_REPO_URL=`git remote -v | awk '{print $2}' | head -n 1`
  if [ "$REMOTE_REPO" == "origin" ] && [ "$REMOTE_REPO_URL" == "$CLANG_GIT_MIRROR_REPOSITORY_URL" ]; then
      echo "#############################################"
      echo "$CLANG_GIT_MIRROR_FOLDER folder was detected"
      echo "It was found that there is already a local copy of the Clang source code"
      echo "The local copy will be updated now."
      echo "sync repro..."
      git fetch --progress --prune origin
      COMMIT=`git rev-parse HEAD`
      git checkout --quiet $COMMIT
      git update-ref refs/heads/master $COMMIT
      git symbolic-ref HEAD refs/heads/master
      echo "Done"
      echo "#############################################"
  fi

else
    echo "#############################################"
    echo "Cloning Clang repo from $CLANG_GIT_MIRROR_REPOSITORY_URL"
    mkdir -p $CLANG_TMP_BASE_FOLDER
    git clone --recursive -b master --single-branch $CLANG_GIT_MIRROR_REPOSITORY_URL $CLANG_GIT_MIRROR_FOLDER
    echo "Done"
    cd $CLANG_GIT_MIRROR_FOLDER
    echo "#############################################"
fi


COMMIT=`git rev-parse HEAD`

cd $PYTHON_CLANG_FOLDER

git checkout master

echo "Removing old files..."
rm -rf $PYTHON_CLANG_FOLDER/clang
rm -rf $PYTHON_CLANG_FOLDER/examples
rm -rf $PYTHON_CLANG_FOLDER/tests

echo ""
echo "Copying new files"
cp -a $CLANG_GIT_MIRROR_FOLDER/bindings/python/clang $PYTHON_CLANG_FOLDER/
cp -a $CLANG_GIT_MIRROR_FOLDER/bindings/python/examples $PYTHON_CLANG_FOLDER/
cp -a $CLANG_GIT_MIRROR_FOLDER/bindings/python/tests $PYTHON_CLANG_FOLDER/

git add clang examples tests -v
git commit -m "updated from https://github.com/llvm-mirror/clang.git - Last commit llvm-mirror/clang/commit/$COMMIT"
echo "#############################################"
# git push
