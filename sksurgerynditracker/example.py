#! /user/bin/python

#the configuration. 
#        "ip" : "169.254.60.146", this is what comes up via zero conf.
settings_vega={
        "tracker type": "vega",
        "ip address" : "192.168.2.17",
        "port" : 8765, 
        "romfiles" : [ "/home/thompson/src/ndicapi/Applications/8700339_smallblue-150130.rom" ,
            "../8700339.rom" ]
        }

settings_polaris={
        "tracker type": "polaris",
        "romfiles" : [ "/home/thompson/src/ndicapi/Applications/8700339_smallblue-150130.rom" ,
            "../8700339.rom" ]
        }

settings_aurora={
        "tracker type": "aurora",
        }

settings_dummy={
        "tracker type": "dummy",
        }

import nditracker
import time
import six

tracker=nditracker.ndiTracker()
tracker.Connect(settings_vega)

tracker.StartTracking()

six.print_ (tracker.GetToolDescriptionsAndPortHandles())
for _ in range (20):
    six.print_ (tracker.GetFrame())
    time.sleep(0.300333)

tracker.StopTracking()
tracker.Close()


