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

def mockndiGetPHSRHandle(_device, index): #pylint:disable=invalid-name
    """Mock of ndiGetPHSRHandle"""
    return int(index)

def mockndiVER(_device, _other_arg): #pylint:disable=invalid-name
    """Mock of ndiVER"""
    return 'Mock for Testing'

class MockNDIDevice():
    """
    A mock NDI device, enables us to keep track of how many tools we've added
    """
    def __init__(self):
        self.attached_tools = 0

    def mockndiCommand(self, _device, command): #pylint:disable=invalid-name
        """Mock a general command, strings over serial"""
        if command == "PHRQ:*********1****":
            self.attached_tools += 1

    def mockndiGetPHRQHandle(self, _device): #pylint:disable=invalid-name
        """Mock of ndiGetPHRQHandle"""
        return int(self.attached_tools - 1)

    def mockndiGetPHSRNumberOfHandles(self, _device): #pylint:disable=invalid-name
        """Mock of ndiGetPHSRNumberOfHandles"""
        return self.attached_tools


class MockBXFrameSource():
    """
    A class to handle mocking of calls to get
    frame. Enables us to increment the frame number and return
    changing values
    """
    def __init__(self):
        self.bx_frame_count = 0
        self.bx_call_count = 0
        self.rotation = array([0, 0, 0, 0])
        self.position = array([0, 0, 0])
        self.velocity = array([10, -20, 5])
        self.quality = array([1])
        self.tracked_tools = 0

    def setdevice(self, ndidevice):
        """
        We set an ndidevice so we know how many tracked objects to
        return
        """
        assert isinstance (ndidevice, MockNDIDevice)
        self.tracked_tools = ndidevice.attached_tools

    def mockndiGetBXFrame(self, _device, port_handle): #pylint:disable=invalid-name
        """Mock of ndiGetBXFrame"""
        self.bx_call_count += 1
        ph_int = int.from_bytes(port_handle, byteorder = 'little')
        if ph_int == 0:
            self.bx_frame_count += 1

        assert ph_int < self.tracked_tools
        if ph_int == self.tracked_tools - 1:
            assert self.bx_call_count == self.bx_frame_count * \
                    self.tracked_tools

        return self.bx_frame_count

    def mockndiGetBXTransform(self, _device, _port_handle): #pylint:disable=invalid-name
        """
        Mock of ndiGetBXTransform. To enable a simple test of tracking
        smoothing translate the mock object between frames. Full testing of
        the averaging code is in the base class
        sksurgerycore.tests.algorithms
        """
        assert self.bx_frame_count > 0
        #the base ndicapi library uses Py_BuildValue to return the transform
        #as a tuple of double float values, so let's make sure we're als
        #returning a tuple
        return tuple(concatenate((self.rotation, self.position, self.quality)))

    def mockndiGetBXTransformMissing(self, _device, _port_handle): #pylint:disable=invalid-name
        """Mock of ndiGetBXTransform"""
        return "MISSING"
