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

       
class Test_glob_regex_io_param_factory(unittest.TestCase):

    def setUp (self):
        """
        Create a list of files separated in time so we can do dependency checking
        """
        import tempfile,time
        self.directory = tempfile.mkdtemp(prefix='testing_tmp')
        self.files = list()
        self.iofiles_a_only = list()
        self.iofiles_a_only_output_only = list()
        for i in xrange(6):
            # starting file names
            test_file = open(os.path.join(self.directory, "a_file%d" % i), "w")
            test_file.write("%d" % i)
            self.files.append (test_file.name)
            test_file.close()
            
            # expected file names
            input_file_name  = os.path.join(self.directory, "input_file_name_%d" % i)
            output_file_name = os.path.join(self.directory, "output_file_name_%d" % i)
            self.iofiles_a_only.append((input_file_name, output_file_name))

            # expected file names with only output substitution
            #   (retaining original input file names)
            self.iofiles_a_only_output_only.append((test_file.name, output_file_name))
        self.iofiles_a_only = tuple(self.iofiles_a_only)
        self.iofiles_a_only_output_only = tuple(self.iofiles_a_only_output_only)
            
        test_file = open(os.path.join(self.directory, "b_file%d" % 7), "w")
        test_file.write("%d" % 7)
        self.files.append (test_file.name)
        test_file.close()
        
        # expected file names with extra "b" file
        self.iofiles_both_ab = list(self.iofiles_a_only)
        self.iofiles_both_ab.append([os.path.join(self.directory, "input_file_name_7"),
                                     os.path.join(self.directory, "output_file_name_7")])
        
        # expected file names with extra "b" file, only output substitution
        self.iofiles_both_ab_output_only = list(self.iofiles_a_only_output_only)
        self.iofiles_both_ab_output_only.append([os.path.join(self.directory, "b_file7"),
                                                 os.path.join(self.directory, "output_file_name_7")])
        
        
        
    def tearDown (self):
        """
        delete files
        """
        for f in self.files:
            os.unlink(f)
        os.removedirs(self.directory)        

        
    def glob_helper(self, match_file_spec, missing_input_file_spec = False, use_glob = True):
        
        if use_glob:
            if missing_input_file_spec:
                return task.glob_regex_io_param_factory (os.path.join(self.directory, "*"), 
                                                      r"(%s)(\d+)" % match_file_spec, 
                                                      r"output_file_name_\2")
            else:
                return task.glob_regex_io_param_factory (os.path.join(self.directory, "*"), 
                                                      r"(%s)(\d+)" % match_file_spec, 
                                                      r"input_file_name_\2",
                                                      r"output_file_name_\2")
        else:
            if missing_input_file_spec:
                return task.glob_regex_io_param_factory (self.files, 
                                                      r"(%s)(\d+)" % match_file_spec, 
                                                      r"output_file_name_\2")
            else:
                return task.glob_regex_io_param_factory (self.files, 
                                                      r"(%s)(\d+)" % match_file_spec, 
                                                      r"input_file_name_\2",
                                                      r"output_file_name_\2")


    def test_params(self):
        #---------------------------------------------------------------------------------
        #   test input_file_spec == "input_file_name_\2"
        #

        # test a files only
        params = self.glob_helper("a_file")
        print list(params())
        print self.iofiles_a_only
        self.assert_(list(params()) == self.iofiles_a_only)

        # test a and b files
        params = self.glob_helper("._file")
        self.assert_(list(params()) == self.iofiles_both_ab)
        
        # test no matching files
        params = self.glob_helper("c_file")
        self.assert_(list(params()) == list())
        
        
        #---------------------------------------------------------------------------------
        #   test input_file_spec == None 

        # test a files only
        params = self.glob_helper("a_file", True)
        self.assert_(list(params()) == self.iofiles_a_only_output_only)

        # test a and b files
        params = self.glob_helper("._file", True)
        self.assert_(list(params()) == self.iofiles_both_ab_output_only)

        # test no matching files
        params = self.glob_helper("c_file", True)
        self.assert_(list(params()) == list())
        
        
        #---------------------------------------------------------------------------------
        #   Same as above but using explicit list of files rather than glob
        #
        #   test input_file_spec == "input_file_name_\2"
        #

        # test a files only
        params = self.glob_helper("a_file", False, False)
        self.assert_(list(params()) == self.iofiles_a_only)

        # test a and b files
        params = self.glob_helper("._file", False, False)
        self.assert_(list(params()) == self.iofiles_both_ab)

        # test no matching files
        params = self.glob_helper("c_file", False, False)
        self.assert_(list(params()) == list())


        #---------------------------------------------------------------------------------
        #   Same as above but using explicit list of files rather than glob
        #
        #   test input_file_spec == None 

        # test a files only
        params = self.glob_helper("a_file", True, False)
        self.assert_(list(params()) == self.iofiles_a_only_output_only)

        # test a and b files
        params = self.glob_helper("._file", True, False)
        self.assert_(list(params()) == self.iofiles_both_ab_output_only)

        # test no matching files
        params = self.glob_helper("c_file", True, False)
        self.assert_(list(params()) == list())
        
                
                
        #print json.dumps(io_files, indent=4), json.dumps(self.iofiles_a_only, indent=4)

        
