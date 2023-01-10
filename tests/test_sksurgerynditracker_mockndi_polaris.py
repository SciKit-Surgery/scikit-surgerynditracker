# coding=utf-8

"""scikit-surgerynditracker tests using a mocked ndicapy"""
import ndicapy
import pytest
from mock import call
from sksurgerynditracker.nditracker import NDITracker

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

def test_connect_polaris_mock(mocker):
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
    spy = mocker.spy(ndicapy, 'ndiCommand')
    tracker = NDITracker(SETTINGS_POLARIS)

    assert spy.call_count == 18
    assert spy.call_args_list[0] == call(True, 'INIT:')
    assert spy.call_args_list[1] == call(True, 'COMM:50000')
    assert spy.call_args_list[2] == call(True, 'PHSR:01')
    assert spy.call_args_list[3] == call(True, 'PHF:00')
    assert spy.call_args_list[4] == call(True, 'PHF:01')
    assert spy.call_args_list[5] == call(True, 'PHF:02')
    assert spy.call_args_list[6] == call(True, 'PHF:03')
    assert spy.call_args_list[7] == call(True, 'PHRQ:*********1****')
    assert spy.call_args_list[8] == call(True, 'PHRQ:*********1****')
    assert spy.call_args_list[9] == call(True, 'PHSR:01')
    assert spy.call_args_list[10] == call(True, 'PHSR:02')
    assert spy.call_args_list[11] == call(True, 'PINIT:00')
    assert spy.call_args_list[12] == call(True, 'PINIT:00')
    assert spy.call_args_list[13] == call(True, 'PHSR:03')
    assert spy.call_args_list[14] == call(True, 'PENA:00D')
    assert spy.call_args_list[15] == call(True, 'PENA:01D')
    assert spy.call_args_list[16] == call(True, 'PENA:02D')
    assert spy.call_args_list[17] == call(True, 'PENA:03D')
    del tracker

def test_connect_polaris_mk_fserial(mocker):
    """
    connects and configures, mocks ndicapy.ndiOpen to False
    reqs: 03, 04
    """
    tracker = None
    mocker.patch('serial.tools.list_ports.comports', mockComports)
    mocker.patch('ndicapy.ndiProbe', mockndiProbe)
    mocker.patch('ndicapy.ndiOpen', mockndiOpen_fail)
    with pytest.raises(IOError):
        tracker = NDITracker(SETTINGS_POLARIS)
        del tracker
