#!/bin/bash

python setup.py build
if [ "$?" != "0" ]; then
	exit 1
fi
python setup.py install
