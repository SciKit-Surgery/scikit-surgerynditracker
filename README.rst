scikit-surgerynditracker
===============================

.. image:: https://github.com/UCL/scikit-surgerynditracker/raw/master/project-icon.png
   :height: 128px
   :width: 128px
   :target: https://github.com/UCL/scikit-surgerynditracker

.. image:: https://github.com/UCL/scikit-surgerynditracker/workflows/.github/workflows/ci.yml/badge.svg
   :target: https://github.com/UCL/scikit-surgerynditracker/actions/
   :alt: GitHub CI test status

.. image:: https://coveralls.io/repos/github/UCL/scikit-surgerynditracker/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/UCL/scikit-surgerynditracker?branch=master
    :alt: Test coverage

.. image:: https://readthedocs.org/projects/scikit-surgerynditracker/badge/?version=latest
    :target: http://scikit-surgerynditracker.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status



scikit-surgerynditracker is a python interface for Northern Digital (NDI) trackers. It should work with Polaris Vicra, Spectra, and Vega optical trackers and Aurora electromagnetic trackers. Tracking data is output as NumPy arrays.

Author: Stephen Thompson

scikit-surgerynditracker is part of the `SNAPPY`_ software project, developed at the `Wellcome EPSRC Centre for Interventional and Surgical Sciences`_, part of `University College London (UCL)`_.


Installing
----------

::

    pip install scikit-surgerynditracker

Using
-----
Configuration is done using Python libraries at instantiation. Invalid
configuration should raise exceptions. Tracking data is returned in a set of
lists, containing the port handles, timestamps, framenumbers, the tracking data
and a tracking quality metric. By default tracking data is returned as a 4x4 NumPy array,
though can be returned as a quaternion by changing the configuration.

::

    from sksurgerynditracker.nditracker import NDITracker
    SETTINGS = {
        "tracker type": "polaris",
        "romfiles" : ["../data/8700339.rom"]
            }
    TRACKER = NDITracker(SETTINGS)

    TRACKER.start_tracking()
    port_handles, timestamps, framenumbers, tracking, quality = TRACKER.get_frame()
    for t in tracking:
      print (t)
    TRACKER.stop_tracking()
    TRACKER.close()

See demo.py for a full example

Developing
----------

Cloning
^^^^^^^

You can clone the repository using the following command:

::

    git clone https://github.com/UCL/SNAPPY/scikit-surgerynditracker


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
.. _`source code repository`: https://github.com/UCL/scikit-surgerynditracker
.. _`Documentation`: https://scikit-surgerynditracker.readthedocs.io
.. _`SNAPPY`: https://www.github.com/UCL/scikit-surgery/wikis/home
.. _`University College London (UCL)`: http://www.ucl.ac.uk/
.. _`Wellcome`: https://wellcome.ac.uk/
.. _`EPSRC`: https://www.epsrc.ac.uk/
.. _`contributing guidelines`: https://github.com/UCL/scikit-surgerynditracker/blob/master/CONTRIBUTING.rst
.. _`license file`: https://github.com/UCL/scikit-surgerynditracker/blob/master/LICENSE

