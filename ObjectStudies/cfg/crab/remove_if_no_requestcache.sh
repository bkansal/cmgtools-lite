#!/bin/sh
for dir in `find . -mindepth 2 -maxdepth 2 -type d '!' -exec test -e "{}/.requestcache" ';' -print`; do echo "Removing $dir"; rm -rf $dir; done