from itertools import izip
class Test_file_list_io_param_factory (unittest.TestCase):

    def generator_via_decorator__init(self, *decoratorArgs):
        """
            saves decorator arguments and forwards like the decorator.__init__ functions
        """
        param_generator_func = task.file_list_io_param_factory  (decoratorArgs)
        return param_generator_func

    def test_correct_file_list (self):
        #
        #   correct file parameters
        #
        param_singleton1 = ["input1", "output1", 1, 2]
        param_singleton2 = [None,     "output1", 1, 2]
        param_singleton3 = ["input1", None,      1, 2]
        param_list1      = [ 
                                ["input1", "output1", 1, 2],
                                [None,     "output2", 1, 2],
                                ["input3", None]           ,
                           ]
        param_list2      = [ 
                                ["input1", "output1", 1, 2],
                                [["input2a","input2b"], "output2", 1, 2],
                                [["input2a","input2b"], ["output2a", "output2b"], 1, 2],
                           ]
        working_params = [(param_singleton1, 1),
                          (param_singleton2, 1),
                          (param_singleton3, 1),
                          (param_list1     , 0),
                          (param_list2     , 0)]     
        
        working_results = [[param_singleton1],
                           [param_singleton2],
                           [param_singleton3],
                           param_list1,
                           param_list2]

        
        for (p, is_singleton), res in izip(working_params, working_results):
            if is_singleton:
                iterator = self.generator_via_decorator__init (*p)
            else:
                iterator = self.generator_via_decorator__init (p)
            coll = list(iterator())
            self.assert_(coll == res)


    def test_too_few_io_params (self):
        #
        #   incorrect file parameters
        #
        self.assertRaises(task.task_FilesArgumentsError, self.generator_via_decorator__init , [["input1"]])
        self.assertRaises(task.task_FilesArgumentsError, self.generator_via_decorator__init , [[None, None, 1, 2]])
        # missing brackets
        self.assertRaises(task.task_FilesArgumentsError, self.generator_via_decorator__init , [1, 2])
        self.assertRaises(task.task_FilesArgumentsError, self.generator_via_decorator__init , [["input1", "output2"], ["input2"]])
        self.assertRaises(task.task_FilesArgumentsError, self.generator_via_decorator__init , [["input1", "output2"],[None, None, 1, 2]])
        self.assertRaises(task.task_FilesArgumentsError, self.generator_via_decorator__init , [["input1", "output2"],[1, 2]])



                           
        
class Test_args_param_factory (unittest.TestCase):
    def generator_via_decorator__init(self, *decoratorArgs):
        """
            saves decorator arguments and forwards like the decorator.__init__ functions
        """
        param_generator_func = task.args_param_factory (decoratorArgs)
        return param_generator_func
        
    def test_params (self):
        
        #
        #   correct even after underlying value changes 
        #
        #param = [1, "b", "c"]
        #result = [(1), ('b'), ('c')]
        param_list       = [ 
                                ["input1", "output1", 1, 2],
                                [None,     "output2", 1, 2],
                                ["input3", None]           ,
                           ]
        import copy
        result = copy.deepcopy(param_list)

        param_generator = self.generator_via_decorator__init(param_list)
        self.assert_(list(param_generator()) == result)
        
        #
        #   works with function parameters not in list
        #
        parameters = [[ 1, "b", "c" ]]
        param_generator = self.generator_via_decorator__init(parameters)
        self.assert_(list(param_generator()) == parameters)
        
        
        #
        #   missing [] assert
        #         
                
        
                       
unittest.main()



