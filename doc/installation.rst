.. include:: global.inc
.. _Installation:

************************************
Installation
************************************

:mod:`Ruffus` is a lightweight python module for building computational pipelines.

.. note ::

    Ruffus requires Python 3.11 or later. The test matrix covers Python 3.11,
    3.12, 3.13 and 3.14. Older Ruffus releases remain available for older
    Python versions.



==============================================================================
conda installation
==============================================================================

The recomended method for installing CGAT-ruffus is to install using `conda <https://conda.io/en/latest/>`_ through
the `bioconda <https://anaconda.org/bioconda/ruffus>`_ channel. The reson for conda being the prefferred method
is that the dependancied are taken care of.

    ::

        conda install -c bioconda ruffus

==============================================================================
pip installation
==============================================================================

    *Ruffus* is also available on `pypi <https://pypi.org/project/ruffus/>`_.

    ::

        pip install ruffus

==============================================================================
Manual installation
==============================================================================

To obtain the latest code, check it out from `github <https://github.com/cgat-developers/ruffus>`_ and activate it.

    ::

        git clone https://github.com/cgat-developers/ruffus.git
	cd ruffus
	python setup.py install










