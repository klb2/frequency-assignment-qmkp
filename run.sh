#!/bin/sh

# ...
# Information about the paper...
# ...
#
# Copyright (C) 20XX ...
# License: GPLv3

echo "Combination 1: K=3, N=10"
python3 frequency_assignment.py -v -u 3 -f 10

echo "Combination 2: K=3, N=100"
python3 frequency_assignment.py -v -u 3 -f 100

echo "Combination 1: K=10, N=100"
python3 frequency_assignment.py -v -u 10 -f 100

echo "Combination 1: K=20, N=100"
python3 frequency_assignment.py -v -u 20 -f 100
