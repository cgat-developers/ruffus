#!/usr/bin/env python
"""
    test_task_misc.py
"""

import json
import unittest, os,sys
if __name__ != '__main__':
    raise Exception ("This is not a callable module [%s]"  % __main__)


exe_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
sys.path.append(os.path.abspath(os.path.join(exe_path,"..", "..")))
from ruffus import *

class Test_needs_update_check_modify_time(unittest.TestCase):

    def setUp (self):
        """
        Create a list of files separated in time so we can do dependency checking
        """
        import tempfile,time
        self.files  = list()
        for i in xrange(6):
            test_file =tempfile.NamedTemporaryFile(delete=False, prefix='testing_tmp')
            self.files.append (test_file.name)
            test_file.close()
            time.sleep(1.1)
        
    def tearDown (self):
        """
        delete files
        """
        for f in self.files:
            os.unlink(f)
        
        
    def test_up_to_date (self):
        #
        #   lists of files
        # 
        self.assert_(not task.needs_update_check_modify_time (self.files[0:2], 
                                                              self.files[2:6]))
        self.assert_(    task.needs_update_check_modify_time (self.files[2:6], 
                                                              self.files[0:2]))
        #
        #   singletons and lists of files
        # 
        self.assert_(not task.needs_update_check_modify_time (self.files[0], 
                                                              self.files[2:6]))
        self.assert_(    task.needs_update_check_modify_time (self.files[2:6], 
                                                              self.files[0]))
        #
        #   singletons
        # 
        self.assert_(    task.needs_update_check_modify_time (self.files[3], 
                                                              self.files[0]))
        self.assert_(    task.needs_update_check_modify_time (self.files[0], 
                                                              self.files[0]))
        
        #
        #   missing files means need update
        # 
        self.assert_(    task.needs_update_check_modify_time (self.files[0:2] + 
                                                                        ["uncreated"], 
                                                              self.files[3:6]))
        self.assert_(    task.needs_update_check_modify_time (self.files[0:2], 
                                                              self.files[3:6] +
                                                                        ["uncreated"]))
        #
        #   None means need update
        # 
        self.assert_(    task.needs_update_check_modify_time (self.files[0:2], 
                                                              None))
        #
        #   None input means need update only if do not exist
        # 
        self.assert_( not task.needs_update_check_modify_time (None, 
                                                              self.files[3:6]))


        #
        #   None + missing file means need update
        # 
        self.assert_(    task.needs_update_check_modify_time (self.files[0:2] + 
                                                                        ["uncreated"], 
                                                              None))
        self.assert_(    task.needs_update_check_modify_time (None, 
                                                              self.files[3:6] + 
                                                                        ["uncreated"]))

        
        
       
                       
unittest.main()

