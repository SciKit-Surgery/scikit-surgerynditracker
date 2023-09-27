# coding=utf-8

"""scikit-surgerynditracker mocks for polaris"""

from numpy import array, concatenate
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

class MockBXFrameSource():
    """
    A class to handle mocking of calls to get
    frame. Enables us to increment the frame number and return
    changing values
    """
    def __init__(self):
        self.bx_frame_count = 0
        self.rotation = array([0, 0, 0, 0])
        self.position = array([0, 0, 0])
        self.velocity = array([10, -20, 5])
        self.quality = array([1])

    def mockndiGetBXFrame(self, _device, _port_handle): #pylint:disable=invalid-name
        """Mock of ndiGetBXFrame"""
        self.bx_frame_count += 1

        return self.bx_frame_count

    def mockndiGetBXTransform(self, _device, _port_handle): #pylint:disable=invalid-name
        """
        Mock of ndiGetBXTransform. To enable a simple test of tracking
        smoothing translate the mock object between frames. Full testing of
        the averaging code is in the base class
        sksurgerycore.tests.algorithms
        """
        assert self.bx_frame_count > 0

        return concatenate((self.rotation, self.position, self.quality))

    def mockndiGetBXTransformMissing(self, _device, _port_handle): #pylint:disable=invalid-name
        """Mock of ndiGetBXTransform"""
        return "MISSING"
