.. include:: ../../global.inc
.. include:: manual_chapter_numbers.inc

.. _new_manual.mkdir.code:

############################################################################################################################################################################################################
|new_manual.mkdir.chapter_num|: Python Code for Preparing directories for output with :ref:`@mkdir() <decorators.mkdir>`
############################################################################################################################################################################################################

.. seealso::

    * :ref:`Manual Table of Contents <new_manual.table_of_contents>`
    * :ref:`mkdir() <decorators.mkdir>` syntax
    * :ref:`formatter() <decorators.formatter>` syntax
    * :ref:`regex() <decorators.regex>` syntax
    * Back to |new_manual.mkdir.chapter_num|: :ref:`Preparing directories for output with @mkdir() <new_manual.mkdir>`

****************************************************************************************************************
Code for :ref:`formatter() <decorators.formatter>` Zoo example
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


        # create directories for each clade
        @mkdir(    create_initial_files,                                       # Input

                   formatter(".+/(?P<clade>\w+).(?P<tame>\w+).animals"),       # Only animals: ignore plants!

                   "{subpath[0][1]}/{clade[0]}")                               # new_directory
        #   Put different animals in different directories depending on their clade
        @transform(create_initial_files,                                       # Input

                   formatter(".+/(?P<clade>\w+).(?P<tame>\w+).animals"),       # Only animals: ignore plants!

                   "{subpath[0][1]}/{clade[0]}/{tame[0]}.{subdir[0][0]}.food", # Replacement

                   "{subpath[0][1]}/{clade[0]}",                               # new_directory
                   "{subdir[0][0]}",                                           # animal_name
                   "{tame[0]}")                                                # tameness
        def feed(input_file, output_file, new_directory, animal_name, tameness):
                print "%40s -> %90s" % (input_file, output_file)
                # this works now
                open(output_file, "w")


        pipeline_run(verbose=0)


****************************************************************************************************************
Code for :ref:`regex() <decorators.regex>` Zoo example
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


        # create directories for each clade
        @mkdir(    create_initial_files,                                        # Input
                   regex(r"(.*?/?)(\w+)/(?P<clade>\w+).(?P<tame>\w+).animals"), # Only animals: ignore plants!
                   r"\g<clade>")                                                # new_directory
        #   Put different animals in different directories depending on their clade
        @transform(create_initial_files,                                        # Input
                   regex(r"(.*?/?)(\w+)/(?P<clade>\w+).(?P<tame>\w+).animals"), # Only animals: ignore plants!
                   r"\1\g<clade>/\g<tame>.\2.food",                             # Replacement
                   r"\1\g<clade>",                                              # new_directory
                   r"\2",                                                       # animal_name
                   "\g<tame>")                                                  # tameness
        def feed(input_file, output_file, new_directory, animal_name, tameness):
            print "%40s -> %90s" % (input_file, output_file)
            # this works now
            open(output_file, "w")


        pipeline_run(verbose=0)

