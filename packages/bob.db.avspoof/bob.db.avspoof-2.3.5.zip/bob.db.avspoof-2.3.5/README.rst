.. vim: set fileencoding=utf-8 :
.. Tue 16 Aug 12:57:10 CEST 2016

.. image:: https://img.shields.io/badge/docs-available-orange.svg
   :target: https://www.idiap.ch/software/bob/docs/bob/bob.db.avspoof/master/index.html
.. image:: https://gitlab.idiap.ch/bob/bob.db.avspoof/badges/v2.3.5/pipeline.svg
   :target: https://gitlab.idiap.ch/bob/bob.db.avspoof/commits/v2.3.5
.. image:: https://gitlab.idiap.ch/bob/bob.db.avspoof/badges/v2.3.5/coverage.svg
   :target: https://gitlab.idiap.ch/bob/bob.db.avspoof/commits/v2.3.5
.. image:: https://img.shields.io/badge/gitlab-project-0000c0.svg
   :target: https://gitlab.idiap.ch/bob/bob.db.avspoof


====================================
 AVspoof Database Interface for Bob
====================================

This package is part of the signal-processing and machine learning toolbox
Bob_. It contains the access API and descriptions for the AVspoof_ Database.
The database contains speech recordings of 44 persons (31 males and 13 females)
performed during the course of two months in four different sessions. The
database also contains several spoofing attacks for the recorded speech,
including voice conversion, speech synthesis, and replay attacks.  Replay
attacks were performed using laptop or two different phones.

This package contains the Bob_-compliant interface implementation with methods
to use the database directly from Python with our certified protocols.


Installation
------------

Complete Bob's `installation`_ instructions. Then, to install this package,
run::

  $ conda install bob.db.avspoof


Contact
-------

For questions or reporting issues to this software package, contact our
development `mailing list`_.


.. Place your references here:
.. _bob: https://www.idiap.ch/software/bob
.. _installation: https://www.idiap.ch/software/bob/install
.. _mailing list: https://www.idiap.ch/software/bob/discuss
.. _avspoof: https://www.idiap.ch/dataset/avspoof
