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

from six import int2byte
from numpy import full, nan

class ndiTracker:
    """For NDI trackers, hopefully will support Polaris, Aurora,
    and Vega, currently only tested with wireless tools on Vega
    """
    def __init__(self):
        """Create an instance ready for connecting."""
        self.device = None
        self.toolDescriptors = []
        self.trackerType = None

    def Connect(self, configuration):
        self._Configure(configuration)
        if self.trackerType == "vega":
            self._ConnectNetwork()
        elif self.trackerType == "aurora" or self.trackerType == "polaris":
            self._ConnectSerial()

        if not self.device:
            raise IOError('Could not connect to NDI device found on ')

        reply = ndiCommand(self.device, 'INIT:')
        self._CheckForErrors('Sending INIT command')

        if self.trackerType == "aurora" or self.trackerType == "polaris":
            ndiCommand(self.device,
                       'COMM:{:d}{:03d}{:d}'
                       .format(NDI_115200, NDI_8N1, NDI_NOHANDSHAKE))

        self._ReadSROMsFromFile()
        self._InitialisePorts()
        self._EnableTools()

    def _ConnectNetwork(self):
        self.device = ndiOpenNetwork(self.ip_address, self.port)

    def _ConnectSerial(self):
        if self.serialPort == -1:
            for port_no in range(self.portsToProbe):
                name = ndiDeviceName(port_no)
                if not name:
                    continue
                result = ndiProbe(name)
                if result == NDI_OKAY:
                    break
        else:
            name = ndiDeviceName(self.serialPort)
            result = ndiProbe(name)

        if result != NDI_OKAY:
            raise IOError(
                'Could not find any NDI device in '
                '{} serial port candidates checked. '
                'Please check the following:\n'
                '\t1) Is an NDI device connected to your computer?\n'
                '\t2) Is the NDI device switched on?\n'
                '\t3) Do you have sufficient privilege to connect to '
                'the device? (e.g. on Linux are you part of the "dialout" '
                'group?)'.format(self.portsToProbe))

        self.device = ndiOpen(name)

    def _Configure(self, configuration):
        """ Reads a configuration dictionary
        describing the tracker configuration.
        and sets class variables.
        """
        if not "tracker type" in configuration:
            raise KeyError("Configuration must contain 'Tracker type'")

        trackerType = configuration.get("tracker type")
        if trackerType == "vega" or trackerType == "polaris" or \
            trackerType == "aurora" or trackerType == "dummy":
            self.trackerType = trackerType
        else:
            raise ValueError(
                "Supported trackers are 'vega', 'aurora', 'polaris', "
                "and 'dummy'")

        if self.trackerType == "vega":
            if not "ip address" in configuration:
                raise KeyError("Configuration for vega must contain"
                               "'ip address'")
            self.ip_address = configuration.get("ip address")
            if not "port" in configuration:
                self.port = 8765
            else:
                self.port = configuration.get("port")

        if self.trackerType == "vega" or self.trackerType == "polaris":
            if "romfiles" not in configuration:
                raise KeyError("Configuration for vega and polaris must"
                               "contain a list of 'romfiles'")

        #read romfiles for all configurations, not sure what would happen
        #for aurora
        for romfile in configuration.get("romfiles"):
            self.toolDescriptors.append({"description" : romfile})

        #optional entries for serial port connections
        if "serial port" in configuration:
            self.serialport = configuration.get("serial port")
        else:
            self.serialport = -1

        if "number of ports to probe" in configuration:
            self.portsToProbe = configuration.get("number of ports to probe")
        else:
            self.portsToProbe = 20

        if self.trackerType == "aurora":
            raise NotImplementedError("Aurora not implemented yet.")

        if self.trackerType == "polaris":
            raise NotImplementedError("Polaris not implemented yet.")

        if self.trackerType == "dummy":
            raise NotImplementedError("Dummy not implemented yet.")

    def Close(self):
        if self.trackerType == "vega":
            ndiCloseNetwork(self.device)
        else:
            ndiClose(self.device)

    def _ReadSROMsFromFile(self):
        self.StopTracking()

        #free ports that are waiting to be freed
        ndiCommand(self.device, 'PHSR:01')
        numberOfTools = ndiGetPHSRNumberOfHandles(self.device)
        for toolIndex in range(numberOfTools):
            portHandle = ndiGetPHRQHandle(self.device, toolIndex)
            ndiCommand(self.device, "PHF:%02X", portHandle)
            self._CheckForErrors('freeing port handle {}.'.format(toolIndex))

        for tool in self.toolDescriptors:
            ndiCommand(self.device, 'PHRQ:*********1****')
            portHandle = ndiGetPHRQHandle(self.device)
            tool.update({"portHandle" : portHandle})

            self._CheckForErrors('getting srom file port handle {}.'.format(portHandle))

            reply = ndiPVWRFromFile(self.device, portHandle, tool.get("description"))
            self._CheckForErrors('setting srom file port handle {}.'.format(portHandle))

        ndiCommand(self.device, 'PHSR:01')
        numberOfTools = ndiGetPHSRNumberOfHandles(self.device)

    def _InitialisePorts(self):
        ndiCommand(self.device, 'PHSR:02')
        numberOfTools = ndiGetPHSRNumberOfHandles(self.device)
        for tool in self.toolDescriptors:
            ndiCommand(self.device, "PINIT:%02X", tool.get("portHandle"))
            self._CheckForErrors('Initialising port handle {}.'.format(tool.get("portHandle")))

    def _EnableTools(self):
        ndiCommand(self.device, "PHSR:03")
        numberOfTools = ndiGetPHSRNumberOfHandles(self.device)
        for tool in self.toolDescriptors:
            mode = 'D'
            ndiCommand(self.device, "PENA:%02X%c", tool.get("portHandle"), mode);
            self._CheckForErrors('Enabling port handle {}.'.format(tool.get("portHandle")))

        ndiCommand(self.device, "PHSR:04")
        numberOfTools = ndiGetPHSRNumberOfHandles(self.device)

    def GetFrame(self):
        #init a numpy array, it would be better if this inited NaN
        transforms= full((len(self.toolDescriptors), 9), nan)
        if not self.trackerType == "dummy":
            ndiCommand(self.device, "BX:0801")

        for i in range(len(self.toolDescriptors)):
            transforms[i, 0] = self.toolDescriptors[i].get("portHandle")
            transform = ndiGetBXTransform(self.device, int2byte(self.toolDescriptors[i].get("portHandle")))
            if not transform == "MISSING" and not transform == "DISABLED":
                transforms[i, 1:9] = (transform)

        return transforms

    def GetToolDescriptionsAndPortHandles(self):
        """ Returns the port handles and tool descriptions """
        descriptions = full((len(self.toolDescriptors), 2), "empty" ,  dtype = object)
        for i in range(len(self.toolDescriptors)):
            descriptions[i, 0] = i# self.toolDescriptors[i].get("portHandle")
            descriptions[i, 1] = self.toolDescriptors[i].get("description")

        return descriptions

    def StartTracking(self):
        ndiCommand(self.device, 'TSTART:')
        self._CheckForErrors('starting tracking.')

    def StopTracking(self):
        ndiCommand(self.device, 'TSTOP:')
        self._CheckForErrors('stopping tracking.')

    def _CheckForErrors(self, message):
        errnum = ndiGetError(self.device)
        if errnum != NDI_OKAY:
            ndiclose(self.device)
            raise ioerror('error when {}. the error'
            ' was: {}'.format(message, ndierrorstring(errnum)))


