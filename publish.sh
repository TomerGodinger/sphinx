#!/bin/bash
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
