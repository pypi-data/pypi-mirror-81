.. vim: set fileencoding=utf-8 :
.. Wed Jan 16 10:07:12 CET 2019

.. image:: https://img.shields.io/badge/docs-available-orange.svg
   :target: https://www.idiap.ch/software/bob/docs/bob/bob.db.casia_fasd/master/index.html
.. image:: https://gitlab.idiap.ch/bob/bob.db.casia_fasd/badges/v2.0.10/pipeline.svg
   :target: https://gitlab.idiap.ch/bob/bob.db.casia_fasd/commits/v2.0.10
.. image:: https://gitlab.idiap.ch/bob/bob.db.casia_fasd/badges/v2.0.10/coverage.svg
   :target: https://gitlab.idiap.ch/bob/bob.db.casia_fasd/commits/v2.0.10
.. image:: https://img.shields.io/badge/gitlab-project-0000c0.svg
   :target: https://gitlab.idiap.ch/bob/bob.db.casia_fasd


=====================================================
 CASIA Face Anti-Spoofing Database Interface for Bob
=====================================================

This package is part of the signal-processing and machine learning toolbox
Bob_. This package contains the Bob_ accessor methods to use the CASIA-FASD
directly from python, with our certified protocols. The actual raw data for
`CASIA FASD`_ database should be downloaded from the original URL. The
CASIA-FASD database is a spoofing attack database which consists of three types
of attacks: warped printed photographs, printed photographs with cut eyes and
video attacks. The samples are taken with three types of cameras: low quality,
normal quality and high quality.


Reference::

  Z. Zhang, J. Yan, S. Lei, D. Yi, S. Z. Li: "A Face Antispoofing Database with Diverse Attacks", In proceedings of the 5th IAPR International Conference on Biometrics (ICB'12), New Delhi, India, 2012.


Installation
------------

Complete Bob's `installation`_ instructions. Then, to install this package,
run::

  $ conda install bob.db.casia_fasd


Contact
-------

For questions or reporting issues to this software package, contact our
development `mailing list`_.


.. Place your references here:
.. _bob: https://www.idiap.ch/software/bob
.. _installation: https://www.idiap.ch/software/bob/install
.. _mailing list: https://www.idiap.ch/software/bob/discuss
.. _casia fasd: http://www.cbsr.ia.ac.cn/english/FaceAntiSpoofDatabases.asp
