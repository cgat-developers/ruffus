.. _Introduction:

************************************
Installation
************************************

The :mod:`ruffus` module is a lightweight way to add support 
for running computational pipelines.

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


======================
Graphical flowcharts
======================

    **Ruffus** relies on the ``dot`` programme from :ref:`Graphviz<http://www.graphviz.org/>`_
    ("Graph visualisation") to make pretty flowchart representations of your pipelines in multiple
    graphical formats (e.g. ``png``, ``jpg``). The crossplatform Graphviz package can be downloaded 
    :ref:`here<http://www.graphviz.org/Download.php`_ for Windows, Linux, Macs and Solaris. Some Linux
    distributions may include prebuilt packages. 

    For Fedora, try
        ::
        
            yum list 'graphviz*' 
            
    For ubuntu / Debian, try
        ::

            sudo apt-get install graphviz








