#! /user/bin/python

"""
Example showing how to initialise, configure, and communicate
with NDI Polaris, Vega, and Aurora trackers.
"""

import time
import six
from sksurgerynditracker.nditracker import NDITracker

def run():
    """Demonstration program

    Example showing how to initialise, configure, and communicate
    with NDI Polaris, Vega, and Aurora trackers.
    Configuration is by python dictionaries, edit as necessary.

    Dictionaries for other systems:

    settings_polaris = {"tracker type": "polaris",
    "romfiles" : ["../data/8700339.rom"]}

    settings_aurora = { "tracker type": "aurora",
    "ports to use" : [1,2]}

    settings_dummy = {"tracker type": "dummy",}

    """

    settings_vega = {
        "tracker type": "vega",
        "ip address" : "192.168.2.17",
        "port" : 8765,
        "romfiles" : [
            "../data/8700339.rom",
            "../data/something_else.rom"]
        }
    tracker = NDITracker(settings_vega)

    tracker.start_tracking()

    six.print_(tracker.get_tool_descriptions())
    for _ in range(20):
        six.print_(tracker.get_frame())
        time.sleep(0.300333)

    tracker.stop_tracking()
    tracker.close()
