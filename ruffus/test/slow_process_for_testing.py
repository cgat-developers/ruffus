#!/usr/bin/env python
from __future__ import print_function
import sys
import os
import time
print("    ", os.getcwd(), file=sys.stderr)
print("    ", os.environ, file=sys.stderr)
loop_variable = 0
loop_limit = 4
while True:
    if loop_variable >= loop_limit:
        break
    try:
        sys.stderr.write("    Stderr %d\n" % loop_variable)
        sys.stderr.flush()
        sys.stdout.write("    Stdout %d\n" % loop_variable)
        sys.stdout.flush()
        loop_variable += 1
        time.sleep(0.5)
    except:
        sys.stderr.write(
            "    Ignore Exception. Now you have made me angry: I won't stop till 100\n")
        loop_limit = 100
        pass
