#!/usr/bin/env python
################################################################################
#
#   ruffus_utility
#
#
#   Copyright (c) 10/9/2009 Leo Goodstadt
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

********************************************
:mod:`ruffus_utility` -- Overview
********************************************


.. moduleauthor:: Leo Goodstadt <ruffus@llew.org.uk>

    Common utility functions


"""




#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   imports        


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
import os,copy
import re
import types
from ruffus_exceptions import *
import glob    


                                
                                
#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Functions        


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888





#_________________________________________________________________________________________

#   get_strings_in_nested_sequence

#_________________________________________________________________________________________
def is_str(arg):
    return issubclass(arg.__class__, str)

def non_str_sequence (arg):
    """
    Whether arg is a sequence.
    We treat a string however as a singleton not as a sequence
    """
    if issubclass(arg.__class__, str) or issubclass(arg.__class__, unicode):
        return False
    try:
        test = iter(arg)
        return True
    except TypeError:
        return False

def get_strings_in_nested_sequence(p, l = None):
    """
    Unravels arbitrarily nested sequence and returns lists of strings
    """
    if l == None:
        l = []
    if is_str(p):
        l.append(p)
    elif non_str_sequence (p):
        for pp in p:
            get_strings_in_nested_sequence(pp, l)
    return l



#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Encoders: turn objects and filenames into a more presentable format

#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
def ignore_unknown_encoder(obj):
    if non_str_sequence (obj):
        return "[%s]" % ", ".join(map(ignore_unknown_encoder, obj))
    try:
        s= str(obj)
        if "object at " in s and s[0] == '<' and s[-1] == '>':
            pos = s.find(" object at ")
            s = "<" + s[1:pos].replace("__main__.", "") + ">"
        return s.replace('"', "'")
    except:
        return "<%s>" % str(obj.__class__).replace('"', "'")

def shorten_filenames_encoder (obj):
    if non_str_sequence (obj):
        return "[%s]" % ", ".join(map(shorten_filenames_encoder, obj))
    if is_str(obj):
        if os.path.isabs(obj) and obj[1:].count('/') > 1:
            return os.path.split(obj)[1]
    return ignore_unknown_encoder(obj)



#
#_________________________________________________________________________________________
#
#   get_tasks_filename_globs_in_nested_sequence
#
#________________________________________________________________________________________ 
glob_letters = set('*[]?')
def is_glob(s):
    """Check whether 's' contains ANY of glob chars"""
    return len(glob_letters.intersection(s)) > 0

def get_tasks_filename_globs_in_nested_sequence(p, treat_strings_as_tasks = False, tasks=None, filenames=None, globs = None):
    """
    Divide parameters into task, filenames or globs
    """
    # 
    # create storage if this is not a recursive call
    # 
    if globs == None:
        tasks, filenames, globs = set(), set(), set()

    #
    #   task function
    # 
    if (type(p) == types.FunctionType):
        tasks.add(p)

    #
    #   output_from treats all arguments as tasks or task names
    # 
    elif isinstance(p, output_from):
        for pp in p.args:
            get_tasks_filename_globs_in_nested_sequence(pp, True,
                                                        tasks, filenames, globs)
    elif is_str(p):
        if treat_strings_as_tasks:
            tasks.add(p)
        elif is_glob(p):
            globs.add(p)
        else:
            filenames.add(p)

    elif non_str_sequence (p):
        for pp in p:
            get_tasks_filename_globs_in_nested_sequence(pp, treat_strings_as_tasks, 
                                                        tasks, filenames, globs)
    return tasks, filenames, globs
   

#
#
#_________________________________________________________________________________________
#
#   get_tasks_filename_globs_in_nested_sequence
#
#________________________________________________________________________________________ 
def expand_filename_globs_in_nested_sequence(p):
    """
    Divide parameters into task, filenames or globs
    """
    if is_str(p):
        if is_glob(p):
            return glob.glob(p)
        else:
            return p
    elif non_str_sequence (p):
        return tuple(expand_filename_globs_in_nested_sequence(pp) for pp in p)
    else:
        return p


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   special markers used by @files_re

#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
class combine(object):
    def __init__ (self, *args):
        self.args = args

class output_from(object):
    def __init__ (self, *args):
        self.args = args
    
    
#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Testing


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

if __name__ == '__main__':
    import sys
    
    # use simplejson in place of json for python < 2.6
    try:                            # DEBUGG
        import json                 # DEBUGG
    except ImportError:             # DEBUGG
        import simplejson           # DEBUGG
        json = simplejson           # DEBUGG
                                    # DEBUGG
                                    # DEBUGG
    dumps = json.dumps              # DEBUGG

    exe_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
    #_________________________________________________________________________________________
    
    #   file_list_io_param_factory
     
    #_________________________________________________________________________________________
    import unittest, time
    class Test_utility_functions(unittest.TestCase):
    
        #       self.assertEqual(self.seq, range(10))
        #       self.assert_(element in self.seq)
        #       self.assertRaises(ValueError, random.sample, self.seq, 20)
    
        def check_equal (self, a,b):
            self.assertEqual(get_tasks_filename_globs_in_nested_sequence(a), b)
            
        def test_expand_filename_globs_in_nested_sequence (self):
            print expand_filename_globs_in_nested_sequence(["test1", ["test2", set([1,2]), (set(["python_modules/*.py"]))]])
            
        def test_get_tasks_filename_globs_in_nested_sequence(self):
            # 
            # test strings
            # 
            self.check_equal("test", (set(), set(['test']), set()))
            self.check_equal([("test1",), "test2", 3], (set(), set(['test1', 'test2']), set()))
            
            #
            # test missing
            # 
            self.check_equal((1,3, [5]), (set(), set(), set()))
            self.check_equal(None, (set(), set(), set()))

            #
            # test glob
            # 
            self.check_equal([("test1.*",), "test?2", 3], (set(), set(), set(['test1.*', 'test?2'])))

            #
            # test glob and string
            # 
            self.check_equal([("test*1",), (("test3",),),"test2", 3], (set(), set(['test3', 'test2']), set(['test*1'])))
            
            #
            # test function
            # 
            self.check_equal(is_glob, (set([is_glob]), set(), set([])))
            self.check_equal([is_glob, [1, "this", ["that*", 5]], [(is_str,)]], (
                            set([is_glob, is_str]), set(["this"]), set(["that*"])))
            #
            # test wrapper
            # 
            self.check_equal(output_from(is_glob, ["what", 7], 5), (set([is_glob, "what"]), set(), set([])))

    #
    #   debug parameter ignored if called as a module
    #     
    if sys.argv.count("--debug"):
        sys.argv.remove("--debug")
    unittest.main()


        
