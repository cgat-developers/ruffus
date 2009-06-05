******
Todo
******

.. _todo-cleanup:

=========================================================
Cleanup
=========================================================

The plan is to store the files and directories created via
a standard interface.

The placeholders for this are a function call ``register_cleanup``.

Jobs can specify the files they created and which need to be
deleted by returning a list of file names from the job function.

So::

    raise Exception = Error
    
    return False = halt pipeline now
    
    return string / list of strings = cleanup files/directories later
    
    return anything else = ignored
    

The cleanup file/directory store interface can be connected to
a text file or a database.

The cleanup function would look like this::

    pipeline_cleanup(cleanup_log(../cleanup.log"), [instance ="october19th" ])
    
This would require pipeline_run to have additional parameters to
    describe a particular run of the pipeline.
    

* Files would be deleted in reverse order, and directories after files.
* By default, only empty directories would be removed. 

  But this could be changed with a ``--forced_remove_dir`` option 
* An ``--remove_empty_parent_directories`` option would be 
  supported by `os.removedirs(path) <http://docs.python.org/library/os.html#os.removedirs>`_.


.. _todo-combining:

=========================================================
Combining files
=========================================================

A common operation (See :ref:`intermediate example <intermediate-pipelines>` and
:ref:`complicated example <complicated-pipelines>`) seems to be combining multiple
input files into one or more output files (i.e. a "many->1" operation). 

A the moment, this can be easily done by writing a simple parameter generating function
with a glob (see :ref:`this code <intermediate-pipelines-combining_files>`.)

However, we could directly support this in ruffus in two ways, both leveraging ``@files_re``.

The idea is that input files to be grouped together should share similar
traits identified by either a regular expression or a function.

Suppose we had the following files::

    cows.mammals.animal
    horses.mammals.animal
    sheep.mammals.animal
    
    snake.reptile.animal
    lizard.reptile.animal
    crocodile.reptile.animal
    
    pufferfish.fish.animal
    
and we wanted to end up with three different resulting output::

    cow.mammals.animal
    horse.mammals.animal
    sheep.mammals.animal
        -> mammals.results
    
    snake.reptile.animal
    lizard.reptile.animal
    crocodile.reptile.animal
        -> reptile.results
    
    pufferfish.fish.animal
        -> fish.results

We could either add a "combining" regex parameter::

    # \1 = species [cow, horse]
    # \2 = phylogenetics group [mammals, reptile, fish]
    @files_re(  "*.animal", 
                r"(.+)\.(.+)\.animal",        
                combining(r"\2"),           # regular expression showing that 
                                            # "mammals/reptile" etc. groups files
                r"\1.\2.animal",            # input file
                r"\2.results")              # output file(s)
    def sort_animals_into_groups(species_file, result_file):
        " ... more code here"
        
Or we could allow a grouping function like the *key* parameter 
in `itertools.groupby <http://docs.python.org/library/itertools.html#itertools.groupby>`_::

    @files_re(  "*.animal", 
                r"(.+)\.(.+)\.animal",        
                combining_func(lambda x: x.split(".")[1]),
                r"\1.\2.animal",            # input file
                r"\2.results")              # output file(s)
    def sort_animals_into_groups(species_file, result_file):
        " ... more code here"
        
In both cases, the extra parameter would be wrapped by a "tagging" class 
(``combining`` and ``combining_func``) for clarity.

Is this too much extra complexity for ruffus or ``@files_re`` to support? 

Is the syntactic convenience worthwhile?
    


    
=========================================================
Return values
=========================================================
Have a system for allowing values to be passed back from jobs


=========================================================
Multiprocessing
=========================================================
Can we run jobs on remote processes / SGE / Hadoop?
