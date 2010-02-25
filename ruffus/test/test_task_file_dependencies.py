#!/usr/bin/env python
################################################################################
#
#   test_task_file_dependencies.py
#
#
#   Copyright (c) 2009 Leo Goodstadt
#   
#   Permission is hereby granted, free of charge, to any person obtaining a copy
#   of this software and associated documentation files (the "Software"), to deal
#   in the Software without restriction, including without limitation the rights
#   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#   copies of the Software, and to permit persons to whom the Software is
#   furnished to do so, subject to the following conditions:
#   
#   The above copyright notice and this permission notice shall be included in
#   all copies or substantial portions of the Software.
#   
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#   THE SOFTWARE.
#################################################################################
"""
    test_task_file_dependencies.py
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

class Test_needs_update_check_modify_time(unittest.TestCase):

    def setUp (self):
        """
        Create a list of files separated in time so we can do dependency checking
        """
        import tempfile,time
        self.files  = list()
        for i in xrange(6):
            #test_file =tempfile.NamedTemporaryFile(delete=False, prefix='testing_tmp')
            #self.files.append (test_file.name)
            #test_file.close()
            
            fh, temp_file_name = tempfile.mkstemp(suffix='.dot')
            self.files.append (temp_file_name)
            os.fdopen(fh, "w").close()
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
                                                              self.files[2:6])[0])
        self.assert_(    task.needs_update_check_modify_time (self.files[2:6], 
                                                              self.files[0:2])[0])
        #
        #   singletons and lists of files
        # 
        self.assert_(not task.needs_update_check_modify_time (self.files[0], 
                                                              self.files[2:6])[0])
        self.assert_(    task.needs_update_check_modify_time (self.files[2:6], 
                                                              self.files[0])[0])
        #
        #   singletons
        # 
        self.assert_(    task.needs_update_check_modify_time (self.files[3], 
                                                              self.files[0])[0])
        self.assert_(    task.needs_update_check_modify_time (self.files[0], 
                                                              self.files[0])[0])
        
        #
        #   missing files means need update
        # 
        self.assert_(    task.needs_update_check_modify_time (self.files[0:2] + 
                                                                        ["uncreated"], 
                                                              self.files[3:6])[0])
        self.assert_(    task.needs_update_check_modify_time (self.files[0:2], 
                                                              self.files[3:6] +
                                                                        ["uncreated"])[0])
        #
        #   None means need update
        # 
        self.assert_(    task.needs_update_check_modify_time (self.files[0:2], 
                                                              None)[0])
        #
        #   None input means need update only if do not exist
        # 
        self.assert_( not task.needs_update_check_modify_time (None, 
                                                              self.files[3:6])[0])


        #
        #   None + missing file means need update
        # 
        self.assert_(    task.needs_update_check_modify_time (self.files[0:2] + 
                                                                        ["uncreated"], 
                                                              None)[0])
        self.assert_(    task.needs_update_check_modify_time (None, 
                                                              self.files[3:6] + 
                                                                        ["uncreated"])[0])

        
        
       
                       
unittest.main()

