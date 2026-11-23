scikit-surgerynditracker
===============================

.. image:: https://github.com/SciKit-Surgery/scikit-surgerynditracker/raw/master/sksndi_logo.png
   :height: 128px
   :target: https://github.com/SciKit-Surgery/scikit-surgerynditracker
   :alt: Logo

|

.. image:: https://github.com/SciKit-Surgery/scikit-surgerynditracker/workflows/.github/workflows/ci.yml/badge.svg
   :target: https://github.com/SciKit-Surgery/scikit-surgerynditracker/actions/
   :alt: GitHub CI test status

.. image:: https://coveralls.io/repos/github/SciKit-Surgery/scikit-surgerynditracker/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/SciKit-Surgery/scikit-surgerynditracker?branch=master
    :alt: Test coverage

.. image:: https://readthedocs.org/projects/scikit-surgerynditracker/badge/?version=latest
    :target: http://scikit-surgerynditracker.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://img.shields.io/badge/Cite-SciKit--Surgery-informational
   :target: https://doi.org/10.1007/s11548-020-02180-5
   :alt: The SciKit-Surgery paper

.. image:: https://img.shields.io/twitter/follow/scikit_surgery?style=social
   :target: https://twitter.com/scikit_surgery?ref_src=twsrc%5Etfw
   :alt: Follow scikit_surgery on twitter

scikit-surgerynditracker is a python interface for Northern Digital (NDI) trackers. It should work with Polaris Vicra, Spectra, and Vega optical trackers and Aurora electromagnetic trackers. Tracking data is output as NumPy arrays.

Author: Stephen Thompson

scikit-surgerynditracker is part of the `SciKit-Surgery`_ software project, developed at the `Wellcome EPSRC Centre for Interventional and Surgical Sciences`_, part of `University College London (UCL)`_.


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

Offline simulator
-----------------

Install the separate ``ndicapi-sim`` package (from its checkout until it is
published), then select the additional ``simulator`` tracker type::

    from sksurgerynditracker.nditracker import NDITracker

    tracker = NDITracker({
        "tracker type": "simulator",
        "romfiles": ["pointer.rom", "reference.rom"],
        "simulation": {},
    })
    try:
        tracker.start_tracking()
        handles, timestamps, frames, poses, quality = tracker.get_frame()
    finally:
        tracker.close()

No hardware or ROM files are required. Default data follows a ten-second orbit
with per-tool radii of 100, 150, ... mm, Z around -1200 mm, rotating orientations,
and collective visibility toggling every four seconds. Set
``"visibility interval": 0`` for continuous visibility. ``"period"`` overrides
the orbit period in seconds. Existing smoothing and quaternion output options
still apply. ``dummy`` retains its existing empty/NaN behaviour.

An existing Polaris, Vega or Aurora configuration can be reused by changing
only ``"tracker type"``. The optional ``simulation`` dictionary overrides
defaults. Tool count and descriptions are inferred from ``romfiles`` without
reading or checking the files; an empty list means zero tools. Without a ROM
list, two named tools are generated. Set ``"simulation": {"tool count": 3}``
to override the count. Existing ROM descriptions are retained in order, and
extra tools receive generated names. Serial and network settings are accepted
but ignored by the simulator; common output and smoothing settings still apply.

``"simulation": {"mode": "playback", "file": "session.ndirec"}`` reserves
the future playback entry point and currently raises ``NotImplementedError``.
See the simulator package README for all configuration and timing details.
The optional ``simulator`` installation extra declares this dependency; native
tracker dependencies are unchanged.

The basic installation does not install or require the simulator. Selecting
``simulator`` without it raises an exception with an installation hint.
Once the simulator package is available on the package index, install both via
``pip install "scikit-surgerynditracker[simulator]"``.

Developing
----------

Cloning
^^^^^^^

You can clone the repository using the following command:

::

    git clone https://github.com/SciKit-Surgery/scikit-surgerynditracker


Running the tests
^^^^^^^^^^^^^^^^^

You can run the unit tests by installing and running tox:

::

    pip install tox
    tox

The base suite runs without ``ndicapi-sim``; only simulator integration cases
are skipped when it is absent. Missing-package guidance is always tested.
An installed but broken simulator is a test failure, not a skip. To enable
integration tests before the simulator is published, install its checkout::

    python -m pip install ../ndicapy-sim
    python -m pytest -q

The normal CI verifies a base installation with no simulator. The separate
``Optional simulator integration`` workflow is manually triggered with a
simulator repository and an accessible commit SHA or release tag. It installs
that source explicitly, requires a successful import, and runs both simulator
unit tests and tracker integration tests. Push the simulator commit before
requesting that workflow. This keeps the default CI independent of an
unpublished optional package.

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
.. _`source code repository`: https://github.com/SciKit-Surgery/scikit-surgerynditracker
.. _`Documentation`: https://scikit-surgerynditracker.readthedocs.io
.. _`SciKit-Surgery`: https://www.github.com/SciKit-Surgery
.. _`University College London (UCL)`: http://www.ucl.ac.uk/
.. _`Wellcome`: https://wellcome.ac.uk/
.. _`EPSRC`: https://www.epsrc.ac.uk/
.. _`contributing guidelines`: https://github.com/SciKit-Surgery/scikit-surgerynditracker/blob/master/CONTRIBUTING.rst
.. _`license file`: https://github.com/SciKit-Surgery/scikit-surgerynditracker/blob/master/LICENSE

