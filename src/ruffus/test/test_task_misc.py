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
sys.path.append(os.path.abspath(os.path.join(exe_path,"..", "..")))
from ruffus import *

class TestMiscFunctions(unittest.TestCase):

    #       self.assertEqual(self.seq, range(10))
    #       self.assert_(element in self.seq)
    #       self.assertRaises(ValueError, random.sample, self.seq, 20)



    def test_is_str(self):
        """
            task.is_str()
        """
        test_str1 = "asfas"
        test_str2 = str()
        test_str3 = list(test_str1)
        test_str4 = list(test_str2)
        self.assert_(task.is_str(test_str1))
        self.assert_(task.is_str(test_str2))
        self.assert_(not task.is_str(test_str3))
        self.assert_(not task.is_str(test_str4))
        
    def test_non_str_sequence (self):
        """
            task.is_str()
        """
        test_str1 = "asfas"
        class inherited_str (str):
            #
            # use __new__ instead of init because str is immutable
            #
            def __new__( cls, a):               
                obj = super( inherited_str, cls).__new__( inherited_str, a )
                return obj                          
                
        test_str2 = inherited_str("test")
        class inherited_list (list):
            def __init__ (self, *param):
                list.__init__(self, *param)
        test_str3 = list(test_str1)
        test_str4 = inherited_list(test_str2)
        self.assert_(not task.non_str_sequence(test_str1))
        self.assert_(not task.non_str_sequence(test_str2))
        self.assert_(task.non_str_sequence(test_str3))
        self.assert_(task.non_str_sequence(test_str4))
        
        
    def test_ioparam_to_str (self):
        self.assert_(task.ioparam_to_str(None) == '')
        self.assert_(task.ioparam_to_str('test') == "'test'")
        self.assert_(task.ioparam_to_str(['test1', 'test2']) == "'test1', 'test2'")

    
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
        
        self.assert_(not task.needs_update_check_directory_missing ([self.directory]))
        self.assert_(    task.needs_update_check_directory_missing (["missing directory"]))
        self.assertRaises(task.error_not_a_directory,
                            task.needs_update_check_directory_missing, [self.tempfile])

        
       
                       
unittest.main()

