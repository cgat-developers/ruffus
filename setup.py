#!/usr/bin/env python
import sys
import os
from setuptools import setup

if not sys.version_info[0:2] >= (2, 6):
    sys.stderr.write("Requires Python later than 2.6\n")
    sys.exit(1)

# quickly import the latest version of ruffus
sys.path.insert(0, os.path.abspath("."))
import ruffus.ruffus_version
sys.path.pop(0)

module_dependencies = []
#module_dependencies = ['multiprocessing>=2.6', 'simplejson']


setup(
        name='ruffus',
        version=ruffus.ruffus_version.__version, #major.minor[.patch[.sub]]
        description='Light-weight Python Computational Pipeline Management',
        maintainer="Leo Goodstadt",
        maintainer_email="ruffus_lib@llew.org.uk",
        author='Leo Goodstadt',
        author_email='ruffus@llew.org.uk',
        long_description=\
"""
***************************************
Overview
***************************************


    The Ruffus module is a lightweight way to add support
    for running computational pipelines.

    Computational pipelines are often conceptually quite simple, especially
    if we breakdown the process into simple stages, or separate **tasks**.

    Each stage or **task** in a computational pipeline is represented by a python function
    Each python function can be called in parallel to run multiple **jobs**.

    Ruffus was originally designed for use in bioinformatics to analyse multiple genome
    data sets.

***************************************
Documentation
***************************************

    Ruffus documentation can be found `here <http://www.ruffus.org.uk>`__ ,
    with `download notes <http://www.ruffus.org.uk/installation.html>`__ ,
    a `tutorial <http://www.ruffus.org.uk/tutorials/new_tutorial/introduction.html>`__ and
    an `in-depth manual <http://www.ruffus.org.uk/tutorials/new_tutorial/manual_contents.html>`__ .


***************************************
Background
***************************************

    The purpose of a pipeline is to determine automatically which parts of a multi-stage
    process needs to be run and in what order in order to reach an objective ("targets")

    Computational pipelines, especially for analysing large scientific datasets are
    in widespread use.
    However, even a conceptually simple series of steps can be difficult to set up and
    maintain.

***************************************
Design
***************************************
    The ruffus module has the following design goals:

        * Lightweight
        * Scalable / Flexible / Powerful
        * Standard Python
        * Unintrusive
        * As simple as possible

***************************************
Features
***************************************

    Automatic support for

        * Managing dependencies
        * Parallel jobs, including dispatching work to computational clusters
        * Re-starting from arbitrary points, especially after errors (checkpointing)
        * Display of the pipeline as a flowchart
        * Managing complex pipeline topologies


***************************************
A Simple example
***************************************

        Use the **@follows(...)** python decorator before the function definitions::

            from ruffus import *
            import sys

            def first_task():
                print "First task"

            @follows(first_task)
            def second_task():
                print "Second task"

            @follows(second_task)
            def final_task():
                print "Final task"




        the ``@follows`` decorator indicate that the ``first_task`` function precedes ``second_task`` in
        the pipeline.

        The canonical Ruffus decorator is ``@transform`` which **transforms** data flowing down a
        computational pipeline from one stage to teh next.

********
Usage
********

    Each stage or **task** in a computational pipeline is represented by a python function
    Each python function can be called in parallel to run multiple **jobs**.

    1. Import module::

            import ruffus


    1. Annotate functions with python decorators

    2. Print dependency graph if you necessary

        - For a graphical flowchart in ``jpg``, ``svg``, ``dot``, ``png``, ``ps``, ``gif`` formats::

            pipeline_printout_graph ("flowchart.svg")

        This requires ``dot`` to be installed

        - For a text printout of all jobs ::

            pipeline_printout(sys.stdout)


    3. Run the pipeline::

        pipeline_run()


""",
        url='http://www.ruffus.org.uk',
        download_url = "https://pypi.python.org/pypi/ruffus",

        install_requires = module_dependencies, #['multiprocessing>=1.0', 'json' ], #, 'python>=2.5'],
        setup_requires   = module_dependencies, #['multiprocessing>=1.0', 'json'],    #, 'python>=2.5'],


        classifiers=[
                    'Intended Audience :: End Users/Desktop',
                    'Development Status :: 5 - Production/Stable',
                    'Intended Audience :: Developers',
                    'Intended Audience :: Science/Research',
                    'Intended Audience :: Information Technology',
                    'License :: OSI Approved :: MIT License',
                    'Programming Language :: Python',
                    'Topic :: Scientific/Engineering',
                    'Topic :: Scientific/Engineering :: Bio-Informatics',
                    'Topic :: System :: Distributed Computing',
                    'Topic :: Software Development :: Build Tools',
                    'Topic :: Software Development :: Build Tools',
                    'Topic :: Software Development :: Libraries',
                    'Environment :: Console',
                    ],
        license = "MIT",
        keywords = "make task pipeline parallel bioinformatics science",


        #packages = find_packages('src'),    # include all packages under src
        #package_dir = {'':'src'},           #packages are under src
        packages=['ruffus'],
        package_dir={'ruffus': 'ruffus'},
        include_package_data = True,    # include everything in source control
        #package_data = {
        #    # If any package contains *.txt files, include them:
        #    '': ['*.TXT'],                                \
        #}


     )

#
#  http://pypi.python.org/pypi
#  http://docs.python.org/distutils/packageindex.html
#
#
#
# python setup.py register
# python setup.py sdist --format=gztar upload
