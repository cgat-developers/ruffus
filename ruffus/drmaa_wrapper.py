#!/usr/bin/env python
################################################################################
#
#
#   drmaa_wrapper.py
#
#   Copyright (C) 2013 Leo Goodstadt
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
:mod:`ruffus.cmdline` -- Overview
********************************************

.. moduleauthor:: Leo Goodstadt <ruffus@llew.org.uk>


    #
    #   Using drmaa
    #
    from ruffus import *
    import drmaa_wrapper

"""

import sys, os
import stat
#
#   tempfile for drmaa scripts
#
import tempfile
import datetime
import subprocess
import time



#_________________________________________________________________________________________

#   error_drmaa_job

#_________________________________________________________________________________________
class error_drmaa_job(Exception):
    """
    All exceptions throw in this module
    """
    def __init__(self, *errmsg):
        Exception.__init__(self, *errmsg)



#_________________________________________________________________________________________

#   read_stdout_stderr_from_files

#_________________________________________________________________________________________
def read_stdout_stderr_from_files( stdout_path, stderr_path, logger = None, cmd_str = "", tries=5):
    '''
    Reads the contents of two specified paths and returns the strings

    Thanks to paranoia approach contributed by Andreas Heger:

        Retry just in case file system hasn't committed.

        Logs error if files are missing: No big deal?

        Cleans up files afterwards

        Returns tuple of stdout and stderr.

    '''
    #
    #   delay up to 10 seconds until files are ready
    #
    for xxx in range(tries):
        if os.path.exists( stdout_path ) and os.path.exists( stderr_path ):
            break
        time.sleep(2)

    try:
        stdout = open( stdout_path, "r" ).readlines()
    except IOError:
        exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
        msg = str(exceptionValue)
        if logger:
            logger.warn( "could not open stdout: %s for \n%s" % (msg, cmd_str))
        stdout = []

    try:
        stderr = open( stderr_path, "r" ).readlines()
    except IOError:
        exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
        msg = str(exceptionValue)
        if logger:
            logger.warn( "could not open stderr: %s for \n%s" % (msg, cmd_str))
        stderr = []

    #
    #   cleanup ignoring errors
    #
    try:
        os.unlink( stdout_path )
        os.unlink( stderr_path )
    except OSError:
        pass

    return stdout, stderr


#_________________________________________________________________________________________

#   setup_drmaa_job

#_________________________________________________________________________________________
def setup_drmaa_job( drmaa_session, job_name, job_environment, working_directory, job_other_options):

    job_template = drmaa_session.createJobTemplate()

    if not working_directory:
        job_template.workingDirectory = os.getcwd()
    else:
        job_template.workingDirectory = working_directory
    if job_environment:
        # dictionary e.g. { 'BASH_ENV' : '~/.bashrc' }
        job_template.jobEnvironment = job_environment
    job_template.args = []
    if job_name:
        job_template.jobName = job_name
    else:
        # nameless jobs sometimes breaks drmaa implementations...
        job_template.jobName = "ruffus_job_" + "_".join(map(str, datetime.datetime.now().timetuple()[0:6]))

    #
    # optional job parameters
    #
    job_template.nativeSpecification = job_other_options

    # separate stdout and stderr
    job_template.joinFiles=False

    return job_template

#_________________________________________________________________________________________

#   write_job_script_to_temp_file

#_________________________________________________________________________________________
def write_job_script_to_temp_file( cmd_str, job_script_directory, job_name, job_other_options, job_environment, working_directory):
    '''
        returns (job_script_path, stdout_path, stderr_path)

    '''
    import sys
    time_stmp_str = "_".join(map(str, datetime.datetime.now().timetuple()[0:6]))
    # create script directory if necessary
    # Ignore errors rather than test for existence to avoid race conditions
    try:
        os.makedirs(job_script_directory)
    except:
        pass
    tmpfile = tempfile.NamedTemporaryFile(mode='w+b', prefix='drmaa_script_' + time_stmp_str + "__", dir = job_script_directory,  delete = False)

    #
    #   hopefully #!/bin/sh is universally portable among unix-like operating systems
    #
    tmpfile.write( "#!/bin/sh\n" )
    #
    # log parameters as suggested by Bernie Pope
    #
    for title, parameter in (   ("job_name",             job_name,         ),
                                ("job_other_options",    job_other_options,),
                                ("job_environment",      job_environment,  ),
                                ("working_directory",     working_directory),       ):
        if parameter:
            tmpfile.write( "#%s=%s\n" % (title, parameter))

    tmpfile.write( cmd_str + "\n" )
    tmpfile.close()

    job_script_path = os.path.abspath( tmpfile.name )
    stdout_path = job_script_path + ".stdout"
    stderr_path = job_script_path + ".stderr"

    os.chmod( job_script_path, stat.S_IRWXG | stat.S_IRWXU )

    return (job_script_path, stdout_path, stderr_path)



#_________________________________________________________________________________________

#   run_job_using_drmaa

#_________________________________________________________________________________________
def run_job_using_drmaa (cmd_str, job_name = None, job_other_options = "", job_script_directory = None, job_environment = None, working_directory = None, retain_job_scripts = False, logger = None, drmaa_session = None):

    """
    Runs specified command remotely using drmaa,
    either with the specified session, or the module shared drmaa session
    """
    import drmaa

    #
    #   used specified session else module session
    #
    if drmaa_session == None:
        raise error_drmaa_job( "Please specify a drmaa_session in run_job()")

    #
    #   make job template
    #
    job_template = setup_drmaa_job( drmaa_session, job_name, job_environment, working_directory, job_other_options)

    #
    #   make job script
    #
    if not job_script_directory:
        job_script_directory = os.getcwd()
    job_script_path, stdout_path, stderr_path = write_job_script_to_temp_file( cmd_str, job_script_directory, job_name, job_other_options, job_environment, working_directory)
    job_template.remoteCommand      = job_script_path
    # drmaa paths specified as [hostname]:file_path.
    # See http://www.ogf.org/Public_Comment_Docs/Documents/2007-12/ggf-drmaa-idl-binding-v1%2000%20RC7.pdf
    job_template.outputPath         = ":" + stdout_path
    job_template.errorPath          = ":" + stderr_path


    #
    #   Run job and wait
    #
    jobid = drmaa_session.runJob(job_template)
    if logger:
        logger.debug( "job has been submitted with jobid %s" % str(jobid ))

    try:
        retval = drmaa_session.wait(jobid, drmaa.Session.TIMEOUT_WAIT_FOREVER)
    except Exception:
        exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
        msg = str(exceptionValue)
        # ignore message 24 in PBS
        # code 24: drmaa: Job finished but resource usage information and/or termination status could not be provided.":
        if not msg.message.startswith("code 24"): raise
        if logger:
            logger.log(MESSAGE, "Warning %s\n"
                                   "The original command was:\n%s\njobid=jobid\n"
                                     (msg.message, cmd_str,jobid) )
        retval = None


    #
    #   Read output
    #
    stdout, stderr = read_stdout_stderr_from_files( stdout_path, stderr_path, logger, cmd_str)

    #
    #   Throw if failed
    #
    if retval and (not retval.hasExited or retval.exitStatus):
        raise error_drmaa_job( "The drmaa command was terminated by signal %i:\n"
                               "The original command was:\n%s\n"
                               "The jobid was: %s\n"
                               "The job script name was: %s\n"
                               "The stderr was: \n%s\n\n"
                               "The stdout was: \n%s\n\n" %
                                 (retval.exitStatus, cmd_str,
                                     jobid,
                                     job_script_path,
                                    "".join( stderr),
                                    "".join( stdout)
                                     ) )


    #
    #   clean up job template
    #
    drmaa_session.deleteJobTemplate(job_template)

    #
    #   Cleanup job script unless retain_job_scripts is set
    #
    if retain_job_scripts:
        # job scripts have the jobid as an extension
        os.rename(job_script_path, job_script_path + ".%s" % jobid )
    else:
        try:
            os.unlink( job_script_path )
        except OSError:
            if logger:
                logger.warn( "Temporary job script wrapper '%s' missing (and ignored) at clean-up" % job_script_path )

    return stdout, stderr


#_________________________________________________________________________________________

#   run_job_locally

#_________________________________________________________________________________________
def run_job_locally (cmd_str, logger = None):
    """
    Runs specified command locally instead of drmaa
    """
    process = subprocess.Popen(  cmd_str,
                                 cwd = os.getcwd(),
                                 shell = True,
                                 stdin = subprocess.PIPE,
                                 stdout = subprocess.PIPE,
                                 stderr = subprocess.PIPE )

    # process.stdin.close()
    stdout, stderr = process.communicate()

    if process.returncode != 0:
        raise error_drmaa_job( "The locally run command was terminated by signal %i:\n"
                               "The original command was:\n%s\n"
                               "The stderr was: \n%s\n\n"
                               "The stdout was: \n%s\n\n" %
                                 (-process.returncode, cmd_str, "".join( stderr), "".join( stdout)) )

    return stdout.splitlines(True), stderr.splitlines(True)


#_________________________________________________________________________________________

#   touch_output_files

#_________________________________________________________________________________________
def touch_output_files (cmd_str, output_files, logger = None):
    """
    Touches output files instead of actually running the command string
    """

    if not output_files or not len(output_files):
        if logger:
            logger.debug("No output files to 'touch' for command:\n%s")
        return

    # make sure is list
    ltypes=(list, tuple)
    if not isinstance(output_files, ltypes):
        output_files = [output_files]
    else:
        output_files = list(output_files)

    #
    #    flatten list of file names
    #    from http://rightfootin.blogspot.co.uk/2006/09/more-on-python-flatten.html
    #
    i = 0
    while i < len(output_files):
        while isinstance(output_files[i], ltypes):
            if not output_files[i]:
                output_files.pop(i)
                i -= 1
                break
            else:
                output_files[i:i + 1] = output_files[i]
        i += 1


    for f  in output_files:
        # ignore non strings
        if not isinstance (f, basestring):
            continue

        # create file
        if not os.path.exists(f):
            # this should be guaranteed to close the new file immediately?
            with open(f, 'w') as p: pass

        # touch existing file
        else:
            os.utime(f, None)




#_________________________________________________________________________________________

#   run_job

#_________________________________________________________________________________________
def run_job(cmd_str, job_name = None, job_other_options = None, job_script_directory = None, job_environment = None, working_directory = None, logger = None, drmaa_session = None, retain_job_scripts = False, run_locally = False, output_files = None, touch_only = False):
    """
    Runs specified command either using drmaa, or locally or only in simulation (touch the output files only)
    """

    if touch_only:
        touch_output_files (cmd_str, output_files, logger)
        return "","",

    if run_locally:
        return run_job_locally (cmd_str, logger)


    return run_job_using_drmaa (cmd_str, job_name, job_other_options, job_script_directory, job_environment, working_directory, retain_job_scripts, logger, drmaa_session)
