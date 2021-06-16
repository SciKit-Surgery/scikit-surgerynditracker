""" Lets see what com ports pyserial reports on our test runners"""

from serial.tools import list_ports #pylint: disable=import-error

def test_list_ports():
    """ What serial ports do we have """
    print([comport.device for comport in list_ports.comports()])
