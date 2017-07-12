#!/bin/sh

echo "== cleaning dist folder"
rm -v dist/*

echo "== Creating distribution"
python setup.py sdist
python setup.py bdist_wheel

echo "== Upload distribution"
twine upload dist/*
