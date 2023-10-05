# coding=utf-8

"""scikit-surgerynditracker tests using a mocked ndicapy"""

import numpy as np
from sksurgerynditracker.nditracker import NDITracker

from tests.polaris_mocks import SETTINGS_POLARIS, SETTINGS_POLARIS_QUAT, \
        SETTINGS_POLARIS_SMOOTH, SETTINGS_POLARIS_QUAT_SMOOTH, \
        mockndiProbe, \
        mockndiOpen, mockndiGetError, mockComports, \
        mockndiGetPHSRHandle, mockndiVER, \
        MockNDIDevice, MockBXFrameSource

def test_getframe_polaris_mock(mocker):
    """
    connects and configures, mocks ndicapy.ndiProbe to pass
    reqs: 03, 04
    """
    tracker = None
    bxsource = MockBXFrameSource()
    ndidevice = MockNDIDevice()
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
    mocker.patch('ndicapy.ndiGetBXFrame', bxsource.mockndiGetBXFrame)
    mocker.patch('ndicapy.ndiGetBXTransform', bxsource.mockndiGetBXTransform)

    tracker = NDITracker(SETTINGS_POLARIS)

    bxsource.setdevice(ndidevice)

    (port_handles, time_stamps, frame_numbers, tracking,
                tracking_quality ) = tracker.get_frame()

    assert len(port_handles) == 2
    assert len(time_stamps) == 2
    assert frame_numbers.count(1) == 2
    expected_tracking_0 = np.array([[1.,0.,0.,10.],
                                 [0.,1.,0.,-20.],
                                 [0.,0.,1.,5.],
                                 [0.,0.,0.,1.]])
    assert np.array_equal(expected_tracking_0, tracking[0])
    expected_tracking_1 = np.array([[1.,0.,0.,0.],
                                 [0.,1.,0.,0.],
                                 [0.,0.,1.,0.],
                                 [0.,0.,0.,1.]])
    assert np.array_equal(expected_tracking_1, tracking[1])
    assert tracking_quality.count(1.) == 2

    (port_handles, time_stamps, frame_numbers, tracking,
                tracking_quality ) = tracker.get_frame()

    assert len(port_handles) == 2
    assert len(time_stamps) == 2
    assert frame_numbers.count(2) == 2
    expected_tracking_0 = np.array([[1.,0.,0.,20.],
                                 [0.,1.,0.,-40.],
                                 [0.,0.,1.,10.],
                                 [0.,0.,0.,1.]])
    assert np.array_equal(expected_tracking_0, tracking[0])
    assert np.array_equal(expected_tracking_1, tracking[1])
    assert tracking_quality.count(1.) == 2

    del tracker

def test_getframe_polaris_mock_quat(mocker):
    """
    Checks that get frame works with quaternions
    """
    tracker = None
    bxsource = MockBXFrameSource()
    ndidevice = MockNDIDevice()
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
    mocker.patch('ndicapy.ndiGetBXFrame', bxsource.mockndiGetBXFrame)
    mocker.patch('ndicapy.ndiGetBXTransform', bxsource.mockndiGetBXTransform)

    tracker = NDITracker(SETTINGS_POLARIS_QUAT)

    bxsource.setdevice(ndidevice)

    (port_handles, time_stamps, frame_numbers, tracking,
                tracking_quality ) = tracker.get_frame()

    assert len(port_handles) == 2
    assert len(time_stamps) == 2
    assert frame_numbers.count(1) == 2
    expected_tracking_0 = np.array([[1.,0.,0.,0.,10.,-20,5.]])
    assert np.array_equal(expected_tracking_0, tracking[0])
    expected_tracking_1 = np.array([[1.,0.,0.,0.,0.,0.,0.]])
    assert np.array_equal(expected_tracking_1, tracking[1])
    assert tracking_quality.count(1.) == 2

    (port_handles, time_stamps, frame_numbers, tracking,
                tracking_quality ) = tracker.get_frame()

    assert len(port_handles) == 2
    assert len(time_stamps) == 2
    assert frame_numbers.count(2) == 2
    expected_tracking_0 = np.array([[1.,0.,0.,0.,20.,-40,10.]])
    assert np.array_equal(expected_tracking_0, tracking[0])
    assert np.array_equal(expected_tracking_1, tracking[1])
    assert tracking_quality.count(1.) == 2

    del tracker

def test_getframe_missing(mocker):
    """
    connects and configures, mocks ndicapy.ndiProbe to pass
    reqs: 03, 04
    """
    tracker = None
    bxsource = MockBXFrameSource()
    ndidevice = MockNDIDevice()
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
    mocker.patch('ndicapy.ndiGetBXFrame', bxsource.mockndiGetBXFrame)
    mocker.patch('ndicapy.ndiGetBXTransform',
            bxsource.mockndiGetBXTransformMissing)

    tracker = NDITracker(SETTINGS_POLARIS)

    bxsource.setdevice(ndidevice)
    (port_handles, time_stamps, frame_numbers, tracking,
                tracking_quality ) = tracker.get_frame()

    assert len(port_handles) == 2
    assert len(time_stamps) == 2
    assert frame_numbers.count(1) == 2
    assert np.any(np.isnan(tracking[0]))
    assert np.any(np.isnan(tracking[1]))
    assert np.all(np.isnan(tracking_quality))

    del tracker

