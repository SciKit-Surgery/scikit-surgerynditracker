#  -*- coding: utf-8 -*-

"""Class implementing communication with NDI (Northern Digital) trackers"""

from platform import system
from subprocess import call
from time import time

from six import int2byte
from numpy import full, nan
from ndicapy import (ndiDeviceName, ndiProbe, ndiOpen, ndiClose,
                     ndiOpenNetwork, ndiCloseNetwork,
                     ndiGetPHSRNumberOfHandles, ndiGetPHRQHandle,
                     ndiPVWRFromFile,
                     ndiGetBXTransform, ndiGetBXFrame,
                     ndiCommand, NDI_OKAY, ndiGetError, ndiErrorString,
                     NDI_115200, NDI_8N1, NDI_NOHANDSHAKE)


class NDITracker:
    """
    Class for communication with NDI trackers.
    Should support Polaris, Aurora,
    and Vega. Currently only tested with wireless tools on Vega
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
        Creates an NDI tracker devices and connects to an NDI Tracker.

        :param configuration: A dictionary containing details of the tracker.

            tracker type: vega polaris aurora dummy

            ip address:

            port:

            romfiles:

            serial port:

        :raise Exception: IOError, KeyError
        """
        self._configure(configuration)
        if self.tracker_type == "vega":
            self._connect_vega()

        if self.tracker_type == "aurora":
            self._connect_aurora()

        if self.tracker_type == "polaris":
            self._connect_polaris()

        if self.tracker_type == "dummy":
            self.device = True

    def _connect_vega(self):
        self._connect_network()

        self._read_sroms_from_file()
        self._initialise_ports()
        self._enable_tools()

    def _connect_polaris(self):
        self._connect_serial()

        self._read_sroms_from_file()
        self._initialise_ports()
        self._enable_tools()

    def _connect_aurora(self):
        self._connect_serial()

    def _connect_network(self):
        #try and ping first to save time with timeouts
        param = '-n' if system().lower() == 'windows' else '-c'
        if call(['ping', param, '1', self.ip_address]) == 0:
            self.device = ndiOpenNetwork(self.ip_address, self.port)
        else:
            raise IOError('Could not find a device at {}'
                          .format(self.ip_address))
        if not self.device:
            raise IOError('Could not connect to network NDI device at {}'
                          .format(self.ip_address))

        ndiCommand(self.device, 'INIT:')
        self._check_for_errors('Sending INIT command')

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
        if not self.device:
            raise IOError('Could not connect to serial NDI device at {}'
                          .format(name))

        ndiCommand(self.device, 'INIT:')
        self._check_for_errors('Sending INIT command')
        ndiCommand(self.device,
                   'COMM:{:d}{:03d}{:d}'
                   .format(NDI_115200, NDI_8N1, NDI_NOHANDSHAKE))

    def _configure(self, configuration):
        """ Reads a configuration dictionary
        describing the tracker configuration.
        and sets class variables.

        raises: ValueError, KeyError
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

        if self.tracker_type == "dummy":
            self._config_dummy(configuration)

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

    def _config_dummy(self, configuration):
        """
        Internal function to check configuration of a testing dummy
        """
        if "romfiles" in configuration:
            for romfile in configuration.get("romfiles"):
                self.tool_descriptors.append({"description" : romfile})

    def close(self):
        """
        Closes the connection to the NDI Tracker and
        deletes the tracker device.

        :raise Exception: ValueError
        """
        if not self.device:
            raise ValueError('close called with no NDI device')

        if self.tracker_type == "vega":
            ndiCloseNetwork(self.device)

        if self.tracker_type in ("aurora", "polaris"):
            ndiClose(self.device)

        self.device = None

    def _read_sroms_from_file(self):
        if not self.device:
            raise ValueError('read srom called with no NDI device')

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
        if not self.device:
            raise ValueError('init ports called with no NDI device')

        ndiCommand(self.device, 'PHSR:02')
        for tool in self.tool_descriptors:
            ndiCommand(self.device, "PINIT:%02X", tool.get("port handle"))
            self._check_for_errors('Initialising port handle {}.'
                                   .format(tool.get("port handle")))

    def _enable_tools(self):
        if not self.device:
            raise ValueError('enable tools called with no NDI device')

        ndiCommand(self.device, "PHSR:03")
        for tool in self.tool_descriptors:
            mode = 'D'
            ndiCommand(self.device, "PENA:%02X%c", tool.get("port handle"),
                       mode)
            self._check_for_errors('Enabling port handle {}.'
                                   .format(tool.get("port handle")))

        ndiCommand(self.device, "PHSR:04")

    def get_frame(self):
        """Gets a frame of tracking data from the NDI device.

        :return: A NumPy array. One row per rigid body. Each row contains:

            0: the port handle,

            1: time stamp

            2: the NDI devices frame number

            3-5: x,y,z coords,

            6-9: the rotation as a quaternion.

            10: the tracking quality.

        Note: The time stamp is based on the host computer clock. Read the
        following extract from NDI's API Guide for advice on what to use:
        "Use the frame number, and not the host computer clock, to identify when
        data was collected. The frame number is incremented by 1 at a constant
        rate of 60 Hz. Associating a time from the host computer clock to
        replies from the system assumes that the duration of time between raw
        data collection and when the reply is received by the host computer is
        constant. This is not necessarily the case."
        """
        return_array = full((len(self.tool_descriptors), 11), nan)
        timestamp = time()
        if not self.tracker_type == "dummy":
            ndiCommand(self.device, "BX:0801")
            for i in range(len(self.tool_descriptors)):
                return_array[i, 0] = self.tool_descriptors[i].get("port handle")
                return_array[i, 1] = timestamp
                return_array[i, 2] = ndiGetBXFrame(
                    self.device, int2byte(
                        self.tool_descriptors[i].get("port handle")))
                transform = ndiGetBXTransform(self.device,
                                              int2byte(self.tool_descriptors[i]
                                                       .get("port handle")))
                if not transform == "MISSING" and not transform == "DISABLED":
                    return_array[i, 3:11] = (transform)
        else:
            for i in range(len(self.tool_descriptors)):
                return_array[i, 1] = timestamp

        return return_array

    def get_tool_descriptions(self):
        """ Returns the port handles and tool descriptions """
        descriptions = full((len(self.tool_descriptors), 2), "empty",
                            dtype=object)
        for i in range(len(self.tool_descriptors)):
            descriptions[i, 0] = i
            descriptions[i, 1] = self.tool_descriptors[i].get("description")

        return descriptions

    def start_tracking(self):
        """
        Tells the NDI devices to start tracking.
        :raise Exception: ValueError
        """
        ndiCommand(self.device, 'TSTART:')
        self._check_for_errors('starting tracking.')

    def stop_tracking(self):
        """
        Tells the NDI devices to stop tracking.
        :raise Exception: ValueError
        """
        ndiCommand(self.device, 'TSTOP:')
        self._check_for_errors('stopping tracking.')

    def _check_for_errors(self, message):
        errnum = ndiGetError(self.device)
        if errnum != NDI_OKAY:
            ndiClose(self.device)
            raise IOError('error when {}. the error was: {}'
                          .format(message, ndiErrorString(errnum)))
