#  -*- coding: utf-8 -*-

"""Class implementing communication with NDI (Northern Digital) trackers"""

from platform import system
from subprocess import call
from time import time

from six import int2byte
from numpy import full, nan
from ndicapy import (ndiDeviceName, ndiProbe, ndiOpen, ndiClose,
                     ndiOpenNetwork, ndiCloseNetwork,
                     ndiGetPHSRNumberOfHandles, ndiGetPHSRHandle,
                     ndiGetPHRQHandle, ndiPVWRFromFile,
                     ndiGetBXTransform, ndiGetBXFrame,
                     ndiGetTXTransform, ndiGetTXFrame,
                     ndiCommand, NDI_OKAY, ndiGetError, ndiErrorString,
                     NDI_115200, NDI_8N1, NDI_NOHANDSHAKE,
                     ndiVER)


class NDITracker:
    """
    Class for communication with NDI trackers.
    Should support Polaris, Aurora,
    and Vega. Currently only tested with wireless tools on Vega
    """
    def __init__(self):
        """Create an instance ready for connecting."""
        self._device = None
        self._tool_descriptors = []
        self._tracker_type = None
        self._ip_address = None
        self._port = None
        self._serial_port = None
        self._ports_to_probe = None
        self._device_firmware_version = None
        self._use_bx_transforms = None
        self._state = None

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
        if self._tracker_type == "vega":
            self._connect_vega()

        if self._tracker_type == "aurora":
            self._connect_aurora()

        if self._tracker_type == "polaris":
            self._connect_polaris()

        if self._tracker_type == "dummy":
            self._device = True

        self._initialise_ports()
        self._enable_tools()
        self._get_firmware_version()
        self._set_use_bx_transforms()
        self._state = 'ready'

    def _set_use_bx_transforms(self):
        """
        We'd like to use BX transforms as this sends binary
        tracking data, so should be faster, however for
        certain devices we can't do this. Here we check the
        firmware version and set _use_bx_transforms to suit.
        """
        self._use_bx_transforms = True
        if self._device_firmware_version == ' AURORA Rev 007':
            self._use_bx_transforms = False
            return
        if self._device_firmware_version == ' AURORA Rev 008':
            self._use_bx_transforms = False
            return
        return

    def _get_firmware_version(self):
        """
        Gets the device's firmware version, and sets
        self._device_firmware_version
        """

        self._device_firmware_version = 'unknown 00.0'

        if self._tracker_type != 'dummy':
            device_info = ndiVER(self._device, 0).split('\n')
            for line in device_info:
                if line.startswith('Freeze Tag:'):
                    self._device_firmware_version = line.split(':')[1]

    def _connect_vega(self):
        self._connect_network()
        self._read_sroms_from_file()

    def _connect_polaris(self):
        self._connect_serial()
        self._read_sroms_from_file()

    def _connect_aurora(self):
        self._connect_serial()
        self._find_wired_ports()

    def _connect_network(self):
        #try and ping first to save time with timeouts
        param = '-n' if system().lower() == 'windows' else '-c'
        if call(['ping', param, '1', self._ip_address]) == 0:
            self._device = ndiOpenNetwork(self._ip_address, self._port)
        else:
            raise IOError('Could not find a device at {}'
                          .format(self._ip_address))
        if not self._device:
            raise IOError('Could not connect to network NDI device at {}'
                          .format(self._ip_address))

        ndiCommand(self._device, 'INIT:')
        self._check_for_errors('Sending INIT command')

    def _connect_serial(self):
        if self._serial_port == -1:
            for port_no in range(self._ports_to_probe):
                name = ndiDeviceName(port_no)
                if not name:
                    continue
                result = ndiProbe(name)
                if result == NDI_OKAY:
                    break
        else:
            name = ndiDeviceName(self._serial_port)
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
                'group?)'.format(self._ports_to_probe))

        self._device = ndiOpen(name)
        if not self._device:
            raise IOError('Could not connect to serial NDI device at {}'
                          .format(name))

        ndiCommand(self._device, 'INIT:')
        self._check_for_errors('Sending INIT command')
        ndiCommand(self._device,
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
            self._tracker_type = tracker_type
        else:
            raise ValueError(
                "Supported trackers are 'vega', 'aurora', 'polaris', "
                "and 'dummy'")

        if self._tracker_type == "vega":
            self._config_vega(configuration)

        if self._tracker_type == "polaris":
            self._config_polaris(configuration)

        if self._tracker_type == "aurora":
            self._config_aurora(configuration)

        if self._tracker_type == "dummy":
            self._config_dummy(configuration)

    def _config_vega(self, configuration):
        """
        Internal function to check configuration of a polaris vega
        """
        if not "ip address" in configuration:
            raise KeyError("Configuration for vega must contain"
                           "'ip address'")
        self._ip_address = configuration.get("ip address")
        if not "port" in configuration:
            self._port = 8765
        else:
            self._port = configuration.get("port")
        if "romfiles" not in configuration:
            raise KeyError("Configuration for vega and polaris must"
                           "contain a list of 'romfiles'")
        for romfile in configuration.get("romfiles"):
            self._tool_descriptors.append({"description" : romfile})

    def _config_polaris(self, configuration):
        """
        Internal function to check configuration for polaris vicra or spectra
        """
        if "romfiles" not in configuration:
            raise KeyError("Configuration for vega and polaris must"
                           "contain a list of 'romfiles'")
        for romfile in configuration.get("romfiles"):
            self._tool_descriptors.append({"description" : romfile})

        if "serial port" in configuration:
            self._serial_port = configuration.get("serial port")
        else:
            self._serial_port = -1

        if "number of ports to probe" in configuration:
            self._ports_to_probe = configuration.get("number of ports to probe")
        else:
            self._ports_to_probe = 20

    def _config_aurora(self, configuration):
        """
        Internal function to check configuration of an aurora
        """
        if "serial port" in configuration:
            self._serial_port = configuration.get("serial port")
        else:
            self._serial_port = -1

        if "number of ports to probe" in configuration:
            self._ports_to_probe = configuration.get("number of ports to probe")
        else:
            self._ports_to_probe = 20

    def _config_dummy(self, configuration):
        """
        Internal function to check configuration of a testing dummy
        """
        if "romfiles" in configuration:
            for romfile in configuration.get("romfiles"):
                self._tool_descriptors.append({"description" : romfile})

    def close(self):
        """
        Closes the connection to the NDI Tracker and
        deletes the tracker device.

        :raise Exception: ValueError
        """
        if not self._device:
            raise ValueError('close called with no NDI device')

        if self._state == "tracking":
            self.stop_tracking()

        if self._tracker_type == "vega":
            ndiCloseNetwork(self._device)

        if self._tracker_type in ("aurora", "polaris"):
            ndiClose(self._device)

        self._device = None
        self._state = None

    def _read_sroms_from_file(self):
        if not self._device:
            raise ValueError('read srom called with no NDI device')

        self.stop_tracking()

        #free ports that are waiting to be freed
        ndiCommand(self._device, 'PHSR:01')
        number_of_tools = ndiGetPHSRNumberOfHandles(self._device)
        for tool_index in range(number_of_tools):
            port_handle = ndiGetPHRQHandle(self._device, tool_index)
            ndiCommand(self._device, "PHF:{0:02x}".format(port_handle))
            self._check_for_errors('freeing port handle {0:02x}.'
                                   .format(tool_index))

        for tool in self._tool_descriptors:
            ndiCommand(self._device, 'PHRQ:*********1****')
            port_handle = ndiGetPHRQHandle(self._device)
            tool.update({"port handle" : port_handle})
            if self._tracker_type == "vega":
                tool.update({"c_str port handle" : int2byte(port_handle)})
            else:
                tool.update({"c_str port handle" : str(port_handle).encode()})

            self._check_for_errors('getting srom file port handle {}.'
                                   .format(port_handle))

            ndiPVWRFromFile(self._device, port_handle,
                            tool.get("description"))
            self._check_for_errors('setting srom file port handle {}.'
                                   .format(port_handle))

        ndiCommand(self._device, 'PHSR:01')

    def _initialise_ports(self):
        """Initialises each port in the list of tool descriptors"""
        if not self._device:
            raise ValueError('init ports called with no NDI device')

        if not self._tracker_type == "dummy":
            ndiCommand(self._device, 'PHSR:02')
            for tool in self._tool_descriptors:
                ndiCommand(self._device, "PINIT:{0:02x}"
                           .format(tool.get("port handle")))
                self._check_for_errors('Initialising port handle {0:02x}.'
                                       .format(tool.get("port handle")))

    def _find_wired_ports(self):
        """For systems with wired tools, gets the number of tools plugged in
        and sticks them in the tool descriptors list"""
        if not self._device:
            raise ValueError('find wired ports called with no NDI device')

        ndiCommand(self._device, 'PHSR:02')
        number_of_tools = ndiGetPHSRNumberOfHandles(self._device)
        while number_of_tools > 0:
            for ndi_tool_index in range(number_of_tools):
                port_handle = ndiGetPHSRHandle(self._device, ndi_tool_index)

                self._tool_descriptors.append({"description" : ndi_tool_index,
                                               "port handle" : port_handle,
                                               "c_str port handle" :
                                               int2byte(port_handle)})
                ndiCommand(self._device, "PINIT:{0:02x}".format(port_handle))
            ndiCommand(self._device, 'PHSR:02')
            number_of_tools = ndiGetPHSRNumberOfHandles(self._device)

    def _enable_tools(self):
        if not self._device:
            raise ValueError('enable tools called with no NDI device')

        if not self._tracker_type == "dummy":
            ndiCommand(self._device, "PHSR:03")
            number_of_tools = ndiGetPHSRNumberOfHandles(self._device)
            for tool_index in range(number_of_tools):
                port_handle = ndiGetPHSRHandle(self._device, tool_index)
                port_handle_already_present = False
                for tool in self._tool_descriptors:
                    if tool.get("port handle") == port_handle:
                        port_handle_already_present = True
                        break
                if not port_handle_already_present:
                    self._tool_descriptors.append({
                        "description" : tool_index,
                        "port handle" : port_handle,
                        "c_str port handle" :
                        int2byte(port_handle)})

                mode = 'D'
                ndiCommand(self._device, "PENA:{0:02x}{1}"
                           .format(port_handle, mode))
                self._check_for_errors('Enabling port handle {}.'
                                       .format(port_handle))

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
        if self._use_bx_transforms:
            frame = self._get_frame_bx()
        else:
            frame = self._get_frame_tx()

        return frame

    def _get_frame_bx(self):
        return_array = full((len(self._tool_descriptors), 11), nan)
        timestamp = time()
        if not self._tracker_type == "dummy":
            ndiCommand(self._device, "BX:0801")
            for i in range(len(self._tool_descriptors)):
                return_array[i, 0] = self._tool_descriptors[i].get(
                    "port handle")
                return_array[i, 1] = timestamp
                return_array[i, 2] = ndiGetBXFrame(
                    self._device,
                    self._tool_descriptors[i].get("c_str port handle"))
                transform = ndiGetBXTransform(
                    self._device,
                    self._tool_descriptors[i].get("c_str port handle"))
                if not transform == "MISSING" and not transform == "DISABLED":
                    return_array[i, 3:11] = (transform)
        else:
            for i in range(len(self._tool_descriptors)):
                return_array[i, 1] = timestamp

        return return_array

    def _get_frame_tx(self):
        return_array = full((len(self._tool_descriptors), 11), nan)
        timestamp = time()
        if not self._tracker_type == "dummy":
            ndiCommand(self._device, "TX:0801")
            for i in range(len(self._tool_descriptors)):
                return_array[i, 0] = self._tool_descriptors[i].get(
                    "port handle")
                return_array[i, 1] = timestamp
                return_array[i, 2] = ndiGetTXFrame(
                    self._device,
                    self._tool_descriptors[i].get("c_str port handle"))
                transform = ndiGetTXTransform(
                    self._device,
                    self._tool_descriptors[i].get("c_str port handle"))
                if not transform == "MISSING" and not transform == "DISABLED":
                    return_array[i, 3:11] = (transform)
        else:
            for i in range(len(self._tool_descriptors)):
                return_array[i, 1] = timestamp

        return return_array

    def get_tool_descriptions(self):
        """ Returns the port handles and tool descriptions """
        descriptions = full((len(self._tool_descriptors), 2), "empty",
                            dtype=object)
        for i in range(len(self._tool_descriptors)):
            descriptions[i, 0] = i
            descriptions[i, 1] = self._tool_descriptors[i].get("description")

        return descriptions

    def start_tracking(self):
        """
        Tells the NDI devices to start tracking.
        :raise Exception: ValueError
        """
        if self._state != 'ready':
            raise ValueError("""Called start tracking before device ready,
            try calling connect first""")

        ndiCommand(self._device, 'TSTART:')
        self._check_for_errors('starting tracking.')
        self._state = 'tracking'

    def stop_tracking(self):
        """
        Tells the NDI devices to stop tracking.
        :raise Exception: ValueError
        """
        ndiCommand(self._device, 'TSTOP:')
        self._check_for_errors('stopping tracking.')
        self._state = 'ready'

    def _check_for_errors(self, message):
        errnum = ndiGetError(self._device)
        if errnum != NDI_OKAY:
            ndiClose(self._device)
            raise IOError('error when {}. the error was: {}'
                          .format(message, ndiErrorString(errnum)))
