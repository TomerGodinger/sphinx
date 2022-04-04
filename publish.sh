#!/bin/bash
for dirname in html/*
do
    vername=${dirname##*/}
    mv "$dirname" "$vername"
    git add "$vername"
done
rmdir html/

git commit -m "publish.sh: Add HTML docs"
git push origin gh-pages
