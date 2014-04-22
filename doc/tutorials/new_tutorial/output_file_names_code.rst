.. include:: ../../global.inc
.. include:: manual_chapter_numbers.inc

.. _new_manual.output_file_names.code:

############################################################################################################################################################################################################
|new_manual.output_file_names.chapter_num|: Python Code for Specifying output file names with :ref:`formatter() <decorators.formatter>` and :ref:`regex() <decorators.regex>`
############################################################################################################################################################################################################

.. seealso::

    * :ref:`Manual Table of Contents <new_manual.table_of_contents>`
    * :ref:`suffix() <decorators.suffix>` syntax
    * :ref:`formatter() <decorators.formatter>` syntax
    * :ref:`regex() <decorators.regex>` syntax
    * Back to |new_manual.output_file_names.chapter_num|: :ref:`Specifying output file names <new_manual.output_file_names>`

************************************************************************
Example Code for :ref:`suffix() <decorators.suffix>`
************************************************************************
    .. code-block:: python

        from ruffus import *

        #---------------------------------------------------------------
        #   create initial files
        #
        @originate([   ['job1.a.start', 'job1.b.start'],
                       ['job2.a.start', 'job2.b.start'],
                       ['job3.a.start', 'job3.b.start']    ])
        def create_initial_file_pairs(output_files):
            # create both files as necessary
            for output_file in output_files:
                with open(output_file, "w") as oo: pass

        #---------------------------------------------------------------
        #
        #   suffix
        #
        @transform(create_initial_file_pairs,             # name of previous task(s) (or list of files, or a glob)
                    suffix(".start"),                     # matching suffix of the "input file"
                    [".output.a.1", 45, ".output.b.1"])   # resulting suffix
        def first_task(input_files, output_parameters):
            print "  input_parameters  = ", input_files
            print "  output_parameters = ", output_parameters


        #
        #       Run
        #
        pipeline_run([first_task])



************************************************************************
Example Code for :ref:`formatter() <decorators.formatter>`
************************************************************************

    .. code-block:: python

        from ruffus import *

        #   create initial files
        @originate([   ['job1.a.start', 'job1.b.start'],
                       ['job2.a.start', 'job2.b.start'],
                       ['job3.a.start', 'job3.c.start']    ])
        def create_initial_file_pairs(output_files):
            # create both files as necessary
            for output_file in output_files:
                with open(output_file, "w") as oo: pass


        #---------------------------------------------------------------
        #
        #   formatter
        #

        #   first task
        @transform(create_initial_file_pairs,                               # Input

                    formatter(".+/job(?P<JOBNUMBER>\d+).a.start",           # Extract job number
                              ".+/job[123].b.start"),                       # Match only "b" files

                    ["{path[0]}/jobs{JOBNUMBER[0]}.output.a.1",             # Replacement list
                     "{path[1]}/jobs{JOBNUMBER[0]}.output.b.1", 45])
        def first_task(input_files, output_parameters):
            print "input_parameters = ", input_files
            print "output_parameters = ", output_parameters


        #
        #       Run
        #
        pipeline_run(verbose=0)


