#! /user/bin/python

"""Brief example showing how to initialise, configure, and communicate
with NDI Polaris, Vega, and Aurora trackers."""

import time
import six
import nditracker

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

TRACKER = nditracker.ndiTracker()
TRACKER.Connect(SETTINGS_VEGA)

TRACKER.StartTracking()

six.print_(TRACKER.GetToolDescriptionsAndPortHandles())
for _ in range(20):
    six.print_(TRACKER.GetFrame())
    time.sleep(0.300333)

TRACKER.StopTracking()
TRACKER.Close()
