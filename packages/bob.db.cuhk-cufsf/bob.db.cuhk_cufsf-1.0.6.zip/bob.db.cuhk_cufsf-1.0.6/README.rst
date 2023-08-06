.. vim: set fileencoding=utf-8 :
.. Tiago de Freitas Pereira <tiago.pereira@idiap.ch>
.. Thu Apr 16 16:39:01 CEST 2015



.. image:: https://img.shields.io/badge/docs-available-orange.svg
   :target: https://www.idiap.ch/software/bob/docs/bob/bob.db.cuhk_cufsf/master/index.html
.. image:: https://gitlab.idiap.ch/bob/bob.db.cuhk_cufsf/badges/v1.0.6/pipeline.svg
   :target: https://gitlab.idiap.ch/bob/bob.db.cuhk_cufsf/commits/v1.0.6
.. image:: https://gitlab.idiap.ch/bob/bob.db.cuhk_cufsf/badges/v1.0.6/coverage.svg
   :target: https://gitlab.idiap.ch/bob/bob.db.cuhk_cufsf/commits/v1.0.6
.. image:: https://img.shields.io/badge/gitlab-project-0000c0.svg
   :target: https://gitlab.idiap.ch/bob/bob.db.cuhk_cufsf


=======================================================
CUHK Face Sketch FERET Database (CUFSF)
=======================================================

This package is part of the signal-processing and machine learning toolbox
Bob_.
This package contains the access API and descriptions for the `CUHK Face Sketch Database (CUFS) <http://mmlab.ie.cuhk.edu.hk/archive/facesketch.html>`.
The actual raw data for the database should be downloaded from the original URL.
This package only contains the Bob accessor methods to use the DB directly from python, with the original protocol of the database.

CUHK Face Sketch FERET Database (CUFSF) is for research on face sketch synthesis and face sketch recognition.
It includes 1194 faces from the FERET database with their respective sketches (drawn by an artist based on a photo of the FERET database).


Installation
------------

Follow our `installation`_ instructions. Then, to install this package, run::
   
   $ conda install bob.db.cuhk_cufsf


Contact
-------

For questions or reporting issues to this software package, contact our
development `mailing list`_.


.. Place your references here:
.. _bob: https://www.idiap.ch/software/bob
.. _installation: https://gitlab.idiap.ch/bob/bob/wikis/Installation
.. _mailing list: https://groups.google.com/forum/?fromgroups#!forum/bob-devel
