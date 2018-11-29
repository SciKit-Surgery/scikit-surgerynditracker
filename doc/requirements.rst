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
+------------+--------------------------------------------------------+-------------------------------------+
|    ID      |  Description                                           |  Test                               |
+============+========================================================+=====================================+
|    0000    |  Module has a help page                                |  pylint, see                        |
|            |                                                        |  tests/pylint.rc and tox.ini        |
+------------+--------------------------------------------------------+-------------------------------------+
|    0001    |  Functions are documented                              |  pylint, see                        |
|            |                                                        |  tests/pylint.rc and tox.ini        |
+------------+--------------------------------------------------------+-------------------------------------+
|    0002    |  Package has a version number                          |  No test yet, handled by git.       |
+------------+--------------------------------------------------------+-------------------------------------+
|    0003    |  Connects and configures, vega, polaris and aurora     |                                     |
+------------+--------------------------------------------------------+-------------------------------------+
|    0004    |  Configures via a python dictionary                    |                                     |
+------------+--------------------------------------------------------+-------------------------------------+
|    0005    |  Provides get frame to get frame of tracking data      |                                     |
+------------+--------------------------------------------------------+-------------------------------------+
|    0006    |  Get frame returns data as numpy array                 |                                     |
+------------+--------------------------------------------------------+-------------------------------------+
|    0007    |  Supports multiple tracked objects                     |                                     |
+------------+--------------------------------------------------------+-------------------------------------+
|    0008    |  Provides a method to stream data to file for later    |                                     |
|            |  use.                                                  |                                     |
+------------+--------------------------------------------------------+-------------------------------------+
|    0009    |  If no tracking available GetFrame Returns NaN         |                                     |
+------------+--------------------------------------------------------+-------------------------------------+