****************************************************************************************************************
Example Code for :ref:`formatter() <decorators.formatter>` with replacements in *extra* arguments
****************************************************************************************************************


    .. code-block:: python

        from ruffus import *

        #   create initial files
        @originate([   ['job1.a.start', 'job1.b.start'],
                       ['job2.a.start', 'job2.b.start'],
                       ['job3.a.start', 'job3.c.start']    ])
        def create_initial_file_pairs(output_files):
            for output_file in output_files:
                with open(output_file, "w") as oo: pass


        #---------------------------------------------------------------
        #
        #   print job number as an extra argument
        #

        #   first task
        @transform(create_initial_file_pairs,                               # Input

                    formatter(".+/job(?P<JOBNUMBER>\d+).a.start",           # Extract job number
                              ".+/job[123].b.start"),                       # Match only "b" files

                    ["{path[0]}/jobs{JOBNUMBER[0]}.output.a.1",             # Replacement list
                     "{path[1]}/jobs{JOBNUMBER[0]}.output.b.1"],

                     "{JOBNUMBER[0]}"
        def first_task(input_files, output_parameters, job_number):
            print job_number, ":", input_files


        pipeline_run(verbose=0)


****************************************************************************************************************
Example Code for :ref:`formatter() <decorators.formatter>` in Zoos
****************************************************************************************************************


    .. code-block:: python

        from ruffus import *

        #   Make directories
        @mkdir(["tiger", "lion", "dog", "crocodile", "rose"])

        @originate(
                    #   List of animals and plants
                    [    "tiger/mammals.wild.animals",
                        "lion/mammals.wild.animals",
                        "lion/mammals.handreared.animals",
                        "dog/mammals.tame.animals",
                        "dog/mammals.wild.animals",
                        "crocodile/reptiles.wild.animals",
                        "rose/flowering.handreared.plants"])
        def create_initial_files(output_file):
            with open(output_file, "w") as oo: pass


        #   Put different animals in different directories depending on their clade
        @transform(create_initial_files,                                       # Input

                   formatter(".+/(?P<clade>\w+).(?P<tame>\w+).animals"),       # Only animals: ignore plants!

                   "{subpath[0][1]}/{clade[0]}/{tame[0]}.{subdir[0][0]}.food", # Replacement

                   "{subpath[0][1]}/{clade[0]}",                               # new_directory
                   "{subdir[0][0]}",                                           # animal_name
                   "{tame[0]}")                                                # tameness
        def feed(input_file, output_file, new_directory, animal_name, tameness):
            print "Food for the {tameness:11s} {animal_name:9s} = {output_file:90s} will be placed in {new_directory}".format(**locals())


        pipeline_run(verbose=0)


        Results in:

        ::

            >>> pipeline_run(verbose=0)
            Food for the wild        crocodile = ./reptiles/wild.crocodile.food will be placed in ./reptiles
            Food for the tame        dog       = ./mammals/tame.dog.food        will be placed in ./mammals
            Food for the wild        dog       = ./mammals/wild.dog.food        will be placed in ./mammals
            Food for the handreared  lion      = ./mammals/handreared.lion.food will be placed in ./mammals
            Food for the wild        lion      = ./mammals/wild.lion.food       will be placed in ./mammals
            Food for the wild        tiger     = ./mammals/wild.tiger.food      will be placed in ./mammals



****************************************************************************************************************
Example Code for :ref:`regex() <decorators.regex>` in zoos
****************************************************************************************************************


    .. code-block:: python

        from ruffus import *

        #   Make directories
        @mkdir(["tiger", "lion", "dog", "crocodile", "rose"])

        @originate(
                    #   List of animals and plants
                    [    "tiger/mammals.wild.animals",
                        "lion/mammals.wild.animals",
                        "lion/mammals.handreared.animals",
                        "dog/mammals.tame.animals",
                        "dog/mammals.wild.animals",
                        "crocodile/reptiles.wild.animals",
                        "rose/flowering.handreared.plants"])
        def create_initial_files(output_file):
            with open(output_file, "w") as oo: pass



        #   Put different animals in different directories depending on their clade
        @transform(create_initial_files,                                        # Input

                   regex(r"(.*?/?)(\w+)/(?P<clade>\w+).(?P<tame>\w+).animals"), # Only animals: ignore plants!

                   r"\1/\g<clade>/\g<tame>.\2.food",                            # Replacement

                   r"\1/\g<clade>",                                             # new_directory
                   r"\2",                                                       # animal_name
                   "\g<tame>")                                                  # tameness
        def feed(input_file, output_file, new_directory, animal_name, tameness):
            print "Food for the {tameness:11s} {animal_name:9s} = {output_file:90s} will be placed in {new_directory}".format(**locals())


        pipeline_run(verbose=0)


        Results in:

        ::

            >>> pipeline_run(verbose=0)
            Food for the wild        crocodile = reptiles/wild.crocodile.food will be placed in reptiles
            Food for the tame        dog       = mammals/tame.dog.food        will be placed in mammals
            Food for the wild        dog       = mammals/wild.dog.food        will be placed in mammals
            Food for the handreared  lion      = mammals/handreared.lion.food will be placed in mammals
            Food for the wild        lion      = mammals/wild.lion.food       will be placed in mammals
            Food for the wild        tiger     = mammals/wild.tiger.food      will be placed in mammals


