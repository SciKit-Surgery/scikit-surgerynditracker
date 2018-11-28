#! /user/bin/python

#the configuration. 
#        "ip" : "169.254.60.146", this is what comes up via zero conf.
settings={
        "tracker type": "vega",
        "ip address" : "192.168.2.17",
        "port" : 8765, 
        "romfiles" : [ "/home/thompson/src/ndicapi/Applications/8700339_smallblue-150130.rom" ,
            "../8700339.rom" ]
        }

import nditracker
import time

tracker=nditracker.ndiTracker()
tracker.Connect(settings)

tracker.StartTracking()
for _ in range (1000):
    tracker.GetFrame()
    time.sleep(0.00333)

tracker.StopTracking()
tracker.Close()


