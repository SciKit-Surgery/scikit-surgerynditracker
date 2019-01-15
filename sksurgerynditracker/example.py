#! /user/bin/python

"""Brief example showing how to initialise, configure, and communicate
with NDI Polaris, Vega, and Aurora trackers."""

import time
import six
from sksurgerynditracker.nditracker import NDITracker

#configuration.
SETTINGS_VEGA = {
        "tracker type": "vega",
        "ip address" : "192.168.2.17",
        "port" : 8765,
        "romfiles" : [
            "../data/8700339_smallblue-150130.rom",
            "../data/8700339.rom"]
        }

SETTINGS_POLARIS = {
        "tracker type": "polaris",
        "romfiles" : [
            "../data/8700339_smallblue-150130.rom",
            "../data/8700339.rom"]
        }

SETTINGS_AURORA = {
        "tracker type": "aurora",
        }

SETTINGS_DUMMY = {
        "tracker type": "dummy",
        }

TRACKER = NDITracker()
TRACKER.connect(SETTINGS_VEGA)

TRACKER.start_tracking()

six.print_(TRACKER.get_tool_descriptions())
for _ in range(20):
    six.print_(TRACKER.get_frame())
    time.sleep(0.300333)

TRACKER.stop_tracking()
TRACKER.close()
