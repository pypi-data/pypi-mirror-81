======================
AtomNeb Python Package
======================

.. image:: https://img.shields.io/pypi/v/atomneb.svg?style=flat
    :target: https://pypi.python.org/pypi/atomneb/
    :alt: PyPI Version

.. image:: https://travis-ci.org/atomneb/AtomNeb-py.svg?branch=master
    :target: https://travis-ci.org/atomneb/AtomNeb-py
    :alt: Build Status

.. image:: https://ci.appveyor.com/api/projects/status/gi4ok3wy7jjn1ekb?svg=true
    :target: https://ci.appveyor.com/project/danehkar/atomneb-py
    :alt: Build Status

.. image:: https://coveralls.io/repos/github/atomneb/AtomNeb-py/badge.svg?
    :target: https://coveralls.io/github/atomneb/AtomNeb-py?branch=master
    :alt: Coverage Status

.. image:: https://img.shields.io/badge/license-GPL-blue.svg
    :target: https://github.com/atomneb/AtomNeb-py/blob/master/LICENSE
    :alt: GitHub license

.. image:: https://img.shields.io/badge/python-2.7%2C%203.8-blue.svg
    :alt: Support Python versions 2.7 and 3.8


Description
============

**AtomNeb-py** is a library written in Python for reading atomic data from **AtomNeb**, which is a database containing atomic data stored in the Flexible Image Transport System (FITS) file format for *collisionally excited lines* and *recombination lines* typically observed in spectra of ionized gaseous nebulae. The AtomNeb database were generated for use in `pyEQUIB <https://github.com/equib/pyEQUIB>`_, `proEQUIB <https://github.com/equib/proEQUIB>`_, and other nebular spectral analysis tools. 


Installation
============

Dependent Python Packages
-------------------------

 This package requires the following packages:

    - `NumPy <https://numpy.org/>`_
    - `pandas <https://pandas.pydata.org/>`_
    - `Astropy <https://www.astropy.org/>`_
    
* To get this package with all the FITS file, you can simply use ``git`` command as follows::

        git clone https://github.com/atomneb/AtomNeb-py

* If you plan to use the recent O II recombination coefficients (`Storey, Sochi and Bastin 2017 <http://adsabs.harvard.edu/abs/2017MNRAS.470..379S>`_), you need to unpack them::

        cd AtomNeb-py/atomic-data-rc/
        tar -xvf *.fits.tar.gz


To install the last version, all you should need to do is

.. code-block::

    $ python setup.py install

To install the stable version, you can use the preferred installer program (pip):

.. code-block::

    $ pip install atomneb


References
==========

* Danehkar, A. (2019). AtomNeb: IDL Library for Atomic Data of Ionized Nebulae. *J. Open Source Softw.*, **4**, 898. doi:`10.21105/joss.00898 <https://doi.org/10.21105/joss.00898>`_

