.. vim: set fileencoding=utf-8 :
.. Tue 16 Aug 11:58:23 CEST 2016

.. image:: https://img.shields.io/badge/docs-available-orange.svg
   :target: https://www.idiap.ch/software/bob/docs/bob/bob.db.voxforge/master/index.html
.. image:: https://gitlab.idiap.ch/bob/bob.db.voxforge/badges/v2.3.6/pipeline.svg
   :target: https://gitlab.idiap.ch/bob/bob.db.voxforge/commits/v2.3.6
.. image:: https://gitlab.idiap.ch/bob/bob.db.voxforge/badges/v2.3.6/coverage.svg
   :target: https://gitlab.idiap.ch/bob/bob.db.voxforge/commits/v2.3.6
.. image:: https://img.shields.io/badge/gitlab-project-0000c0.svg
   :target: https://gitlab.idiap.ch/bob/bob.db.voxforge


========================================
 Voxforge Toy Database Interface for Bob
========================================

This package is part of the signal-processing and machine learning toolbox
Bob_.
Voxforge offers a collection of transcribed speech for use with Free and Open Source Speech Recognition Engines. In this package, we design a speaker recognition protocol that uses a small subset of the english audio files (only 6561 files) belonging to 30 speakers randomly selected. This subset is split into three equivalent parts: Training (10 speakers), Development (10 speakers) and Evaluation (10 speakers) sets.


Installation
------------

Complete Bob's `installation`_ instructions. Then, to install this package,
run::

  $ conda install bob.db.voxforge


Contact
-------

For questions or reporting issues to this software package, contact our
development `mailing list`_.


.. Place your references here:
.. _bob: https://www.idiap.ch/software/bob
.. _installation: https://www.idiap.ch/software/bob/install
.. _mailing list: https://www.idiap.ch/software/bob/discuss
