.. vim: set fileencoding=utf-8 :
.. Pavel Korshunov <pavel.korshunov@idiap.ch>
.. Wed 19 Oct 22:36:22 2016 CET

.. image:: https://img.shields.io/badge/docs-available-orange.svg
   :target: https://www.idiap.ch/software/bob/docs/bob/bob.pad.base/master/index.html
.. image:: https://gitlab.idiap.ch/bob/bob.pad.base/badges/v2.3.1/pipeline.svg
   :target: https://gitlab.idiap.ch/bob/bob.pad.base/commits/v2.3.1
.. image:: https://gitlab.idiap.ch/bob/bob.pad.base/badges/v2.3.1/coverage.svg
   :target: https://gitlab.idiap.ch/bob/bob.pad.base/commits/v2.3.1
.. image:: https://img.shields.io/badge/gitlab-project-0000c0.svg
   :target: https://gitlab.idiap.ch/bob/bob.pad.base

========================================
Scripts to run anti-spoofing experiments
========================================

This package is part of the signal-processing and machine learning toolbox
Bob_. This package is the base of ``bob.pad`` family of packages, which allow to run comparable and reproducible
presentation attack detection (PAD) experiments on publicly available databases.

This package contains basic functionality to run PAD experiments.
It provides a generic ``./bin/spoof.py`` script that takes several parameters, including:

* A database and its evaluation protocol
* A data preprocessing algorithm
* A feature extraction algorithm
* A PAD algorithm

All these steps of the PAD system are given as configuration files.

In this base class implementation, only a core functionality is implemented. The specialized algorithms should
be provided by other packages, which are usually in the ``bob.pad`` namespace, like a ``bob.pad.voice`` package.

Installation
------------

Complete Bob's `installation`_ instructions. Then, to install this package,
run::

  $ conda install bob.pad.base


Contact
-------

For questions or reporting issues to this software package, contact our
development `mailing list`_.


.. Place your references here:
.. _bob: https://www.idiap.ch/software/bob
.. _installation: https://gitlab.idiap.ch/bob/bob/wikis/Installation
.. _mailing list: https://groups.google.com/forum/?fromgroups#!forum/bob-devel
