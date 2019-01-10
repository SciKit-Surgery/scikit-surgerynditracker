#! /user/bin/python

"""Brief example showing how to initialise, configure, and communicate
with NDI Polaris, Vega, and Aurora trackers."""

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

import nditracker
import time
import six

tracker = nditracker.ndiTracker()
tracker.Connect(SETTINGS_VEGA)

tracker.StartTracking()

six.print_(tracker.GetToolDescriptionsAndPortHandles())
for _ in range(20):
    six.print_(tracker.GetFrame())
    time.sleep(0.300333)

tracker.StopTracking()
tracker.Close()
