################################################################################
#
#   proxy_logger.py
#
#
#   Copyright (c) 10/9/2009 Leo Goodstadt
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
****************************************************************************
Create proxy for logging for use with multiprocessing
****************************************************************************

These can be safely sent (marshalled) across process boundaries


===========
Example 1
===========

    Set up logger from config file::

        from proxy_logger import *
        args={}
        args["config_file"] = "/my/config/file"

        (logger_proxy,
         logging_mutex) = make_shared_logger_and_proxy (setup_std_shared_logger,
                                                        "my_logger", args)


===========
Example 2
===========

    Log to file ``"/my/lg.log"`` in the specified format (Time / Log name / Event type / Message).

    Delay file creation until first log.

    Only log ``Debug`` messages

        Other alternatives for the logging threshold (``args["level"]``) include

            * ``logging.DEBUG``
            * ``logging.INFO``
            * ``logging.WARNING``
            * ``logging.ERROR``
            * ``logging.CRITICAL``

    ::

        from proxy_logger import *
        args={}
        args["file_name"] = "/my/lg.log"
        args["formatter"] = "%(asctime)s - %(name)s - %(levelname)6s - %(message)s"
        args["delay"]     = True
        args["level"]     = logging.DEBUG

        (logger_proxy,
         logging_mutex) = make_shared_logger_and_proxy (setup_std_shared_logger,
                                                        "my_logger", args)

===========
Example 3
===========

    Rotate log files every 20 Kb, with up to 10 backups.
    ::

        from proxy_logger import *
        args={}
        args["file_name"] = "/my/lg.log"
        args["rotating"] = True
        args["maxBytes"]=20000
        args["backupCount"]=10
        (logger_proxy,
         logging_mutex) = make_shared_logger_and_proxy (setup_std_shared_logger,
                                                        "my_logger", args)



==============
To use:
==============

    ::

        (logger_proxy,
         logging_mutex) = make_shared_logger_and_proxy (setup_std_shared_logger,
                                                        "my_logger", args)

        with logging_mutex:
            my_log.debug('This is a debug message')
            my_log.info('This is an info message')
            my_log.warning('This is a warning message')
            my_log.error('This is an error message')
            my_log.critical('This is a critical error message')
            my_log.log(logging.DEBUG, 'This is a debug message')

    Note that the logging function ``exception()`` is not included because python
    stack trace information is not well-marshalled
    (`pickle <http://docs.python.org/library/pickle.html>`_\ d) across processes.

