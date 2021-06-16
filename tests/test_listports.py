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

    for port_number, serial_port in enumerate(serial_ports):
        pyserial_port_name = serial_port.device
        ndicapy_port_name = ndiDeviceName(port_number)
        print("Checking port:", pyserial_port_name, ndicapy_port_name)
        assert pyserial_port_name == ndicapy_port_name
