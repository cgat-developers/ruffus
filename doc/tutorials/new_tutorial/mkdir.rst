.. include:: ../../global.inc
.. include:: manual_chapter_numbers.inc

.. index::
    pair: mkdir; Tutorial

.. _new_manual.mkdir:

######################################################################################################################################################################
|new_manual.mkdir.chapter_num|: Preparing directories for output with :ref:`@mkdir() <decorators.mkdir>`
######################################################################################################################################################################

.. seealso::

   * :ref:`Manual Table of Contents <new_manual.table_of_contents>`
   * :ref:`@follows(mkdir()) syntax in detail <decorators.follows>`
   * :ref:`@mkdir syntax in detail <decorators.mkdir>`

.. note::

    Remember to look at the example code:

        * :ref:`new_manual.mkdir.code`


***************************************
Overview
***************************************

    In |new_manual.transform_in_parallel.chapter_num|, we saw that we could use :ref:`@follows(mkdir()) <new_manual.follows.mkdir>` to
    ensure that output directories exist:

    .. code-block:: python
        :emphasize-lines: 4

        #
        #   create_new_files() @follows mkdir
        #
        @follows(mkdir("output/results/here"))
        @originate(["output/results/here/a.start_file",
                    "output/results/here/b.start_file"])
        def create_new_files(output_file_pair):
            pass


    This ensures that the decorated task follows (:ref:`@follows <new_manual.follows.mkdir>`) the
    making of the specified directory (``mkdir()``).

    Sometimes, however, the **Output** is intended not for any single directory but a group
    of destinations depending on the parsed contents of **Input** paths.

*********************************************************************************************************************
Creating directories after string substitution in a zoo...
*********************************************************************************************************************

    You may remember :ref:`this example <new_manual.output_file_names.formatter.zoo>` from |new_manual.output_file_names.chapter_num|:

    We want to feed the denizens of a zoo. The original file names are spread over several directories and we
    group their food supply by the *clade* of the animal in the following manner:

        .. image:: ../../images/simple_tutorial_zoo_animals_formatter_example.jpg
           :scale: 50

        .. code-block:: python
            :emphasize-lines: 13,14

            #   Put different animals in different directories depending on their clade
            @transform(create_initial_files,                                       # Input

                       formatter(".+/(?P<clade>\w+).(?P<tame>\w+).animals"),       # Only animals: ignore plants!

                       "{subpath[0][1]}/{clade[0]}/{tame[0]}.{subdir[0][0]}.food", # Replacement

                       "{subpath[0][1]}/{clade[0]}",                               # new_directory
                       "{subdir[0][0]}",                                           # animal_name
                       "{tame[0]}")                                                # tameness
            def feed(input_file, output_file, new_directory, animal_name, tameness):
                print "%40s -> %90s" % (input_file, output_file)
                # this blows up
                # open(output_file, "w")


    The example code from |new_manual.output_file_names.chapter_num| is, however, incomplete. If we were to actually create the specified
    files we would realise that we had forgotten to create the destination directories ``reptiles``, ``mammals`` first!

==============================================================================
using :ref:`formatter() <decorators.formatter>`
==============================================================================

    We could of course create directories manually.
    However, apart from being tedious and error prone, we have already gone to some lengths
    to parse out the diretories for :ref:`@transform <decorators.transform>`.
    Why don't we use the same logic to make the directories?

    Can you see the parallels between the syntax for :ref:`@mkdir <decorators.mkdir>` and :ref:`@transform <decorators.transform>`?

        .. code-block:: python

            # create directories for each clade
            @mkdir(    create_initial_files,                                       # Input

                       formatter(".+/(?P<clade>\w+).(?P<tame>\w+).animals"),       # Only animals: ignore plants!
                       "{subpath[0][1]}/{clade[0]})                                # new_directory

            #   Put animals of each clade in the same directory
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

    See the :ref:`example code <new_manual.mkdir.code>`

==============================================================================
using :ref:`regex() <decorators.regex>`
==============================================================================

    If you are particularly fond of using regular expression to parse file paths,
    you could also use :ref:`regex() <decorators.regex>`:


        .. code-block:: python

            # create directories for each clade
            @mkdir(    create_initial_files,                                       # Input

                       regex(r"(.*?)/?(\w+)/(?P<clade>\w+).(?P<tame>\w+).animals"), # Only animals: ignore plants!
                       r"\1/\g<clade>")                                             # new_directory

            #   Put animals of each clade in the same directory
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

