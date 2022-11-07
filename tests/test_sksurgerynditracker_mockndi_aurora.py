# coding=utf-8

"""scikit-surgerynditracker tests using a mocked ndicapy"""
import ndicapy
import pytest
from mock import call
from sksurgerynditracker.nditracker import NDITracker

# configuration.
SETTINGS_AURORA = {
    "tracker type": "aurora"
}


class MockPort:
    """A fake serial port for ndi"""
    device = 'bad port'


def mockndiProbe(port_name):  # pylint:disable=invalid-name
    """Mock of ndiProbe"""
    if port_name == 'good port':
        return ndicapy.NDI_OKAY
    return ndicapy.NDI_PROBE_FAIL


def mockndiOpen(port_name):  # pylint:disable=invalid-name
    """Mock of ndiOpen"""
    if port_name == 'good port':
        return True
    return False


def mockndiGetError(_device):  # pylint:disable=invalid-name
    """Mock of ndiGetError"""
    return ndicapy.NDI_OKAY


def mockndiGetErrorFail(_device):  # pylint:disable=invalid-name
    """Mock of ndiGetErrorFail"""
    return ndicapy.NDI_PROBE_FAIL


def mockComports():  # pylint:disable=invalid-name
    """Returns a list of mock comports"""
    mock_ports = [MockPort] * 20
    mock_ports[5].device = 'good port'
    return mock_ports


def mockndiGetPHSRNumberOfHandles(_device):  # pylint:disable=invalid-name
    """Mock of ndiGetPHSRNumberOfHandles"""
    mockndiGetPHSRNumberOfHandles.number_of_tool_handles -= 1
    return mockndiGetPHSRNumberOfHandles.number_of_tool_handles


def mockndiGetPHRQHandle(_device, index=0):  # pylint:disable=invalid-name
    """Mock of ndiGetPHRQHandle"""
    return int(index)


def mockndiGetPHSRHandle(_device, index):  # pylint:disable=invalid-name
    """Mock of ndiGetPHSRHandle"""
    return int(index)


def mockndiVER(_device, _other_arg):  # pylint:disable=invalid-name
    """Mock of ndiVER"""
    return 'Freeze Tag: Mock for Testing'


def test_connect_aurora_mock(mocker):
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

    mockndiGetPHSRNumberOfHandles.number_of_tool_handles = 3
    tracker = NDITracker(SETTINGS_AURORA)

    assert spy.call_count == 13
    assert spy.call_args_list[0] == call(True, 'INIT:')
    assert spy.call_args_list[1] == call(True, 'COMM:50000')
    assert spy.call_args_list[2] == call(True, 'PHSR:02')
    assert spy.call_args_list[3] == call(True, 'PINIT:00')
    assert spy.call_args_list[4] == call(True, 'PINIT:01')
    assert spy.call_args_list[5] == call(True, 'PHSR:02')
    assert spy.call_args_list[6] == call(True, 'PINIT:00')
    assert spy.call_args_list[7] == call(True, 'PHSR:02')
    assert spy.call_args_list[8] == call(True, 'PHSR:02')
    assert spy.call_args_list[9] == call(True, 'PINIT:00')
    assert spy.call_args_list[10] == call(True, 'PINIT:01')
    assert spy.call_args_list[11] == call(True, 'PINIT:00')
    assert spy.call_args_list[12] == call(True, 'PHSR:03')
    tracker.start_tracking()
    assert spy.call_args_list[13] == call(True, 'TSTART:')
    tracker.stop_tracking()
    assert spy.call_args_list[14] == call(True, 'TSTOP:')
    tracker.close()
    del tracker


