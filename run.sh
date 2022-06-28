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

echo "Combination 3: K=10, N=100"
python3 frequency_assignment.py -v -u 10 -f 100

echo "Combination 4: K=20, N=50"
python3 frequency_assignment.py -v -u 20 -f 50

echo "Combination 5: K=20, N=100"
python3 frequency_assignment.py -v -u 20 -f 100

echo "Combination 6: K=45, N=100"
python3 frequency_assignment.py -v -u 45 -f 100
