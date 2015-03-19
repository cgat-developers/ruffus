#!/usr/bin/env python
from __future__ import print_function
import sys, os, time
print ("    ", os.getcwd(), file = sys.stderr)
print ("    ", os.environ, file = sys.stderr)
for ii in range(4):
    sys.stderr.write("    Stderr %d\n" % ii)
    sys.stderr.flush()
    sys.stdout.write("    Stdout %d\n" % ii)
    sys.stdout.flush()
    time.sleep(0.5)

