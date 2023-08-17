# coding=utf-8

"""scikit-surgerynditracker mocks for polaris"""

import ndicapy

SETTINGS_POLARIS = {
    "tracker type": "polaris",
    "ports to probe": 20,
    "romfiles" : [
        "data/something_else.rom",
        "data/8700339.rom"]
    }

class MockPort:
    """A fake serial port for ndi"""
    device = 'bad port'

def mockndiProbe(port_name): #pylint:disable=invalid-name
    """Mock of ndiProbe"""
    if port_name == 'good port':
        return ndicapy.NDI_OKAY
    return ndicapy.NDI_PROBE_FAIL

def mockndiOpen(port_name): #pylint:disable=invalid-name
    """Mock of ndiOpen"""
    if port_name == 'good port':
        return True
    return False

def mockndiOpen_fail(port_name): #pylint:disable=invalid-name
    """Mock of ndiOpen that always fail"""
    if port_name == 'good port':
        return False
    return False

def mockndiGetError(_device): #pylint:disable=invalid-name
    """Mock of ndiGetError"""
    return ndicapy.NDI_OKAY

def mockComports(): #pylint:disable=invalid-name
    """Returns a list of mock comports"""
    mock_ports = [MockPort]*20
    mock_ports[5].device = 'good port'
    return mock_ports

def mockndiGetPHSRNumberOfHandles(_device): #pylint:disable=invalid-name
    """Mock of ndiGetPHSRNumberOfHandles"""
    return 4

def mockndiGetPHRQHandle(_device): #pylint:disable=invalid-name
    """Mock of ndiGetPHRQHandle"""
    return int(0)

def mockndiGetPHSRHandle(_device, index): #pylint:disable=invalid-name
    """Mock of ndiGetPHSRHandle"""
    return int(index)

def mockndiVER(_device, _other_arg): #pylint:disable=invalid-name
    """Mock of ndiVER"""
    return 'Mock for Testing'

def mockndiGetBXFrame(_device, _port_handle): #pylint:disable=invalid-name
    """Mock of ndiGetBXFrame"""
    bx_frame_count = 0
    return bx_frame_count

def mockndiGetBXTransform(_device, _port_handle): #pylint:disable=invalid-name
    """Mock of ndiGetBXTransform"""
    return [0,0,0,0,0,0,0,0]

def mockndiGetBXTransformMissing(_device, _port_handle): #pylint:disable=invalid-name
    """Mock of ndiGetBXTransform"""
    return "MISSING"
