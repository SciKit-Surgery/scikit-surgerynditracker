#  -*- coding: utf-8 -*-

"""Class implementing communication with NDI (Northern Digital) trackers"""

#there is some cut and paste from Doshkun's wherepy and from NifTKNDICapiTracker.*

#we can import generic tracker code from scikit-tracker, which isn't written yet.

from ndicapy import (ndiDeviceName, ndiProbe, ndiOpen, ndiClose,
                     ndiOpenNetwork, ndiCloseNetwork,
                     ndiGetPHSRNumberOfHandles, ndiGetPHRQHandle,
                     ndiPVWRFromFile,
                     ndiGetBXTransform,
                     ndiCommand, NDI_OKAY, ndiGetError, ndiErrorString,
                     ndiGetGXTransform, NDI_XFORMS_AND_STATUS,
                     NDI_115200, NDI_8N1, NDI_NOHANDSHAKE)

from six import ( print_, int2byte)


#where should we set things like this?
VIRTUAL_SROM_SIZE=1024
#THIS isn't necessary if we use ndicapy read from file function as that
#will pad it out to 1024 anyway
#so current niftk library
#reads sroms at contructor, then calls internal connect
#which calls enabletoolports

#this could be done with six.binary_type()
#if sys.version_info[0] >= 3:
#    def c_str(value):
#        """Convert passed value to a Python3-compatible
#        C-style string for use in NDI API functions.
#        """
#        return bytes(str(value), 'utf-8')
#else:
#    def c_str(value):
#        """Convert passed value to a Python2-compatible
#        C-style string for use in NDI API functions.
#        """
#        return str(value)

class ndiTracker:
    """For NDI trackers, hopefully will support Polaris, Aurora,
    and Vega, currently only tested with wireless tools on Vega
    """
    def __init__(self):
        """Create an instance ready for connecting."""
        #super(Tracker, self).__init__()
        self.device = None
        self.portHandles = None

    def Connect (self, ip , port ):
        self.device = ndiOpenNetwork(ip, port)
        if not self.device:
            raise IOError(
            'Could not connect to NDI device found on '
            '{}'.format(name))

        reply = ndiCommand(self.device, 'INIT:')
        error = ndiGetError(self.device)
        if  error != NDI_OKAY:
            raise IOError(
            'Error when sending command: '
            '{}'.format(ndiErrorString(error)))

    def Close (self):
        ndiCloseNetwork(self.device)

    def ReadSROMsFromFile (self,  sromFilenames ):
        #basically want to implement NDICapitracker::EnableToolPorts
        # // stop tracking
        #if (this->IsDeviceTracking) //this is an integer flag maintaned my m_Tracker. We can do that I guess.
        #let's not bother with it for now, see what sort of errors we get if we call TSTOP when not in tracking mode?
        #check whether there's a call to ndi.
        #other wise just do this
        self.StopTracking()

        #free ports that are waiting to be freed
        ndiCommand(self.device,'PHSR:01')
        numberOfTools=ndiGetPHSRNumberOfHandles(self.device)
        for toolIndex in range (numberOfTools):
            portHandle = ndiGetPHSRHandle(self.device,toolIndex)
            ndiCommand(self.device,"PHF:%02X",portHandle)
            self._CheckForErrors('freeing port handle {}.'.format(toolIndex))

        for sromfilename in sromFilenames:
            #no wired tools
            #get a port handle, there's a lot of wildcards in the
            #next PHRQ command?
            ndiCommand(self.device, 'PHRQ:*********1****')
            #not sure this is the python module
            portHandle = ndiGetPHRQHandle(self.device);

            print_("Loading  " , sromfilename, " to port handle ", portHandle);
            self._CheckForErrors('getting srom file port handle {}.'.format(portHandle))

            #this returns some sortof ndibit field? What do we do with it
            reply=ndiPVWRFromFile(self.device, portHandle, sromfilename)
            print_(reply)
            self._CheckForErrors('setting srom file port handle {}.'.format(portHandle))

        ndiCommand(self.device,'PHSR:01')
        numberOfTools=ndiGetPHSRNumberOfHandles(self.device)
        print_("Now there are " , numberOfTools, " on device")

    def _InitialisePorts (self):
        ndiCommand(self.device,'PHSR:02')
        numberOfTools=ndiGetPHSRNumberOfHandles(self.device)
        print_("Initialising " , numberOfTools, " on device")
        for toolIndex in range (numberOfTools):
            portHandle = ndiGetPHRQHandle(self.device)
            ndiCommand(self.device,"PINIT:%02X",portHandle)
            self._CheckForErrors('Initialising port handle {}.'.format(portHandle))

    def _EnableTools (self):
        ndiCommand(self.device,"PHSR:03")
        numberOfTools=ndiGetPHSRNumberOfHandles(self.device)
        print_("Enabling " , numberOfTools, " on device")
        for toolIndex in range (numberOfTools):
            portHandle = ndiGetPHRQHandle(self.device)
            #I think we can skip this bit for the minute, we're only
            #going to implement default mode
            #ndiCommand(self.device,"PHINF:%02X0001",portHandle)
            mode='D'
            print_("Enabling " , toolIndex);
            ndiCommand(self.device,"PENA:%02X%c",portHandle,mode);
            self._CheckForErrors('Enabling port handle {}.'.format(portHandle))

        ndiCommand(self.device,"PHSR:04")
        numberOfTools=ndiGetPHSRNumberOfHandles(self.device)
        print_("There are " , numberOfTools, " enabled tools on device")
        #we also need to initialise and enable !!

    def GetFrame (self):
        #TX - will get a frame in text format, not the most efficient
        #ndiCommand(self.device, "TX:0801")
        #BX does it in binary format, then there are a bunch of handy
        #helpers to convert to plain text.
        ndiCommand(self.device, "BX:0801")
        transform = None
        numberOfTools=ndiGetPHSRNumberOfHandles(self.device)
        portHandle = ndiGetPHRQHandle(self.device)
        print_( portHandle)
        return ndiGetBXTransform (self.device, int2byte(portHandle))
        #ndiGetBXFrame??
        #portnumber = 0;
        #ndiGetTXTransform (self.device, portnumber, transform)


    def StartTracking (self):
        ndiCommand(self.device, 'TSTART:')
        self._CheckForErrors('starting tracking.')

    def StopTracking (self):
        ndiCommand(self.device, 'TSTOP:')
        self._CheckForErrors('stopping tracking.')

    def _CheckForErrors ( self, message ):
        errnum = ndiGetError(self.device)
        if errnum != NDI_OKAY:
            ndiclose(self.device)
            raise ioerror('error when {}. the error'
            ' was: {}'.format(message,ndierrorstring(errnum)))


