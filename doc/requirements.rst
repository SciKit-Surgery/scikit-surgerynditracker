.. highlight:: shell

.. _requirements:

===============================================
Requirements for scikit-surgerynditracker
===============================================

This is the software requirements file for scikit-surgerynditracker, part of the
SNAPPY project. The requirements listed below should define
what scikit-surgerynditracker does. Each requirement can be matched to a unit test that
checks whether the requirement is met.

Requirements
~~~~~~~~~~~~
+----------+--------------------------------------------------------+-------------------------------------+
|  ID      |  Description                                           |  Test                               |
+==========+========================================================+=====================================+
|    00    |  Module has a help page                                |  pylint, see                        |
|          |                                                        |  tests/pylint.rc and tox.ini        |
+----------+--------------------------------------------------------+-------------------------------------+
|    01    |  Functions are documented                              |  pylint, see                        |
|          |                                                        |  tests/pylint.rc and tox.ini        |
+----------+--------------------------------------------------------+-------------------------------------+
|    02    |  Package has a version number                          |  handled by versioneer              |
+----------+--------------------------------------------------------+-------------------------------------+
|    03    |  Connects and configures, vega, polaris and aurora     |  test_configure                     |
+----------+--------------------------------------------------------+-------------------------------------+
|    04    |  Configures via a python dictionary                    |  test_configure                     |
+----------+--------------------------------------------------------+-------------------------------------+
|    05    |  Provides get frame to get frame of tracking data      |  test_get_frame                     |
+----------+--------------------------------------------------------+-------------------------------------+
|    06    |  Get frame returns data as numpy array                 |  test_get_frame                     |
+----------+--------------------------------------------------------+-------------------------------------+
|    07    |  Supports multiple tracked objects                     |  test_get_frame                     |
+----------+--------------------------------------------------------+-------------------------------------+
|    09    |  If no tracking available GetFrame Returns NaN         |  -                                  |
+----------+--------------------------------------------------------+-------------------------------------+




