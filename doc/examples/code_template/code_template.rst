.. include:: ../../global.inc

.. _code_template:

******************************************************
Standard code for developing Ruffus pipelines
******************************************************



We find that much of our Ruffus pipeline code is built on the same template and this is generally 
a good place to start developing a new pipeline.

All you need to do is 

 * change the file name(!)
 * add any command line arguments
 * Place your pipeline code where it says
    ::

        #       Put pipeline code here
    
    and run the script

 .. note::

        Python code for the Ruffus script template is available for:

            * :ref:`Display <code_template.code>` or 
            * :download:`Download <../../static_data/example_scripts/ruffus_template.py>`

The standard code uses the ubiquitous optparse module (but should be easily adaptable for
argparse) and provides command line options for:



#################
1) Logging
#################
    
    The script provides for logging both to the command line:
        ::

            myscript -v
            myscript --verbose

    and an optional log file:
        ::
    
            myscript --log_file PIPELINE.LOG_FILE

    Loggin is ignored if ``--verbose`` or ``--log_file`` are not specified
    on the command line

    To write to the same log file from multiple processes, you need to pass
    ``logger_proxy`` rather than ``logger`` in your Ruffus decorators, as well as
    ``logging_mutex``. The latter allows writing to the log files to be synchronised 
    across different jobs:

        ::
    
            with logging_mutex:
    
                logger_proxy.info("Look Ma. No hands")
             
    Logging is set up so that you can write 


=================================
        A) Only to the log file:
=================================
            ::
        
                logger.info("A message")
    
=================================
        B) Only to the display:
=================================
            ::
        
                logger.debug("A message")
    
======================================
        C) To both simultaneously:
======================================
            ::
        
                logger.log(MESSAGE, "A message")
    

##################################
3) Tracing pipeline progress
##################################

    This is extremely useful for understanding what is happening with your pipeline, what tasks and which
    jobs are up-to-date etc.

    See the :ref:`manual <manual.tracing_pipeline_parameters>` for a full discussion 

    To trace the pipeline, call script with the following options
        ::

            myscript -n

            or 

            myscript --just_print

    Increasing levels of verbosity (``-v`` to ``-vvvvvvvvv``) provide more detailed output


##################################
4) Printing a flowchart
##################################

    This can be specified using the following option:

        ::
            
            myscript --flowchart xxxchart.svg

    The extension of the flowchart file indicates what format the flowchart should take,
    for example, ``svg``, ``jpg`` etc.


#######################################################
5) Running the pipeline on multiple processors
#######################################################

    Optionally specify the number of parallel strands of execution and which the final task is::

        myscript --jobs 15 --target_tasks "final_task"
        myscript -j 15
    
    

