#!/usr/bin/env python
"""
    test_task_misc.py
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

        
        
   
class Test_needs_update_check_directory_missing(unittest.TestCase):

    def setUp (self):
        """
        Create temp directory and temp file
        """
        import tempfile

        #test_file =tempfile.NamedTemporaryFile(delete=False)
        #self.tempfile = test_file.name
        #test_file.close()
        fh, self.tempfile = tempfile.mkstemp(suffix='.dot')
        os.fdopen(fh, "w").close()
        self.directory = tempfile.mkdtemp(prefix='testing_tmp')
        
    def tearDown (self):
        """
        delete files
        """
        os.unlink(self.tempfile)
        os.removedirs(self.directory)        
        
    def test_up_to_date (self):
        #
        #   lists of files
        # 
        
        self.assert_(not task.needs_update_check_directory_missing ([self.directory])[0])
        self.assert_(    task.needs_update_check_directory_missing (["missing directory"])[0])
        self.assertRaises(task.error_not_a_directory,
                            task.needs_update_check_directory_missing, [self.tempfile])

        
       
                       
unittest.main()

