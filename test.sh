#!/usr/bin/env bash

for file in $(ls src/*.py)
do
	mypy $file
done

# python3 -m unittest discover -s src
