################################################################################
#
#
#   combinatorics.py
#
#   Copyright (c) 2013 Leo Goodstadt
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
:mod:`ruffus.combinatorics` -- Overview
********************************************

.. moduleauthor:: Leo Goodstadt <ruffus@llew.org.uk>


    #
    #   @product
    #
    from ruffus import *

    @product(
        "/a_directory/dataset1.*.bam",
        formatter( ".*/dataset1\.(?P<ID>\d+).bam" ),
        "/a_different/directory/dataset2.*.bam",
        formatter(".species", ".*/dataset2\.(?P<ID>\d+).bam" ),
        "{path[0][0]}/{base_name[0][0]}.{base_name[0][0]}.out",
        "{path[0][0]}",       # extra: path for 1st input, 1st file
        "{path[1][0]}",       # extra: path for 2nd input, 1st file
        "{basename[0][1]}",   # extra: file name for 1st input, 2nd file
        "{ID[1][1]}",         # extra: regular expression named capture group for 2nd input, 2nd file
        )
    def task1( infiles, outfile,
                input_1__path,
                input_2__path,
                input_1__2nd_file_name,
                input_2__3rd_file_match
                ):
        print infiles
        print outfile
        print input_1__path
        print input_2__path
        print input_1__2nd_file_name
        print input_2__3rd_file_match
"""

from .task import task_decorator


#
#   Combinatoric generators:
#
class product(task_decorator):
    pass


class permutations(task_decorator):
    pass


class combinations(task_decorator):
    pass


class combinations_with_replacement(task_decorator):
    pass
