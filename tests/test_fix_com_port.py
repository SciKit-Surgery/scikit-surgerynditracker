""" Lets see what com ports pyserial reports on our test runners"""

import sksurgerynditracker.serial_utils.com_ports as cp

def test_fix_com_port():
    """
    Test that fix_com_port_greater_than_9 prepends the
    relevant ports
    """

    assert cp.fix_com_port_greater_than_9('COM1') == 'COM1'
    assert cp.fix_com_port_greater_than_9('/dev/ttyS31') == '/dev/ttyS31'
    assert cp.fix_com_port_greater_than_9('COM10') == '\\\\.\\COM10'
