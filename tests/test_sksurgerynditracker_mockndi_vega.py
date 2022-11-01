# coding=utf-8

"""scikit-surgerynditracker tests using a mocked ndicapy"""
import pytest
import ndicapy
from mock import call
from sksurgerynditracker.nditracker import NDITracker

SETTINGS_VEGA = {
    "tracker type": "vega",
    "ip address" : "127.0.0.1",
    "port" : 0000,
    "romfiles" : [
        "data/something_else.rom",
        "data/8700339.rom"]
    }

def mockndiOpenNetwork(_ip_address, _port): #pylint:disable=invalid-name
    """Mock of ndiOpenNetwork"""
    return True

def mockndiOpenNetwork_nodevice(_ip_address, _port):  # pylint:disable=invalid-name
    """Mock of ndiOpenNetwork with no device"""
    return False

def mockndiGetError(_device): #pylint:disable=invalid-name
    """Mock of ndiGetError"""
    return ndicapy.NDI_OKAY

def mockndiGetPHSRNumberOfHandles(_device): #pylint:disable=invalid-name
    """Mock of ndiGetPHSRNumberOfHandles"""
    return 0

def mockndiGetPHRQHandle(_device, index=0): #pylint:disable=invalid-name
    """Mock of ndiGetPHRQHandle"""
    return int(index)

def mockndiGetPHSRHandle(_device, index): #pylint:disable=invalid-name
    """Mock of ndiGetPHSRHandle"""
    return int(index)

def mockndiVER(_device, _other_arg): #pylint:disable=invalid-name
    """Mock of ndiVER"""
    return 'Mock for Testing'

def test_connect_vega_mock(mocker):
    """
    connects and configures, mocks ndicapy.ndiProbe to pass
    reqs: 03, 04
    """
    tracker = None
    mocker.patch('ndicapy.ndiOpenNetwork', mockndiOpenNetwork)
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
    tracker = NDITracker(SETTINGS_VEGA)

    assert spy.call_count == 9
    assert spy.call_args_list[0] == call(True, 'INIT:')
    assert spy.call_args_list[1] == call(True, 'PHSR:01')
    assert spy.call_args_list[3] == call(True, 'PHRQ:*********1****')
    assert spy.call_args_list[4] == call(True, 'PHSR:01')
    assert spy.call_args_list[5] == call(True, 'PHSR:02')
    assert spy.call_args_list[6] == call(True, 'PINIT:00')
    assert spy.call_args_list[7] == call(True, 'PINIT:00')
    assert spy.call_args_list[8] == call(True, 'PHSR:03')
    del tracker

def test_connect_vega_mock_nodevice(mocker):
    """
    connects and configures, mocks ndicapy.ndiProbe to pass
    reqs: 03, 04
    """
    tracker = None
    mocker.patch('ndicapy.ndiOpenNetwork', mockndiOpenNetwork_nodevice)
    mocker.patch('ndicapy.ndiCommand')

    with pytest.raises(IOError,
                       match='Could not connect to network NDI device'):

        tracker = NDITracker(SETTINGS_VEGA)
        del tracker
