#!/usr/bin/env python
from time import sleep
import sys

try:
    for i in range(50):
        sleep(1)
        sys.stderr.write("{}\n".format(i))
    sleep(1)
    sys.stderr.write("Done\n")
except:
    sys.stderr.write("Exception!!!!!!!!!!!!!!!!!!!!!\n")
    pass
