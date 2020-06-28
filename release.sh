#!/bin/sh

echo "== cleaning dist folder"
rm -v dist/*

echo "== Creating distribution"
venv/bin/python setup.py sdist
venv/bin/python setup.py bdist_wheel

echo "== Upload distribution"
twine upload dist/*
