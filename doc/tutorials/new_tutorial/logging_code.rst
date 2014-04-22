.. include:: ../../global.inc
.. include:: manual_chapter_numbers.inc

.. _new_manual.logging.code:

######################################################################################################
|new_manual.logging.chapter_num|: Python Code for Logging progress through a pipeline
######################################################################################################

.. seealso::

    * :ref:`Manual Table of Contents <new_manual.table_of_contents>`
    * Back to |new_manual.logging.chapter_num|: :ref:`Logging progress through a pipeline <new_manual.logging>`

****************************************
Rotating set of file logs
****************************************

    .. code-block:: python
        :emphasize-lines: 10,14,17,31

        import logging
        import logging.handlers

        LOG_FILENAME = '/tmp/ruffus.log'

        # Set up a specific logger with our desired output level
        logger = logging.getLogger('My_Ruffus_logger')
        logger.setLevel(logging.DEBUG)

        # Rotate a set of 5 log files every 2kb
        handler = logging.handlers.RotatingFileHandler(
                      LOG_FILENAME, maxBytes=2000, backupCount=5)

        # Add the log message handler to the logger
        logger.addHandler(handler)

        # Ruffus pipeline
        from ruffus import *

        # Start with some initial data file of yours...
        initial_file = "job1.input"
        open(initial_file, "w")

        @transform( initial_file,
                    suffix(".input"),
                    ".output1"),
        def first_task(input_file, output_file):
            "Some detailed description"
            pass

        #   use our custom logging object
        pipeline_run(logger=logger)
        print open("/tmp/ruffus.log").read()

