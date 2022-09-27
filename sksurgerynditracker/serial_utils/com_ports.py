"""Utilities to help deal with COM ports"""


def fix_com_port_greater_than_9(device_name):
    """
    Checks the device name. If it is a COM port
    returns the device name prepended with \\\\.\\
    see Microsoft KB115831.

    :param device_name: string device name
    :returns: if device name is COMXX returns \\\\.\\device_name
        otherwise returns device name
    """

    if device_name[0:3] != 'COM' or len(device_name) == 4:
        return device_name
    return '\\\\.\\' + device_name
