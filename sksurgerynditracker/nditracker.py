#  -*- coding: utf-8 -*-

"""Class implementing communication with NDI (Northern Digital) trackers"""

from ndicapy import (ndiDeviceName, ndiProbe, ndiOpen, ndiClose,
                     ndiOpenNetwork, ndiCloseNetwork,
                     ndiGetPHSRNumberOfHandles, ndiGetPHRQHandle,
                     ndiPVWRFromFile,
                     ndiGetBXTransform,
                     ndiCommand, NDI_OKAY, ndiGetError, ndiErrorString,
                     ndiGetGXTransform, NDI_XFORMS_AND_STATUS,
                     NDI_115200, NDI_8N1, NDI_NOHANDSHAKE)

from six import ( print_, int2byte)

class ndiTracker:
    """For NDI trackers, hopefully will support Polaris, Aurora,
    and Vega, currently only tested with wireless tools on Vega
    """
    def __init__(self):
        """Create an instance ready for connecting."""
        self.device = None
        self.toolDescriptors = []
        self.trackerType = None

    def Connect (self, configuration ):
        self._Configure( configuration )
        if self.trackerType == "vega":
            self.device = ndiOpenNetwork(self.ip_address, self.port)

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

    def _Configure(self, configuration):
        """ Reads a configuration dictionary
        describing the tracker configuration.
        and sets class variables.
        """
        if not "tracker type" in configuration:
            raise KeyError ( "Configuration must contain 'Tracker type'" )

        trackerType = configuration.get("tracker type")
        if trackerType == "vega" or trackerType == "polaris" or \
            trackerType == "aurora" or trackerType == "dummy":
            self.trackerType = trackerType
        else:
            raise ValueError ( "Supported trackers are 'vega', 'aurora', 'polaris', and 'dummy'" )

        if self.trackerType == "vega":
            if not "ip address" in configuration:
                raise KeyError ( "Configuration for vega must contain 'ip address'" )
            self.ip_address = configuration.get("ip address")
            if not "port" in configuration:
                self.port = 8765
            else:
                self.port = configuration.get("port")

        if self.trackerType == "vega" or self.trackerType == "polaris":
            if "romfiles" not in configuration:
                raise KeyError ( "Configuration for vega and polaris must contain a list of 'romfiles'" )
            for romfile in configuration.get("romfiles"):
                self.toolDescriptors.append( { "description" : romfile } )

        if self.trackerType == "aurora" or  self.trackerType == "polaris" or self.trackerType == "dummy":
            raise NotImplementedError ( " Polaris, aurora, and dummy not implemented yet")

    def Close (self):
        ndiCloseNetwork(self.device)

    def ReadSROMsFromFile (self):
        self.StopTracking()

        #free ports that are waiting to be freed
        ndiCommand(self.device,'PHSR:01')
        numberOfTools=ndiGetPHSRNumberOfHandles(self.device)
        for toolIndex in range (numberOfTools):
            portHandle = ndiGetPHRQHandle(self.device,toolIndex)
            ndiCommand(self.device,"PHF:%02X",portHandle)
            self._CheckForErrors('freeing port handle {}.'.format(toolIndex))

        for tool in self.toolDescriptors:
            ndiCommand(self.device, 'PHRQ:*********1****')
            portHandle = ndiGetPHRQHandle(self.device);
            tool.update ({ "portHandle" : portHandle } )

            self._CheckForErrors('getting srom file port handle {}.'.format(portHandle))

            reply=ndiPVWRFromFile(self.device, portHandle, tool.get("description"))
            self._CheckForErrors('setting srom file port handle {}.'.format(portHandle))

        ndiCommand(self.device,'PHSR:01')
        numberOfTools=ndiGetPHSRNumberOfHandles(self.device)
        print_("Now there are " , numberOfTools, " on device")

    def _InitialisePorts (self):
        ndiCommand(self.device,'PHSR:02')
        numberOfTools=ndiGetPHSRNumberOfHandles(self.device)
        for tool in self.toolDescriptors:
            ndiCommand(self.device,"PINIT:%02X",tool.get("portHandle"))
            self._CheckForErrors('Initialising port handle {}.'.format(tool.get("portHandle")))

    def _EnableTools (self):
        ndiCommand(self.device,"PHSR:03")
        numberOfTools=ndiGetPHSRNumberOfHandles(self.device)
        for tool in self.toolDescriptors:
            mode='D'
            ndiCommand(self.device,"PENA:%02X%c",tool.get("portHandle"),mode);
            self._CheckForErrors('Enabling port handle {}.'.format(tool.get("portHandle")))

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
        for tool in self.toolDescriptors:
            print_ ( tool.get("description"))
            print_ (ndiGetBXTransform (self.device, int2byte(tool.get("portHandle"))))
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


