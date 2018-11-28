#! /user/bin/python

#the configuration. 
#        "ip" : "169.254.60.146", this is what comes up via zero conf.
settings={
        "tracker type": "vega",
        "ip address" : "192.168.2.17",
        "port" : 8765, 
        "romfiles" : [ "/home/thompson/src/ndicapi/Applications/8700339_smallblue-150130.rom" ]
        }

import nditracker
import time

tracker=nditracker.ndiTracker()
tracker.Connect(settings)
tracker.ReadSROMsFromFile()
tracker._InitialisePorts()
tracker._EnableTools()
tracker.StartTracking()
for _ in range (10):
    print (tracker.GetFrame())
    time.sleep(0.5)

tracker.Close()