"""


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   imports


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

import sys
import os


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Shared logging


# 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

import multiprocessing
import multiprocessing.managers


import logging
import logging.handlers


#
#   setup_logger
#
def setup_std_shared_logger(logger_name, args):
    """
    This function is a simple around wrapper around the python
    `logging <http://docs.python.org/library/logging.html>`_ module.

    This *logger_factory* example creates logging objects which can
    then be managed by proxy via ``ruffus.proxy_logger.make_shared_logger_and_proxy()``

    This can be:

        * a `disk log file <http://docs.python.org/library/logging.html#filehandler>`_
        * a automatically backed-up `(rotating) log <http://docs.python.org/library/logging.html#rotatingfilehandler>`_.
        * any log specified in a `configuration file <http://docs.python.org/library/logging.html#configuration-file-format>`_

    These are specified in the ``args`` dictionary forwarded by ``make_shared_logger_and_proxy()``

    :param logger_name: name of log
    :param args: a dictionary of parameters forwarded from ``make_shared_logger_and_proxy()``

        Valid entries include:

            .. describe:: "level"

                Sets the `threshold <http://docs.python.org/library/logging.html#logging.Handler.setLevel>`_ for the logger.

            .. describe:: "config_file"

                The logging object is configured from this `configuration file <http://docs.python.org/library/logging.html#configuration-file-format>`_.

            .. describe:: "file_name"

                Sets disk log file name.

            .. describe:: "rotating"

                Chooses a `(rotating) log <http://docs.python.org/library/logging.html#rotatingfilehandler>`_.

            .. describe:: "maxBytes"

                Allows the file to rollover at a predetermined size

            .. describe:: "backupCount"

                If backupCount is non-zero, the system will save old log files by appending the extensions ``.1``, ``.2``, ``.3`` etc., to the filename.

            .. describe:: "delay"

                Defer file creation until the log is written to.

            .. describe:: "formatter"

                `Converts <http://docs.python.org/library/logging.html#formatter-objects>`_ the message to a logged entry string.
                For example,
                ::

                    "%(asctime)s - %(name)s - %(levelname)6s - %(message)s"



    """

    #
    #   Log file name with logger level
    #
    new_logger = logging.getLogger(logger_name)
    if "level" in args:
        new_logger.setLevel(args["level"])

    if "config_file" in args:
        logging.config.fileConfig(args["config_file"])

    else:
        if "file_name" not in args:
            raise Exception(
                "Missing file name for log. Remember to set 'file_name'")
        log_file_name = args["file_name"]

        if "rotating" in args:
            rotating_args = {}
            # override default
            rotating_args["maxBytes"] = args.get("maxBytes", 100000)
            rotating_args["backupCount"] = args.get("backupCount", 5)
            handler = logging.handlers.RotatingFileHandler(
                log_file_name, **rotating_args)
        else:
            defer_loggin = "delay" in args
            handler = logging.handlers.RotatingFileHandler(
                log_file_name, delay=defer_loggin)

        #       %(name)s
        #       %(levelno)s
        #       %(levelname)s
        #       %(pathname)s
        #       %(filename)s
        #       %(module)s
        #       %(funcName)s
        #       %(lineno)d
        #       %(created)f
        #       %(relativeCreated)d
        #       %(asctime)s
        #       %(msecs)d
        #       %(thread)d
        #       %(threadName)s
        #       %(process)d
        #       %(message)s
        #
        # E.g.: "%(asctime)s - %(name)s - %(levelname)6s - %(message)s"
        #
        if "formatter" in args:
            my_formatter = logging.Formatter(args["formatter"])
            handler.setFormatter(my_formatter)

        new_logger.addHandler(handler)

    #
    #   This log object will be wrapped in proxy
    #
    return new_logger


#
#   Proxy object for logging
#       Logging messages will be marshalled (forwarded) to the process where the
#       shared log lives
#
class LoggerProxy(multiprocessing.managers.BaseProxy):
    def debug(self, *args, **kwargs):
        return self._callmethod('debug', args, kwargs)

    def log(self, *args, **kwargs):
        return self._callmethod('log', args, kwargs)

    def info(self, *args, **kwargs):
        return self._callmethod('info', args, kwargs)

    def warning(self, *args, **kwargs):
        return self._callmethod('warning', args, kwargs)

    def error(self, *args, **kwargs):
        return self._callmethod('error', args, kwargs)

    def critical(self, *args, **kwargs):
        return self._callmethod('critical', args, kwargs)

    def log(self, *args, **kwargs):
        return self._callmethod('log', args, kwargs)

    def __str__(self):
        return "<LoggingProxy>"

    def __repr__(self):
        return 'LoggerProxy()'

#
#   Register the setup_logger function as a proxy for setup_logger
#
#   We use SyncManager as a base class so we can get a lock proxy for synchronising
#       logging later on
#


class LoggingManager(multiprocessing.managers.SyncManager):
    """
    Logging manager sets up its own process and will create the real Log object there
    We refer to this (real) log via proxies
    """
    pass


def make_shared_logger_and_proxy(logger_factory, logger_name, args):
    """
    Make a `logging <http://docs.python.org/library/logging.html>`_ object
    called "\ ``logger_name``\ " by calling ``logger_factory``\ (``args``\ )

    This function will return a proxy to the shared logger which can be copied to jobs
    in other processes, as well as a mutex which can be used to prevent simultaneous logging
    from happening.

    :param logger_factory: functions which creates and returns an object with the
                           `logging <http://docs.python.org/library/logging.html>`_ interface.
                           ``setup_std_shared_logger()`` is one example of a logger factory.
    :param logger_name: name of log
    :param args: parameters passed (as a single argument) to ``logger_factory``
    :returns: a proxy to the shared logger which can be copied to jobs in other processes
    :returns: a mutex which can be used to prevent simultaneous logging from happening

    """
    #
    #   make shared log and proxy
    #
    manager = LoggingManager()
    manager.register('setup_logger',
                     logger_factory,
                     proxytype=LoggerProxy,
                     exposed=('critical', 'log',
                              'info', 'debug', 'warning', 'error'))
    manager.start()
    logger_proxy = manager.setup_logger(logger_name, args)

    #
    #   make sure we are not logging at the same time in different processes
    #
    logging_mutex = manager.Lock()

    return logger_proxy, logging_mutex
