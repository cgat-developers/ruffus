#!/usr/bin/env python
"""
    test_follows_mkdir.py
    
"""

# use simplejson in place of json for python < 2.6
try:
    import json
except ImportError:
    import simplejson
    json = simplejson
import unittest, os,sys
if __name__ != '__main__':
    raise Exception ("This is not a callable module [%s]"  % __main__)


exe_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
sys.path.insert(0, os.path.abspath(os.path.join(exe_path,"..", "..")))
from ruffus import *

directories = [os.path.abspath('a'), 'b']    
@follows(mkdir(directories), mkdir('c'), mkdir('d', 'e'), mkdir('e'))
def task_which_makes_directories ():
    pass


import unittest

class Test_task_mkdir(unittest.TestCase):

    def setUp (self):
        """
        """
        pass
        
    def tearDown (self):
        """
        delete directories
        """
        for d in 'abcde':
            fullpath = os.path.join(exe_path, d)
            os.rmdir(fullpath)


    def test_mkdir (self):
        pipeline_run([task_which_makes_directories])
        
        for d in 'abcde':
            fullpath = os.path.join(exe_path, d)
            self.assert_(os.path.exists(fullpath))


if __name__ == '__main__':
    try:
        unittest.main()
    except Exception, e:
        print e
