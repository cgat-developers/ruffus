.. include:: global.inc
.. _Installation:

************************************
Installation
************************************

:mod:`Ruffus` is a lightweight python module for building computational pipelines.

.. note ::

    Ruffus requires Python 2.6 or higher or Python 3.0 or higher



==============================================================================
The easy way
==============================================================================

    *Ruffus* is available as an
    `easy-install <http://peak.telecommunity.com/DevCenter/EasyInstall>`_ -able package
    on the `Python Package Index <http://pypi.python.org/pypi/Sphinx>`_.

    ::

        sudo pip install ruffus --upgrade

    This may also work for older installations::

        easy_install -U ruffus


    See below if ``eady_install`` is missing


==============================================================================
The most up-to-date code:
==============================================================================
        * `Download the latest sources <https://pypi.python.org/pypi/ruffus>`_ or

        * Check out the latest code from Google using git::

            git clone https://bunbun68@code.google.com/p/ruffus/ .

        * Bleeding edge Ruffus development takes place on github::

            git clone git@github.com:bunbun/ruffus.git .


        * To install after downloading, change to the , type::

             python ./setup.py install

======================
Prequisites
======================
==============================================================================
Installing easy_install
==============================================================================

    If your system doesn't have ``easy_install``, you can `install  <ubuntu/linux mint>`__ one using a package manager, for example::

        # ubuntu/linux mint
        $ sudo apt-get install python-setuptools
        $ or  sudo yum install python-setuptools

    or manually::

        sudo curl http://peak.telecommunity.com/dist/ez_setup.py | python

    or manually::

        wget peak.telecommunity.com/dist/ez_setup.py
        sudo python ez_setup.py



==============================================================================
Installing pip
==============================================================================

    If Pip is missing::

        $ sudo easy_install -U pip


==============================================================================
 Graphical flowcharts The most up-to-date code:
==============================================================================

    **Ruffus** relies on the ``dot`` programme from `Graphviz <http://www.graphviz.org/>`_
    ("Graph visualisation") to make pretty flowchart representations of your pipelines in multiple
    graphical formats (e.g. ``png``, ``jpg``). The crossplatform Graphviz package can be
    `downloaded here <http://www.graphviz.org/Download.php>`_ for Windows,

    Linux, Macs and Solaris.     For Fedora, try
        ::

            yum list 'graphviz*'

    For ubuntu / Debian, try
        ::

            sudo apt-get install graphviz








