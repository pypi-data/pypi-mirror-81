.. vim: set fileencoding=utf-8 :
.. Mon 08 Aug 2016 10:52:47 CEST

.. image:: https://img.shields.io/badge/docs-available-orange.svg
   :target: https://www.idiap.ch/software/bob/docs/bob/bob.blitz/master/index.html
.. image:: https://gitlab.idiap.ch/bob/bob.blitz/badges/v2.0.22/pipeline.svg
   :target: https://gitlab.idiap.ch/bob/bob.blitz/commits/v2.0.22
.. image:: https://gitlab.idiap.ch/bob/bob.blitz/badges/v2.0.22/coverage.svg
   :target: https://gitlab.idiap.ch/bob/bob.blitz/commits/v2.0.22
.. image:: https://img.shields.io/badge/gitlab-project-0000c0.svg
   :target: https://gitlab.idiap.ch/bob/bob.blitz


====================================
 Python bindings for Blitz++ Arrays
====================================

This package is part of the signal-processing and machine learning toolbox
Bob_. It provides a bridge between our C++ array infrastructure (based on
Blitz++) and NumPy arrays. Almost all of our Python C/C++ extensions use this
package to transparently and efficiently convert NumPy arrays to Blitz++ arrays
and vice-versa.


Installation
------------

Complete Bob's `installation`_ instructions. Then, to install this package,
run::

  $ conda install bob.blitz


Contact
-------

For questions or reporting issues to this software package, contact our
development `mailing list`_.


.. Place your references here:
.. _bob: https://www.idiap.ch/software/bob
.. _installation: https://www.idiap.ch/software/bob/install
.. _mailing list: https://www.idiap.ch/software/bob/discuss
