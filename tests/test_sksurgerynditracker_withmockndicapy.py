# coding=utf-8

"""scikit-surgerynditracker tests using a mocked ndicapy"""
import ndicapy
from sksurgerynditracker.nditracker import NDITracker

#configuration.
SETTINGS_VEGA = {
    "tracker type": "vega",
    "ip address" : "999.999.999.999",
    "port" : 8765,
    "romfiles" : [
        "data/something_else.rom",
        "data/8700339.rom"]
    }

SETTINGS_POLARIS = {
    "tracker type": "polaris",
    "ports to probe": 20,
    "romfiles" : [
        "data/something_else.rom",
        "data/8700339.rom"]
    }

SETTINGS_AURORA = {
    "tracker type": "aurora"
    }

SETTINGS_DUMMY = {
    "tracker type": "dummy",
    }

SETTINGS_DUMMY_QUATERNIONS = {
    "tracker type": "dummy",
    "use quaternions": True
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

def mockndiGetPHRQHandle(_device, index=0): #pylint:disable=invalid-name
    """Mock of ndiGetPHRQHandle"""
    return int(index)

def mockndiGetPHSRHandle(_device, index): #pylint:disable=invalid-name
    """Mock of ndiGetPHSRHandle"""
    return int(index)

def mockndiVER(_device, _other_arg): #pylint:disable=invalid-name
    """Mock of ndiVER"""
    return 'Mock for Testing'

def test_connect_serial_mock(mocker):
    """
    connects and configures, mocks ndicapy.ndiProbe to pass
    reqs: 03, 04
    """
    tracker = None
    mocker.patch('serial.tools.list_ports.comports', mockComports)
    mocker.patch('ndicapy.ndiProbe', mockndiProbe)
    mocker.patch('ndicapy.ndiOpen', mockndiOpen)
    mocker.patch('ndicapy.ndiCommand')
    mocker.patch('ndicapy.ndiGetError', mockndiGetError)
    mocker.patch('ndicapy.ndiClose')
    mocker.patch('ndicapy.ndiGetPHSRNumberOfHandles',
            mockndiGetPHSRNumberOfHandles)
    mocker.patch('ndicapy.ndiGetPHRQHandle', mockndiGetPHRQHandle)
    mocker.patch('ndicapy.ndiPVWRFromFile')
    mocker.patch('ndicapy.ndiGetPHSRHandle', mockndiGetPHSRHandle)
    mocker.patch('ndicapy.ndiVER', mockndiVER)
    tracker = NDITracker(SETTINGS_POLARIS)
    del tracker
