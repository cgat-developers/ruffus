#!/usr/bin/env python
from __future__ import print_function
"""

    test_softlink_uptodate.py

        use :
            --debug               to test automatically
            -j N / --jobs N       to specify multitasking
            -v                    to see the jobs in action
            -n / --just_print     to see what jobs would run

"""


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   options


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
import sys, os

# add self to search path for testing
exe_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
sys.path.insert(0,os.path.abspath(os.path.join(exe_path,"..", "..")))



from ruffus import *

#parser = cmdline.get_argparse(   description='Test soft link up to date?', version = "%(prog)s v.2.23")
#options = parser.parse_args()

#  optional logger which can be passed to ruffus tasks
#logger, logger_mutex = cmdline.setup_logging (__name__, options.log_file, options.verbose)

#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Tasks


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Tasks


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#
#   First task
#
@originate(["a.1", "b.1"])
def start_task(output_file_name):
    with open(output_file_name,  "w") as f:
        pass

#
#   Forwards file names, is always as up to date as its input files...
#
@transform(start_task, suffix(".1"), ".1")
def same_file_name_task(input_file_name, output_file_name):
    pass

#
#   Links file names, is always as up to date if links are not missing
#
@transform(start_task, suffix(".1"), ".linked.1")
def linked_file_name_task(input_file_name, output_file_name):
    os.symlink(input_file_name, output_file_name)


#
#   Final task linking everything
#
@transform([linked_file_name_task, same_file_name_task], suffix(".1"), ".3")
def final_task (input_file_name, output_file_name):
    with open(output_file_name,  "w") as f:
        pass

#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Run pipeline


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888


import unittest, shutil
try:
    from StringIO import StringIO
except:
    from io import StringIO

class Test_ruffus(unittest.TestCase):
    def setUp(self):
        for f in ["a.1", "b.1", "a.linked.1", "b.linked.1", "a.3", "b.3", "a.linked.3", "b.linked.3"]:
            try:
                os.unlink(f)
            except:
                pass

    def tearDown(self):
        for f in ["a.1", "b.1", "a.linked.1", "b.linked.1", "a.3", "b.3", "a.linked.3", "b.linked.3"]:
            if os.path.lexists(f):
                os.unlink(f)
            else:
                raise Exception("Expected %s missing" % f)

    def test_ruffus (self):
        pipeline_run(log_exceptions = True, verbose = 0)

    def test_newstyle_ruffus (self):
        test_pipeline = Pipeline("test")
        test_pipeline.originate(start_task, ["a.1", "b.1"])
        test_pipeline.transform(same_file_name_task, start_task, suffix(".1"), ".1")
        test_pipeline.transform(linked_file_name_task, start_task, suffix(".1"), ".linked.1")
        test_pipeline.transform(final_task, [linked_file_name_task, same_file_name_task], suffix(".1"), ".3")
        test_pipeline.run(log_exceptions = True, verbose = 0)



if __name__ == '__main__':
    unittest.main()


