#!/usr/bin/env python
from __future__ import print_function
import unittest
import shutil
from ruffus import add_inputs, suffix, mkdir, regex, Pipeline, output_from, touch_file
import ruffus
import sys

"""


        Demonstrates the new Ruffus syntax in version 2.6
"""

import os
tempdir = os.path.relpath(os.path.abspath(os.path.splitext(__file__)[0]))

# add grandparent to search path for testing
grandparent_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, grandparent_dir)


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   imports


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888


def touch(outfile):
    with open(outfile, "w"):
        pass


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Tasks


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
def task_originate(o):
    """
    Makes new files
    """
    touch(o)


def task_m_to_1(i, o):
    """
    Merges files together
    """
    with open(o, "w") as o_file:
        for f in sorted(i):
            with open(f) as ii:
                o_file.write(f + "=" + ii.read() + "; ")


def task_1_to_1(i, o):
    """
    1 to 1 for transform
    """
    with open(o, "w") as o_file:
        with open(i) as ii:
            o_file.write(i + "+" + ii.read())


DEBUG_do_not_define_tail_task = False
DEBUG_do_not_define_head_task = False


#
#   Returns a fully formed sub pipeline useable as a building block
#

def make_pipeline1(pipeline_name,   # Pipelines need to have a unique name
                   starting_file_names):
    test_pipeline = Pipeline(pipeline_name)

    #   We can change the starting files later using
    #          set_input() for transform etc.
    #       or set_output() for originate
    #   But it can be more convenient to just pass this to the function making the pipeline
    #
    test_pipeline.originate(task_originate, starting_file_names)\
        .follows(mkdir(tempdir), mkdir(tempdir + "/testdir", tempdir + "/testdir2"))\
        .posttask(touch_file(tempdir + "/testdir/whatever.txt"))
    test_pipeline.transform(task_func=task_m_to_1,
                            name="add_input",
                            # Lookup Task from function name task_originate()
                            #   So long as this is unique in the pipeline
                            input=task_originate,
                            filter=regex(r"(.+)"),
                            add_inputs=add_inputs(
                                tempdir + "/testdir/whatever.txt"),
                            output=r"\1.22")
    test_pipeline.transform(task_func=task_1_to_1,
                            name="22_to_33",
                            # Lookup Task from Task name
                            #   Function name is not unique in the pipeline
                            input=output_from("add_input"),
                            filter=suffix(".22"),
                            output=".33")
    tail_task = test_pipeline.transform(task_func=task_1_to_1,
                                        name="33_to_44",
                                        # Ask Pipeline to lookup Task from Task name
                                        input=test_pipeline["22_to_33"],
                                        filter=suffix(".33"),
                                        output=".44")

    #   Set the tail task so that users of my sub pipeline can use it as a dependency
    #       without knowing the details of task names
    #
    #   Use Task() object directly without having to lookup
    test_pipeline.set_tail_tasks([tail_task])

    #   If we try to connect a Pipeline without tail tasks defined, we have to
    #       specify the exact task within the Pipeline.
    #   Otherwise Ruffus will not know which task we mean and throw an exception
    if DEBUG_do_not_define_tail_task:
        test_pipeline.set_tail_tasks([])

    # Set the head task so that users of my sub pipeline send input into it
    #   without knowing the details of task names
    test_pipeline.set_head_tasks([test_pipeline[task_originate]])

    return test_pipeline

#
#   Returns a fully formed sub pipeline useable as a building block
#


def make_pipeline2(pipeline_name="pipeline2"):
    test_pipeline2 = Pipeline(pipeline_name)
    test_pipeline2.transform(task_func=task_1_to_1,
                             # task name
                             name="44_to_55",
                             # placeholder: will be replaced later with set_input()
                             input=None,
                             filter=suffix(".44"),
                             output=".55")
    test_pipeline2.merge(task_func=task_m_to_1,
                         input=test_pipeline2["44_to_55"],
                         output=tempdir + "/final.output",)

    # Set head and tail
    test_pipeline2.set_tail_tasks([test_pipeline2[task_m_to_1]])
    if not DEBUG_do_not_define_head_task:
        test_pipeline2.set_head_tasks([test_pipeline2["44_to_55"]])

    return test_pipeline2


def run_pipeline():

    #   First two pipelines are created as separate instances by the make_pipeline1 function
    pipeline1a = make_pipeline1(pipeline_name="pipeline1a", starting_file_names=[
                                tempdir + "/" + ss for ss in ("a.1", "b.1")])
    pipeline1b = make_pipeline1(pipeline_name="pipeline1b", starting_file_names=[
                                tempdir + "/" + ss for ss in ("c.1", "d.1")])

    #   The Third pipeline is a clone of pipeline1b
    pipeline1c = pipeline1b.clone(new_name="pipeline1c")

    #   Set the "originate" files for pipeline1c to ("e.1" and "f.1")
    #       Otherwise they would use the original ("c.1", "d.1")
    pipeline1c.set_output(output=[])
    pipeline1c.set_output(output=[tempdir + "/" + ss for ss in ("e.1", "f.1")])

    #   Join all pipeline1a-c to pipeline2
    pipeline2 = make_pipeline2()
    pipeline2.set_input(input=[pipeline1a, pipeline1b, pipeline1c])

    #pipeline2.printout_graph("test.svg", "svg", [task_m_to_1])
    #pipeline2.printout(verbose = 0)
    pipeline2.run(multiprocess=10, verbose=0)


class Test_task(unittest.TestCase):

    def tearDown(self):
        """
        """
        try:
            shutil.rmtree(tempdir)
        except:
            pass

    def test_subpipelines(self):

        run_pipeline()

        # Check that the output reflecting the pipeline topology is correct.
        correct_output = '{tempdir}/a.1.55={tempdir}/a.1.44+{tempdir}/a.1.33+{tempdir}/a.1.22+{tempdir}/a.1=; {tempdir}/testdir/whatever.txt=; ; ' \
                         '{tempdir}/b.1.55={tempdir}/b.1.44+{tempdir}/b.1.33+{tempdir}/b.1.22+{tempdir}/b.1=; {tempdir}/testdir/whatever.txt=; ; ' \
                         '{tempdir}/c.1.55={tempdir}/c.1.44+{tempdir}/c.1.33+{tempdir}/c.1.22+{tempdir}/c.1=; {tempdir}/testdir/whatever.txt=; ; ' \
                         '{tempdir}/d.1.55={tempdir}/d.1.44+{tempdir}/d.1.33+{tempdir}/d.1.22+{tempdir}/d.1=; {tempdir}/testdir/whatever.txt=; ; ' \
                         '{tempdir}/e.1.55={tempdir}/e.1.44+{tempdir}/e.1.33+{tempdir}/e.1.22+{tempdir}/e.1=; {tempdir}/testdir/whatever.txt=; ; ' \
                         '{tempdir}/f.1.55={tempdir}/f.1.44+{tempdir}/f.1.33+{tempdir}/f.1.22+{tempdir}/f.1=; {tempdir}/testdir/whatever.txt=; ; '.format(
                             tempdir=tempdir)
        with open(tempdir + "/final.output") as real_output:
            real_output_str = real_output.read()
        self.assertEqual(correct_output, real_output_str)


if __name__ == '__main__':
    unittest.main()
