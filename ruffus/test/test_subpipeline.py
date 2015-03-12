#!/usr/bin/env python
from __future__ import print_function
"""

    test_transform_with_no_re_matches.py

        test messages with no regular expression matches

"""

import os
import sys

# add grandparent to search path for testing
grandparent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, grandparent_dir)

# module name = script name without extension
module_name = os.path.splitext(os.path.basename(__file__))[0]


# funky code to import by file name
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ruffus_name = os.path.basename(parent_dir)
ruffus = __import__ (ruffus_name)

for attr in "follows", "transform", "merge", "add_inputs", "inputs", "suffix", "mkdir", "regex", "pipeline_run", "Pipeline":
    globals()[attr] = getattr (ruffus, attr)





print("\tRuffus Version = ", ruffus.__version__)


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   imports


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
import shutil


def touch (outfile):
    with open(outfile, "w"):
        pass


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Tasks


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
tempdir = "tempdir/"
def task_originate(o):
    touch(o)



def task3_add_inputs(i, o):
    names = ",".join(sorted(i))
    with open(o, "w") as oo:
        oo.write(names)

def task_merge(i, o):
    with open(o, "w") as o_file:
        for f in sorted(i):
            with open(f) as ii:
                o_file.write(f +":" + ii.read() + "; ")

def task_forward(i, o):
    with open(o, "w") as o_file:
        with open(i) as ii:
            o_file.write(i +":" + ii.read())










import unittest

class Test_task(unittest.TestCase):

    def tearDown (self):
        """
        """
        try:
            shutil.rmtree(tempdir)
        except:
            pass


    def make_pipeline1(self, pipeline_name, starting_file_names, do_not_define_tail_task = False):
        test_pipeline = Pipeline(pipeline_name)

        test_pipeline.originate(task_originate, starting_file_names)\
            .follows(mkdir(tempdir), mkdir(tempdir + "testdir", tempdir + "testdir2"))
        test_pipeline.transform(task_func   = task3_add_inputs,
                                input       = task_originate,
                                filter      = regex(r"(.*)"),
                                add_inputs  = add_inputs("test_transform_inputs.*y"),
                                output      = r"\1.22")
        test_pipeline.transform(task_func   = task_forward,
                                name        = "22_to_33",
                                input       = task3_add_inputs,
                                filter      = suffix(".22"),
                                output      = ".33")
        test_pipeline.transform(task_func   = task_forward,
                                name        = "33_to_44",
                                input       = test_pipeline["22_to_33"],
                                filter      = suffix(".33"),
                                output      = ".44")
        if not do_not_define_tail_task:
            test_pipeline.set_tail_tasks(test_pipeline["33_to_44"])
        test_pipeline.set_head_tasks(test_pipeline[task_originate])

        return test_pipeline

    def make_pipeline2(self, pipeline_name = "pipeline2", do_not_define_head_task = False):
        test_pipeline2 = Pipeline(pipeline_name)
        test_pipeline2.transform(task_func   = task_forward,
                                name        = "44_to_55",
                                 # placeholder
                                input       = None,
                                filter      = suffix(".44"),
                                output      = ".55")
        test_pipeline2.merge(   task_func   = task_merge,
                                input       = test_pipeline2["44_to_55"],
                                output      = tempdir + "final.output")
        test_pipeline2.set_tail_tasks(test_pipeline2[task_merge])
        if not do_not_define_head_task:
            test_pipeline2.set_head_tasks(test_pipeline2["44_to_55"])

        return test_pipeline2


    def test_subpipelines (self):

        # first two pipelines
        test_pipeline1a = self.make_pipeline1(pipeline_name = "pipeline1a", starting_file_names = [tempdir + ss for ss in ("a.1", "b.1")])
        test_pipeline1b = self.make_pipeline1(pipeline_name = "pipeline1b", starting_file_names = [tempdir + ss for ss in ("c.1", "d.1")])
        # third pipeline is a clone of pipeline1b
        test_pipeline1c = test_pipeline1b.clone(new_name = "pipeline1c")
        test_pipeline1c.set_output(output = [])
        test_pipeline1c.set_output(output = [tempdir + ss for ss in ("e.1", "f.1")])

        # join all three to pipeline2
        test_pipeline2 = self.make_pipeline2()
        test_pipeline2.set_input(input = [test_pipeline1a, test_pipeline1b, test_pipeline1c])


        #test_pipeline2.printout_graph("test.svg", "svg", [task_merge])
        #test_pipeline2.printout_graph("test.dot", "dot", [task_merge])
        test_pipeline2.printout(verbose = 0)
        test_pipeline2.run(multiprocess = 10, verbose = 0)

        correct_output = 'tempdir/a.1.55:tempdir/a.1.44:tempdir/a.1.33:tempdir/a.1.22:tempdir/a.1,test_transform_inputs.py; tempdir/b.1.55:tempdir/b.1.44:tempdir/b.1.33:tempdir/b.1.22:tempdir/b.1,test_transform_inputs.py; tempdir/c.1.55:tempdir/c.1.44:tempdir/c.1.33:tempdir/c.1.22:tempdir/c.1,test_transform_inputs.py; tempdir/d.1.55:tempdir/d.1.44:tempdir/d.1.33:tempdir/d.1.22:tempdir/d.1,test_transform_inputs.py; tempdir/e.1.55:tempdir/e.1.44:tempdir/e.1.33:tempdir/e.1.22:tempdir/e.1,test_transform_inputs.py; tempdir/f.1.55:tempdir/f.1.44:tempdir/f.1.33:tempdir/f.1.22:tempdir/f.1,test_transform_inputs.py; '

        with open(tempdir + "final.output") as real_output:
            real_output_str = real_output.read()
        self.assertEqual(correct_output, real_output_str)



if __name__ == '__main__':
    unittest.main()

