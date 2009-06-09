.. _Introduction:

************
Introduction
************

The :mod:`ruffus` module is a lightweight way to add support 
for running computational pipelines.

============
Features
============

The :mod:`ruffus` provides automatic support for
 
        * Managing dependencies
        * Parallel jobs
        * Re-starting from arbitrary points, especially after errors
        * Display of the pipeline as a flowchart
        * Reporting


.. _Installation:

==================
Installation
==================

The easy way 
============

    rufus is available as an 
    `easy-install <http://peak.telecommunity.com/DevCenter/EasyInstall>`_ -able package 
    on the `Python Package Index <http://pypi.python.org/pypi/Sphinx>`_.

    #) Install setuptools::

        wget peak.telecommunity.com/dist/ez_setup.py
        sudo python ez_setup.py

    #) Install *Ruffus* automatically::
    
        easy_install -U ruffus

The most up-to-date code:
==============================
    More rarely, the most up-to-date code can be found from 

      * download the latest sources from 
        `here <http://code.google.com/p/ruffus/downloads/list>`_ 

        or check out the latest code from svn::

            svn checkout http://ruffus.googlecode.com/svn/trunk/ ruffus-read-only
    
        or ask to be a project member and enter your google name::

            svn checkout https://ruffus.googlecode.com/svn/trunk/ ruffus --username yourname

      * To install, type::
        
           python setup.py install


=============================
Whence the name *Ruffus*?
=============================

.. image:: images/cyl_ruffus.jpg

**Cylindrophis ruffus** is the name of the 
`red-tailed pipe snake <http://en.wikipedia.org/wiki/Cylindrophis_ruffus>`_ (bad python-y pun)
which can be found in `Hong Kong <http://www.discoverhongkong.com/eng/index.html>`_ where the author comes from.
Be careful not to step on one when running down country park lanes at full speed 
in Hong Kong: this snake is a `rare breed <http://www.hkras.org/eng/info/hkspp.htm>`_!

*Ruffus* is a shy creature, and pretends to be a cobra by putting up its red tail and ducking its
head in its coils when startled. It does most of its work at night and sleeps during the day:
typical of many python programmers!

The original image is from `wikimedia <http://upload.wikimedia.org/wikipedia/commons/a/a1/Cyl_ruffus_061212_2025_tdp.jpg>`_





























