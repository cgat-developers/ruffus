#!/usr/bin/env python
from time import sleep
import random
import sys

try:
    for i in range(50):
        sleep(1)
        #if random.randint(5) == 4:
        #    print >> sys.stderr,  "Throw"
        #    raise Exception("WWWWW")
        print >> sys.stderr, i,
    sleep(1)
    print >> sys.stderr,  "Done"
except:
    print >> sys.stderr,  "Exception!!!!!!!!!!!!!!!!!!!!!"
    pass