def test_connect_aurora_mock_error(mocker):
    """
    connects and configures, mocks ndicapy.ndiProbe to pass IOError()
    """
    tracker = None
    mocker.patch('serial.tools.list_ports.comports', mockComports)
    mocker.patch('ndicapy.ndiProbe', mockndiProbe)
    mocker.patch('ndicapy.ndiOpen', mockndiOpen)
    mocker.patch('ndicapy.ndiCommand')
    mocker.patch('ndicapy.ndiGetError', mockndiGetErrorFail)
    mocker.patch('ndicapy.ndiClose')
    mocker.patch('ndicapy.ndiGetPHSRNumberOfHandles',
                 mockndiGetPHSRNumberOfHandles)
    mocker.patch('ndicapy.ndiGetPHRQHandle', mockndiGetPHRQHandle)
    mocker.patch('ndicapy.ndiPVWRFromFile')
    mocker.patch('ndicapy.ndiGetPHSRHandle', mockndiGetPHSRHandle)
    mocker.patch('ndicapy.ndiVER', mockndiVER)

    mockndiGetPHSRNumberOfHandles.number_of_tool_handles = 3
    with pytest.raises(IOError):
        tracker = NDITracker(SETTINGS_AURORA)

    del tracker

def test_starttracking_aurora_ready(mocker):
    """
    connects and configures, mocks non ready state to pass
    ValueError() in start_tracking()
    """

    tracker = None
    mocker.patch('serial.tools.list_ports.comports', mockComports)
    mocker.patch('ndicapy.ndiProbe', mockndiProbe)
    mocker.patch('ndicapy.ndiOpen', mockndiOpen)
    mocker.patch('ndicapy.ndiCommand')
    mocker.patch('ndicapy.ndiGetError', mockndiGetError)
    mocker.patch('ndicapy.ndiGetPHSRNumberOfHandles',
                 mockndiGetPHSRNumberOfHandles)
    mocker.patch('ndicapy.ndiGetPHSRHandle', mockndiGetPHSRHandle)
    mocker.patch('ndicapy.ndiVER', mockndiVER)
    mockndiGetPHSRNumberOfHandles.number_of_tool_handles = 3

    with pytest.raises(ValueError):
        tracker = NDITracker(SETTINGS_AURORA)
        tracker._state = 'non_ready'  # pylint: disable=protected-access
        tracker.start_tracking()

    del tracker


def test_initialise_ports_aurora(mocker):
    """
    connects and configures, mocks non ready state to pass
    ValueError() in start_tracking()
    """

    tracker = None
    mocker.patch('serial.tools.list_ports.comports', mockComports)
    mocker.patch('ndicapy.ndiProbe', mockndiProbe)
    mocker.patch('ndicapy.ndiOpen', mockndiOpen)
    mocker.patch('ndicapy.ndiCommand')
    mocker.patch('ndicapy.ndiGetError', mockndiGetError)
    mocker.patch('ndicapy.ndiGetPHSRNumberOfHandles',
                 mockndiGetPHSRNumberOfHandles)
    mocker.patch('ndicapy.ndiGetPHSRHandle', mockndiGetPHSRHandle)
    mocker.patch('ndicapy.ndiVER', mockndiVER)
    mockndiGetPHSRNumberOfHandles.number_of_tool_handles = 3

    with pytest.raises(ValueError):
        tracker = NDITracker(SETTINGS_AURORA)
        tracker._device = False  # pylint: disable=protected-access
        tracker._initialise_ports()  # pylint: disable=protected-access

    del tracker

def test_enable_tools_aurora(mocker):
    """
    connects and configures, mocks non ready state to pass
    ValueError() in start_tracking()
    """

    tracker = None
    mocker.patch('serial.tools.list_ports.comports', mockComports)
    mocker.patch('ndicapy.ndiProbe', mockndiProbe)
    mocker.patch('ndicapy.ndiOpen', mockndiOpen)
    mocker.patch('ndicapy.ndiCommand')
    mocker.patch('ndicapy.ndiGetError', mockndiGetError)
    mocker.patch('ndicapy.ndiGetPHSRNumberOfHandles',
                 mockndiGetPHSRNumberOfHandles)
    mocker.patch('ndicapy.ndiGetPHSRHandle', mockndiGetPHSRHandle)
    mocker.patch('ndicapy.ndiVER', mockndiVER)
    mockndiGetPHSRNumberOfHandles.number_of_tool_handles = 3

    with pytest.raises(ValueError):
        tracker = NDITracker(SETTINGS_AURORA)
        tracker._device = False  # pylint: disable=protected-access
        tracker._enable_tools()  # pylint: disable=protected-access

    del tracker
