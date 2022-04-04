#!/bin/bash

set -e

CURRENT_BRANCH=`git rev-parse --abbrev-ref HEAD`

make clean
make ghpages

git switch gh-pages

for dirname in html/*
do
    vername=${dirname##*/}
    rm -rf "$vername"
    mv "$dirname" "$vername"
    git add "$vername"
done
rmdir html/

git commit -m "publish.sh: Add HTML docs"
git push origin gh-pages

git switch $CURRENT_BRANCH
