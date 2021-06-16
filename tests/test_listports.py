""" Lets see what com ports pyserial reports on our test runners"""

from serial.tools import list_ports #pylint: disable=import-error
from ndicapy import ndiDeviceName

def test_list_ports():
    """
    Check that ndicapy.ndiDeviceName gets all the comports found
    by pyserial
    """
    #list ports
    print([comport.device for comport in list_ports.comports()])

    serial_ports = list_ports.comports()

    ndi_port_names = []
    for port_number, _ in enumerate(serial_ports):
        ndi_port_names.append(ndiDeviceName(port_number))

    for serial_port in serial_ports:
        pyserial_port_name = serial_port.device
        print("Checking port:", pyserial_port_name, ndi_port_names)
        assert pyserial_port_name in ndi_port_names
