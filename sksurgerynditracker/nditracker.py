#  -*- coding: utf-8 -*-

"""Class implementing communication with NDI (Northern Digital) trackers"""

from platform import system
from subprocess import call
from time import time

from six import int2byte
from numpy import full, nan, reshape, transpose
import ndicapy

def _check_config_aurora(configuration):
    """
    Internal function to check configuration of an aurora
    """
    if "serial port" not in configuration:
        configuration.update({"serial port": -1})

    if "number of ports to probe" not in configuration:
        configuration.update({"ports to probe" : 20})


class NDITracker:
    """
    Class for communication with NDI trackers.
    Should support Polaris, Aurora,
    and Vega. Currently only tested with wireless tools on Vega
    """
    def __init__(self, configuration):
        """
        Creates an NDI tracker devices and connects to an NDI Tracker.

        :param configuration: A dictionary containing details of the tracker.

            tracker type: vega polaris aurora dummy

            ip address:

            port:

            romfiles:

            serial port:

            ports to probe:

        :raises Exception: IOError, KeyError, OSError
        """
        self._device = None
        self._tool_descriptors = []
        self._tracker_type = None
        self._state = None
        self._use_quaternions = None

        self._get_frame = None
        self._get_transform = None
        self._capture_string = None

        self._configure(configuration)
        if self._tracker_type == "vega":
            self._connect_vega(configuration)

        if self._tracker_type == "aurora":
            self._connect_aurora(configuration)

        if self._tracker_type == "polaris":
            self._connect_polaris(configuration)

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
        self._get_frame = getattr(ndicapy, 'ndiGetBXFrame')
        self._get_transform = getattr(ndicapy, 'ndiGetBXTransform')
        self._capture_string = 'BX:0801'

        firmware = self._get_firmware_version()
        if firmware in (' AURORA Rev 007', ' AURORA Rev 008'):
            self._get_frame = getattr(ndicapy, 'ndiGetTXFrame')
            self._get_transform = getattr(ndicapy, 'ndiGetTXTransform')
            self._capture_string = 'TX:0801'

    def _get_firmware_version(self):
        """
        Gets the device's firmware version, and sets
        self._device_firmware_version
        """

        device_firmware_version = 'unknown 00.0'

        if self._tracker_type != 'dummy':
            device_info = ndicapy.ndiVER(self._device, 0).split('\n')
            for line in device_info:
                if line.startswith('Freeze Tag:'):
                    device_firmware_version = line.split(':')[1]
        return device_firmware_version

    def _connect_vega(self, configuration):
        self._connect_network(configuration)
        self._read_sroms_from_file()

    def _connect_polaris(self, configuration):
        self._connect_serial(configuration)
        self._read_sroms_from_file()

    def _connect_aurora(self, configuration):
        self._connect_serial(configuration)
        self._find_wired_ports()

    def _connect_network(self, configuration):
        #try and ping first to save time with timeouts
        param = '-n' if system().lower() == 'windows' else '-c'
        ip_address = configuration.get("ip address")
        port = configuration.get("port")
        if call(['ping', param, '1', ip_address]) == 0:
            self._device = ndicapy.ndiOpenNetwork(ip_address, port)
        else:
            raise IOError('Could not find a device at {}'
                          .format(ip_address))
        if not self._device:
            raise IOError('Could not connect to network NDI device at {}'
                          .format(ip_address))

        ndicapy.ndiCommand(self._device, 'INIT:')
        self._check_for_errors('Sending INIT command')

    def _connect_serial(self, configuration):
        serial_port = configuration.get("serial port")
        ports_to_probe = configuration.get("ports to probe")
        if serial_port == -1:
            for port_no in range(ports_to_probe):
                name = ndicapy.ndiDeviceName(port_no)
                if not name:
                    continue
                result = ndicapy.ndiProbe(name)
                if result == ndicapy.NDI_OKAY:
                    break
        else:
            name = ndicapy.ndiDeviceName(serial_port)
            result = ndicapy.ndiProbe(name)

        if result != ndicapy.NDI_OKAY:
            raise IOError(
                'Could not find any NDI device in '
                '{} serial port candidates checked. '
                'Please check the following:\n'
                '\t1) Is an NDI device connected to your computer?\n'
                '\t2) Is the NDI device switched on?\n'
                '\t3) Do you have sufficient privilege to connect to '
                'the device? (e.g. on Linux are you part of the "dialout" '
                'group?)'.format(ports_to_probe))

        self._device = ndicapy.ndiOpen(name)
        if not self._device:
            raise IOError('Could not connect to serial NDI device at {}'
                          .format(name))

        ndicapy.ndiCommand(self._device, 'INIT:')
        self._check_for_errors('Sending INIT command')
        ndicapy.ndiCommand(self._device,
                           'COMM:{:d}{:03d}{:d}'
                           .format(ndicapy.NDI_115200, ndicapy.NDI_8N1,
                                   ndicapy.NDI_NOHANDSHAKE))

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
            self._check_config_vega(configuration)

        if self._tracker_type == "polaris":
            self._check_config_polaris(configuration)

        if self._tracker_type == "aurora":
            _check_config_aurora(configuration)

        if self._tracker_type == "dummy":
            self._check_config_dummy(configuration)

        if "use quaternions" in configuration:
            self._use_quaternions = configuration.get("use quaternions")
        else:
            self._use_quaternions = False

    def _check_config_vega(self, configuration):
        """
        Internal function to check configuration of a polaris vega
        """
        if not "ip address" in configuration:
            raise KeyError("Configuration for vega must contain"
                           "'ip address'")
        if not "port" in configuration:
            configuration.update({"port":8765})

        if "romfiles" not in configuration:
            raise KeyError("Configuration for vega and polaris must"
                           "contain a list of 'romfiles'")
        for romfile in configuration.get("romfiles"):
            self._tool_descriptors.append({"description" : romfile})

    def _check_config_polaris(self, configuration):
        """
        Internal function to check configuration for polaris vicra or spectra
        """
        if "romfiles" not in configuration:
            raise KeyError("Configuration for vega and polaris must"
                           "contain a list of 'romfiles'")
        for romfile in configuration.get("romfiles"):
            self._tool_descriptors.append({"description" : romfile})

        if "serial port" not in configuration:
            configuration.update({"serial port": -1})

        if "number of ports to probe" not in configuration:
            configuration.update({"ports to probe" : 20})

    def _check_config_dummy(self, configuration):
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

        :raises Exception: ValueError
        """
        if not self._device:
            raise ValueError('close called with no NDI device')

        if self._state == "tracking":
            self.stop_tracking()

        if self._tracker_type == "vega":
            ndicapy.ndiCloseNetwork(self._device)

        if self._tracker_type in ("aurora", "polaris"):
            ndicapy.ndiClose(self._device)

        self._device = None
        self._state = None

    def _read_sroms_from_file(self):
        if not self._device:
            raise ValueError('read srom called with no NDI device')

        self.stop_tracking()

        #free ports that are waiting to be freed
        ndicapy.ndiCommand(self._device, 'PHSR:01')
        number_of_tools = ndicapy.ndiGetPHSRNumberOfHandles(self._device)
        for tool_index in range(number_of_tools):
            port_handle = ndicapy.ndiGetPHRQHandle(self._device, tool_index)
            ndicapy.ndiCommand(self._device, "PHF:{0:02x}".format(port_handle))
            self._check_for_errors('freeing port handle {0:02x}.'
                                   .format(tool_index))

        for tool in self._tool_descriptors:
            ndicapy.ndiCommand(self._device, 'PHRQ:*********1****')
            port_handle = ndicapy.ndiGetPHRQHandle(self._device)
            tool.update({"port handle" : port_handle})
            if self._tracker_type == "vega":
                tool.update({"c_str port handle" : int2byte(port_handle)})
            else:
                tool.update({"c_str port handle" : str(port_handle).encode()})

            self._check_for_errors('getting srom file port handle {}.'
                                   .format(port_handle))

            ndicapy.ndiPVWRFromFile(self._device, port_handle,
                                    tool.get("description"))
            self._check_for_errors('setting srom file port handle {}.'
                                   .format(port_handle))

        ndicapy.ndiCommand(self._device, 'PHSR:01')

    def _initialise_ports(self):
        """Initialises each port in the list of tool descriptors"""
        if not self._device:
            raise ValueError('init ports called with no NDI device')

        if not self._tracker_type == "dummy":
            ndicapy.ndiCommand(self._device, 'PHSR:02')
            for tool in self._tool_descriptors:
                ndicapy.ndiCommand(self._device, "PINIT:{0:02x}"
                                   .format(tool.get("port handle")))
                self._check_for_errors('Initialising port handle {0:02x}.'
                                       .format(tool.get("port handle")))

    def _find_wired_ports(self):
        """For systems with wired tools, gets the number of tools plugged in
        and sticks them in the tool descriptors list"""
        if not self._device:
            raise ValueError('find wired ports called with no NDI device')

        ndicapy.ndiCommand(self._device, 'PHSR:02')
        number_of_tools = ndicapy.ndiGetPHSRNumberOfHandles(self._device)
        while number_of_tools > 0:
            for ndi_tool_index in range(number_of_tools):
                port_handle = ndicapy.ndiGetPHSRHandle(self._device,
                                                       ndi_tool_index)

                self._tool_descriptors.append({"description" : ndi_tool_index,
                                               "port handle" : port_handle,
                                               "c_str port handle" :
                                               int2byte(port_handle)})
                ndicapy.ndiCommand(self._device,
                                   "PINIT:{0:02x}".format(port_handle))
            ndicapy.ndiCommand(self._device, 'PHSR:02')
            number_of_tools = ndicapy.ndiGetPHSRNumberOfHandles(self._device)

    def _enable_tools(self):
        if not self._device:
            raise ValueError('enable tools called with no NDI device')

        if not self._tracker_type == "dummy":
            ndicapy.ndiCommand(self._device, "PHSR:03")
            number_of_tools = ndicapy.ndiGetPHSRNumberOfHandles(self._device)
            for tool_index in range(number_of_tools):
                port_handle = ndicapy.ndiGetPHSRHandle(self._device, tool_index)
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
                ndicapy.ndiCommand(self._device, "PENA:{0:02x}{1}"
                                   .format(port_handle, mode))
                self._check_for_errors('Enabling port handle {}.'
                                       .format(port_handle))

    def get_frame(self):
        """Gets a frame of tracking data from the NDI device.

        :return:

            port_numbers : list of port handles, one per tool

            time_stamps : list of timestamps (cpu clock), one per tool

            frame_numbers : list of framenumbers (tracker clock) one per tool

            tracking : list of 4x4 tracking matrices, rotation and position,
            or if use_quaternions is true, a list of tracking quaternions,
            column 0-2 is x,y,z column 3-6 is the rotation as a quaternion.

            tracking_quality : list the tracking quality, one per tool.

        Note: The time stamp is based on the host computer clock. Read the
        following extract from NDI's API Guide for advice on what to use:
        "Use the frame number, and not the host computer clock, to identify when
        data was collected. The frame number is incremented by 1 at a constant
        rate of 60 Hz. Associating a time from the host computer clock to
        replies from the system assumes that the duration of time between raw
        data collection and when the reply is received by the host computer is
        constant. This is not necessarily the case."
        """
        port_handles = []
        time_stamps = []
        frame_numbers = []
        tracking = []
        tracking_quality = []

        timestamp = time()
        if not self._tracker_type == "dummy":
            ndicapy.ndiCommand(self._device, self._capture_string)
            for i in range(len(self._tool_descriptors)):
                port_handles.append(self._tool_descriptors[i].get(
                    "port handle"))
                time_stamps.append(timestamp)
                frame_numbers.append(self._get_frame(
                    self._device,
                    self._tool_descriptors[i].get("c_str port handle")))
                qtransform = self._get_transform(
                    self._device,
                    self._tool_descriptors[i].get("c_str port handle"))
                if not qtransform == "MISSING" and not qtransform == "DISABLED":
                    tracking_quality.append(qtransform[7])
                    if not self._use_quaternions:
                        transform = transpose(
                            reshape(ndicapy.ndiTransformToMatrixd(qtransform),
                                    [4, 4]))
                    else:
                        transform = reshape(qtransform[0:7], [1, 7])
                else:
                    tracking_quality.append(nan)
                    if not self._use_quaternions:
                        transform = full((4, 4), nan)
                    else:
                        transform = full((1, 7), nan)

                tracking.append(transform)

        else:
            for i in range(len(self._tool_descriptors)):
                port_handles.append(self._tool_descriptors[i].get(
                    "port handle"))
                time_stamps.append(timestamp)
                frame_numbers.append(0)
                tracking_quality.append(0.0)
                if not self._use_quaternions:
                    tracking.append(full((4, 4), nan))
                else:
                    tracking.append(full((1, 7), nan))

        return port_handles, time_stamps, frame_numbers, tracking, \
                tracking_quality

    def get_tool_descriptions(self):
        """ Returns the port handles and tool descriptions """
        port_handles = []
        descriptions = []
        for i in range(len(self._tool_descriptors)):
            port_handles.append(self._tool_descriptors[i].get("port handle"))
            descriptions.append(self._tool_descriptors[i].get("description"))

        return port_handles, descriptions

    def start_tracking(self):
        """
        Tells the NDI devices to start tracking.
        :raises Exception: ValueError
        """
        if self._state != 'ready':
            raise ValueError("""Called start tracking before device ready,
            try calling connect first""")

        ndicapy.ndiCommand(self._device, 'TSTART:')
        self._check_for_errors('starting tracking.')
        self._state = 'tracking'

    def stop_tracking(self):
        """
        Tells the NDI devices to stop tracking.
        :raises Exception: ValueError
        """
        ndicapy.ndiCommand(self._device, 'TSTOP:')
        self._check_for_errors('stopping tracking.')
        self._state = 'ready'

    def _check_for_errors(self, message):
        errnum = ndicapy.ndiGetError(self._device)
        if errnum != ndicapy.NDI_OKAY:
            ndicapy.ndiClose(self._device)
            raise IOError('error when {}. the error was: {}'
                          .format(message, ndicapy.ndiErrorString(errnum)))
