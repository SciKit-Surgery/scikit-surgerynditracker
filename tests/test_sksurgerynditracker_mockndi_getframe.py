# coding=utf-8

"""scikit-surgerynditracker tests using a mocked ndicapy"""
from sksurgerynditracker.nditracker import NDITracker

from tests.polaris_mocks import SETTINGS_POLARIS, mockndiProbe, \
        mockndiOpen, mockndiGetError, mockComports, \
        mockndiGetPHSRNumberOfHandles, mockndiGetPHRQHandle, \
        mockndiGetPHSRHandle, mockndiVER, mockndiGetBXFrame, \
        mockndiGetBXTransform, mockndiGetBXTransformMissing

def test_getframe_polaris_mock(mocker):
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
    mocker.patch('ndicapy.ndiGetBXFrame', mockndiGetBXFrame)
    mocker.patch('ndicapy.ndiGetBXTransform', mockndiGetBXTransform)

    tracker = NDITracker(SETTINGS_POLARIS)
    tracker.get_frame()

    del tracker

def test_getframe_missing(mocker):
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
    mocker.patch('ndicapy.ndiGetBXFrame', mockndiGetBXFrame)
    mocker.patch('ndicapy.ndiGetBXTransform', mockndiGetBXTransformMissing)

    tracker = NDITracker(SETTINGS_POLARIS)
    tracker.get_frame()

    del tracker
