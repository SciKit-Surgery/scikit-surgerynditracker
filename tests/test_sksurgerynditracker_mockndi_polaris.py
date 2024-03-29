# coding=utf-8

"""scikit-surgerynditracker tests using a mocked ndicapy"""
import ndicapy
import pytest
from mock import call
from sksurgerynditracker.nditracker import NDITracker

from tests.polaris_mocks import SETTINGS_POLARIS, mockndiProbe, \
        mockndiOpen, mockndiOpen_fail, mockndiGetError, mockComports, \
        mockndiGetPHSRHandle, mockndiVER, MockNDIDevice

def test_connect_polaris_mock(mocker):
    """
    connects and configures, mocks ndicapy.ndiProbe to pass
    reqs: 03, 04
    """
    tracker = None
    ndidevice = MockNDIDevice()
    #add a couple of extra tools to increase test coverage
    ndidevice.attached_tools = 2
    mocker.patch('serial.tools.list_ports.comports', mockComports)
    mocker.patch('ndicapy.ndiProbe', mockndiProbe)
    mocker.patch('ndicapy.ndiOpen', mockndiOpen)
    mocker.patch('ndicapy.ndiCommand', ndidevice.mockndiCommand)
    mocker.patch('ndicapy.ndiGetError', mockndiGetError)
    mocker.patch('ndicapy.ndiClose')
    mocker.patch('ndicapy.ndiGetPHSRNumberOfHandles',
            ndidevice.mockndiGetPHSRNumberOfHandles)
    mocker.patch('ndicapy.ndiGetPHRQHandle', ndidevice.mockndiGetPHRQHandle)
    mocker.patch('ndicapy.ndiPVWRFromFile')
    mocker.patch('ndicapy.ndiGetPHSRHandle', mockndiGetPHSRHandle)
    mocker.patch('ndicapy.ndiVER', mockndiVER)
    spy = mocker.spy(ndicapy, 'ndiCommand')
    tracker = NDITracker(SETTINGS_POLARIS)

    assert spy.call_count == 16
    assert spy.call_args_list[0] == call(True, 'INIT:')
    assert spy.call_args_list[1] == call(True, 'COMM:50000')
    assert spy.call_args_list[2] == call(True, 'PHSR:01')
    assert spy.call_args_list[3] == call(True, 'PHF:00')
    assert spy.call_args_list[4] == call(True, 'PHF:01')
    assert spy.call_args_list[5] == call(True, 'PHRQ:*********1****')
    assert spy.call_args_list[6] == call(True, 'PHRQ:*********1****')
    assert spy.call_args_list[7] == call(True, 'PHSR:01')
    assert spy.call_args_list[8] == call(True, 'PHSR:02')
    assert spy.call_args_list[9] == call(True, 'PINIT:02')
    assert spy.call_args_list[10] == call(True, 'PINIT:03')
    assert spy.call_args_list[11] == call(True, 'PHSR:03')
    assert spy.call_args_list[12] == call(True, 'PENA:00D')
    assert spy.call_args_list[13] == call(True, 'PENA:01D')
    assert spy.call_args_list[14] == call(True, 'PENA:02D')
    assert spy.call_args_list[15] == call(True, 'PENA:03D')
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
