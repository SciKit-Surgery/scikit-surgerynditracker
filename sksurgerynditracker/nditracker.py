#  -*- coding: utf-8 -*-

"""Class implementing communication with NDI (Northern Digital) trackers"""

from six import int2byte
from numpy import full, nan
from ndicapy import (ndiDeviceName, ndiProbe, ndiOpen, ndiClose,
                     ndiOpenNetwork, ndiCloseNetwork,
                     ndiGetPHSRNumberOfHandles, ndiGetPHRQHandle,
                     ndiPVWRFromFile,
                     ndiGetBXTransform,
                     ndiCommand, NDI_OKAY, ndiGetError, ndiErrorString,
                     NDI_115200, NDI_8N1, NDI_NOHANDSHAKE)


class NDITracker:
    """For NDI trackers, hopefully will support Polaris, Aurora,
    and Vega, currently only tested with wireless tools on Vega
    """
    def __init__(self):
        """Create an instance ready for connecting."""
        self.device = None
        self.tool_descriptors = []
        self.tracker_type = None
        self.ip_address = None
        self.port = None
        self.serial_port = None
        self.ports_to_probe = None

    def connect(self, configuration):
        """
        Initialises and attempts to connect to an NDI Tracker.

        :param configuration: A dictionary containing details of the
        tracker.
            tracker type: vega polaris aurora dummy
            ip address:
            port:
            romfiles:
            serial port:
        """
        self._configure(configuration)
        if self.tracker_type == "vega":
            self._connect_network()
        elif self.tracker_type == "aurora" or self.tracker_type == "polaris":
            self._connect_serial()

        if not self.device:
            raise IOError('Could not connect to NDI device found on ')

        ndiCommand(self.device, 'INIT:')
        self._check_for_errors('Sending INIT command')

        if self.tracker_type == "aurora" or self.tracker_type == "polaris":
            ndiCommand(self.device,
                       'COMM:{:d}{:03d}{:d}'
                       .format(NDI_115200, NDI_8N1, NDI_NOHANDSHAKE))

        self._read_sroms_from_file()
        self._initialise_ports()
        self._enable_tools()

    def _connect_network(self):
        self.device = ndiOpenNetwork(self.ip_address, self.port)

    def _connect_serial(self):
        if self.serial_port == -1:
            for port_no in range(self.ports_to_probe):
                name = ndiDeviceName(port_no)
                if not name:
                    continue
                result = ndiProbe(name)
                if result == NDI_OKAY:
                    break
        else:
            name = ndiDeviceName(self.serial_port)
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
                'group?)'.format(self.ports_to_probe))

        self.device = ndiOpen(name)

    def _configure(self, configuration):
        """ Reads a configuration dictionary
        describing the tracker configuration.
        and sets class variables.
        """
        if not "tracker type" in configuration:
            raise KeyError("Configuration must contain 'Tracker type'")

        tracker_type = configuration.get("tracker type")
        if tracker_type in ("vega", "polaris", "aurora", "dummy"):
            self.tracker_type = tracker_type
        else:
            raise ValueError(
                "Supported trackers are 'vega', 'aurora', 'polaris', "
                "and 'dummy'")

        if self.tracker_type == "vega":
            self._config_vega(configuration)

        if self.tracker_type == "polaris":
            self._config_polaris(configuration)

        if self.tracker_type == "aurora":
            self._config_aurora(configuration)

    def _config_vega(self, configuration):
        """
        Internal function to check configuration of a polaris vega
        """
        if not "ip address" in configuration:
            raise KeyError("Configuration for vega must contain"
                           "'ip address'")
        self.ip_address = configuration.get("ip address")
        if not "port" in configuration:
            self.port = 8765
        else:
            self.port = configuration.get("port")
        if "romfiles" not in configuration:
            raise KeyError("Configuration for vega and polaris must"
                           "contain a list of 'romfiles'")
        for romfile in configuration.get("romfiles"):
            self.tool_descriptors.append({"description" : romfile})

    def _config_polaris(self, configuration):
        """
        Internal function to check configuration for polaris vicra or spectra
        """
        if "romfiles" not in configuration:
            raise KeyError("Configuration for vega and polaris must"
                           "contain a list of 'romfiles'")
        for romfile in configuration.get("romfiles"):
            self.tool_descriptors.append({"description" : romfile})

        if "serial port" in configuration:
            self.serial_port = configuration.get("serial port")
        else:
            self.serial_port = -1

        if "number of ports to probe" in configuration:
            self.ports_to_probe = configuration.get("number of ports to probe")
        else:
            self.ports_to_probe = 20

    def _config_aurora(self, configuration):
        """
        Internal function to check configuration of an aurora
        """
        if "serial port" in configuration:
            self.serial_port = configuration.get("serial port")
        else:
            self.serial_port = -1

        if "number of ports to probe" in configuration:
            self.ports_to_probe = configuration.get("number of ports to probe")
        else:
            self.ports_to_probe = 20

    def close(self):
        """
        Closes the connection to the NDI Tracker.
        """
        if self.tracker_type == "vega":
            ndiCloseNetwork(self.device)
        else:
            ndiClose(self.device)

    def _read_sroms_from_file(self):
        self.stop_tracking()

        #free ports that are waiting to be freed
        ndiCommand(self.device, 'PHSR:01')
        number_of_tools = ndiGetPHSRNumberOfHandles(self.device)
        for tool_index in range(number_of_tools):
            port_handle = ndiGetPHRQHandle(self.device, tool_index)
            ndiCommand(self.device, "PHF:%02X", port_handle)
            self._check_for_errors('freeing port handle {}.'.format(tool_index))

        for tool in self.tool_descriptors:
            ndiCommand(self.device, 'PHRQ:*********1****')
            port_handle = ndiGetPHRQHandle(self.device)
            tool.update({"port handle" : port_handle})

            self._check_for_errors('getting srom file port handle {}.'
                                   .format(port_handle))

            ndiPVWRFromFile(self.device, port_handle,
                            tool.get("description"))
            self._check_for_errors('setting srom file port handle {}.'
                                   .format(port_handle))

        ndiCommand(self.device, 'PHSR:01')

    def _initialise_ports(self):
        ndiCommand(self.device, 'PHSR:02')
        for tool in self.tool_descriptors:
            ndiCommand(self.device, "PINIT:%02X", tool.get("port handle"))
            self._check_for_errors('Initialising port handle {}.'
                                   .format(tool.get("port handle")))

    def _enable_tools(self):
        ndiCommand(self.device, "PHSR:03")
        for tool in self.tool_descriptors:
            mode = 'D'
            ndiCommand(self.device, "PENA:%02X%c", tool.get("port handle"),
                       mode)
            self._check_for_errors('Enabling port handle {}.'
                                   .format(tool.get("port handle")))

        ndiCommand(self.device, "PHSR:04")

    def get_frame(self):
        """
        Get's a frame of tracking data from the NDI device.
        Each frame consists of a numpy array. The array has a
        separate row for each tracked rigid body. Each
        row contains:
            the port handle,
            3 columns for x,y,z coords,
            4 columns for the rotation as a quaternion.
            1 column containing the tracking quality.
        """
        #init a numpy array, it would be better if this inited NaN
        transforms = full((len(self.tool_descriptors), 9), nan)
        if not self.tracker_type == "dummy":
            ndiCommand(self.device, "BX:0801")

        for i in range(len(self.tool_descriptors)):
            transforms[i, 0] = self.tool_descriptors[i].get("port handle")
            transform = ndiGetBXTransform(self.device,
                                          int2byte(self.tool_descriptors[i]
                                                   .get("port handle")))
            if not transform == "MISSING" and not transform == "DISABLED":
                transforms[i, 1:9] = (transform)

        return transforms

    def get_tool_descriptions(self):
        """ Returns the port handles and tool descriptions """
        descriptions = full((len(self.tool_descriptors), 2), "empty",
                            dtype=object)
        for i in range(len(self.tool_descriptors)):
            descriptions[i, 0] = i
            descriptions[i, 1] = self.tool_descriptors[i].get("description")

        return descriptions

    def start_tracking(self):
        """ Tells the NDI devices to start tracking. """
        ndiCommand(self.device, 'TSTART:')
        self._check_for_errors('starting tracking.')

    def stop_tracking(self):
        """ Tells the NDI devices to stop tracking. """
        ndiCommand(self.device, 'TSTOP:')
        self._check_for_errors('stopping tracking.')

    def _check_for_errors(self, message):
        errnum = ndiGetError(self.device)
        if errnum != NDI_OKAY:
            ndiClose(self.device)
            raise IOError('error when {}. the error was: {}'
                          .format(message, ndiErrorString(errnum)))
