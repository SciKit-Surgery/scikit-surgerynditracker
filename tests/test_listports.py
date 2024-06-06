""" Lets see what com ports pyserial reports on our test runners"""

import sys
from serial.tools import list_ports  # pylint: disable=import-error
from ndicapy import ndiDeviceName


def test_list_ports():
    """
    Check that ndicapy.ndiDeviceName gets all the comports found
    by pyserial
    """
    print("List of available ports: ",
          [comport.device for comport in list_ports.comports()])

    serial_ports = list_ports.comports()

    ndi_port_names = []
    max_com_port = 0
    for port_number, serial_port in enumerate(serial_ports):
        ndi_port_names.append(ndiDeviceName(port_number))
        try:
            windows_port_number = int(serial_port.device.replace('COM', ''))
            max_com_port = max(max_com_port, windows_port_number)
        except ValueError:
            # we're probably not on windows, so don't care
            pass

    while len(ndi_port_names) < max_com_port:
        port_number = len(ndi_port_names)
        ndi_port_names.append(ndiDeviceName(port_number))

    for serial_port in serial_ports:
        pyserial_port_name = serial_port.device
        print("Checking port:", pyserial_port_name,
              "in ndi_port_names: ", ndi_port_names)
        if 'linux' not in sys.platform:
            assert pyserial_port_name in ndi_port_names