def test_getframe_smooth_mock(mocker):
    """
    connects and configures, mocks ndicapy.ndiProbe to pass
    reqs: 03, 04
    """
    tracker = None
    bxsource = MockBXFrameSource()
    ndidevice = MockNDIDevice()
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
    mocker.patch('ndicapy.ndiGetBXFrame', bxsource.mockndiGetBXFrame)
    mocker.patch('ndicapy.ndiGetBXTransform', bxsource.mockndiGetBXTransform)

    tracker = NDITracker(SETTINGS_POLARIS_SMOOTH)

    bxsource.setdevice(ndidevice)

    (port_handles, time_stamps, frame_numbers, tracking,
                tracking_quality ) = tracker.get_frame()

    assert len(port_handles) == 2
    assert len(time_stamps) == 2
    assert frame_numbers.count(1) == 2
    expected_tracking_0 = np.array([[1.,0.,0.,10.],
                                 [0.,1.,0.,-20.],
                                 [0.,0.,1.,5.],
                                 [0.,0.,0.,1.]])
    assert np.array_equal(expected_tracking_0, tracking[0])
    expected_tracking_1 = np.array([[1.,0.,0.,0.],
                                 [0.,1.,0.,0.],
                                 [0.,0.,1.,0.],
                                 [0.,0.,0.,1.]])
    assert np.array_equal(expected_tracking_1, tracking[1])
    assert tracking_quality.count(1.) == 2

    (port_handles, time_stamps, frame_numbers, tracking,
                tracking_quality ) = tracker.get_frame()

    assert len(port_handles) == 2
    assert len(time_stamps) == 2
    assert frame_numbers.count(2) == 2
    expected_tracking_0 = np.array([[1.,0.,0.,15.],
                                 [0.,1.,0.,-30.],
                                 [0.,0.,1.,7.5],
                                 [0.,0.,0.,1.]])
    assert np.array_equal(expected_tracking_0, tracking[0])
    assert np.array_equal(expected_tracking_1, tracking[1])
    assert tracking_quality.count(1.) == 2

    del tracker

def test_getframe_smooth_mock_quat(mocker):
    """
    Checks that get frame works with quaternions
    """
    tracker = None
    bxsource = MockBXFrameSource()
    ndidevice = MockNDIDevice()
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
    mocker.patch('ndicapy.ndiGetBXFrame', bxsource.mockndiGetBXFrame)
    mocker.patch('ndicapy.ndiGetBXTransform', bxsource.mockndiGetBXTransform)

    tracker = NDITracker(SETTINGS_POLARIS_QUAT_SMOOTH)

    bxsource.setdevice(ndidevice)

    (port_handles, time_stamps, frame_numbers, tracking,
                tracking_quality ) = tracker.get_frame()

    assert len(port_handles) == 2
    assert len(time_stamps) == 2
    assert frame_numbers.count(1) == 2
    expected_tracking_0 = np.array([[1.,0.,0.,0.,10.,-20,5.]])
    assert np.array_equal(expected_tracking_0, tracking[0])
    expected_tracking_1 = np.array([[1.,0.,0.,0.,0.,0.,0.]])
    assert np.array_equal(expected_tracking_1, tracking[1])
    assert tracking_quality.count(1.) == 2

    (port_handles, time_stamps, frame_numbers, tracking,
                tracking_quality ) = tracker.get_frame()

    assert len(port_handles) == 2
    assert len(time_stamps) == 2
    assert frame_numbers.count(2) == 2
    expected_tracking_0 = np.array([[1.,0.,0.,0.,15.,-30,7.5]])
    assert np.array_equal(expected_tracking_0, tracking[0])
    assert np.array_equal(expected_tracking_1, tracking[1])
    assert tracking_quality.count(1.) == 2

    del tracker

def test_getframe_missing_smooth(mocker):
    """
    connects and configures, mocks ndicapy.ndiProbe to pass
    reqs: 03, 04
    """
    tracker = None
    bxsource = MockBXFrameSource()
    ndidevice = MockNDIDevice()
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
    mocker.patch('ndicapy.ndiGetBXFrame', bxsource.mockndiGetBXFrame)
    mocker.patch('ndicapy.ndiGetBXTransform',
            bxsource.mockndiGetBXTransformMissing)

    tracker = NDITracker(SETTINGS_POLARIS_SMOOTH)

    bxsource.setdevice(ndidevice)
    (port_handles, time_stamps, frame_numbers, tracking,
                tracking_quality ) = tracker.get_frame()

    assert len(port_handles) == 2
    assert len(time_stamps) == 2
    assert frame_numbers.count(1) == 2
    assert np.any(np.isnan(tracking[0]))
    assert np.any(np.isnan(tracking[1]))
    assert np.all(np.isnan(tracking_quality))

    del tracker
