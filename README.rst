scikit-surgerynditracker
===============================

.. image:: https://weisslab.cs.ucl.ac.uk/WEISS/SoftwareRepositories/scikit-surgerynditracker/raw/master/project-icon.png
   :height: 128px
   :width: 128px
   :target: https://weisslab.cs.ucl.ac.uk/WEISS/SoftwareRepositories/scikit-surgerynditracker

.. image:: https://weisslab.cs.ucl.ac.uk/WEISS/SoftwareRepositories/scikit-surgerynditracker/badges/master/build.svg
   :target: https://weisslab.cs.ucl.ac.uk/WEISS/SoftwareRepositories/scikit-surgerynditracker/pipelines
   :alt: GitLab-CI test status

.. image:: https://weisslab.cs.ucl.ac.uk/WEISS/SoftwareRepositories/scikit-surgerynditracker/badges/master/coverage.svg
    :target: https://weisslab.cs.ucl.ac.uk/WEISS/SoftwareRepositories/scikit-surgerynditracker/commits/master
    :alt: Test coverage

.. image:: https://readthedocs.org/projects/scikit-surgerynditracker/badge/?version=latest
    :target: http://scikit-surgerynditracker.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status



scikit-surgerynditracker is a python interface for Northern Digital (NDI) trackers. It should work with Polaris Vicra, Spectra, and Vega optical trackers and Aurora electromagnetic trackers. Tracking data is output as NumPy arrays.

Author: Stephen Thompson

scikit-surgerynditracker is part of the `SNAPPY`_ software project, developed at the `Wellcome EPSRC Centre for Interventional and Surgical Sciences`_, part of `University College London (UCL)`_.


Installing
----------

You can pip install from PyPi or directly from the repository as follows:

::

    pip install git+https://weisslab.cs.ucl.ac.uk/WEISS/SoftwareRepositories/scikit-surgerynditracker

Using
-----
::
    from sksurgerynditracker.nditracker import NDITracker
    SETTINGS = {
        "tracker type": "polaris",
        "romfiles" : ["../data/8700339.rom"]
            }
    TRACKER = NDITracker()
    TRACKER.connect(SETTINGS)

    TRACKER.start_tracking()
    print(TRACKER.get_frame()
    TRACKER.stop_tracking()
    TRACKER.close()

See example.py for a full example

Developing
----------

Cloning
^^^^^^^

You can clone the repository using the following command:

::

    git clone https://weisslab.cs.ucl.ac.uk/WEISS/SoftwareRepositories/scikit-surgerynditracker


Running the tests
^^^^^^^^^^^^^^^^^

You can run the unit tests by installing and running tox:

::

    pip install tox
    tox

Contributing
^^^^^^^^^^^^

Please see the `contributing guidelines`_.


Useful links
^^^^^^^^^^^^

* `Source code repository`_
* `Documentation`_


Licensing and copyright
-----------------------

Copyright 2018 University College London.
scikit-surgerynditracker is released under the BSD-3 license. Please see the `license file`_ for details.


Acknowledgements
----------------

Supported by `Wellcome`_ and `EPSRC`_.


.. _`Wellcome EPSRC Centre for Interventional and Surgical Sciences`: http://www.ucl.ac.uk/weiss
.. _`source code repository`: https://weisslab.cs.ucl.ac.uk/WEISS/SoftwareRepositories/scikit-surgerynditracker
.. _`Documentation`: https://scikit-surgerynditracker.readthedocs.io
.. _`SNAPPY`: https://weisslab.cs.ucl.ac.uk/WEISS/PlatformManagement/SNAPPY/wikis/home
.. _`University College London (UCL)`: http://www.ucl.ac.uk/
.. _`Wellcome`: https://wellcome.ac.uk/
.. _`EPSRC`: https://www.epsrc.ac.uk/
.. _`contributing guidelines`: https://weisslab.cs.ucl.ac.uk/WEISS/SoftwareRepositories/scikit-surgerynditracker/blob/master/CONTRIBUTING.rst
.. _`license file`: https://weisslab.cs.ucl.ac.uk/WEISS/SoftwareRepositories/scikit-surgerynditracker/blob/master/LICENSE

