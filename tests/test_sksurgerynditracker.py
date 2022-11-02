# coding=utf-8

"""scikit-surgerynditracker tests"""

#what testing can we do with out being attached to a tracker?
#What testing can we do when we are attached to a tracker?
#We could build a fake ndi tracker, that listens on a port
#and responds appropriately.

import pytest
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

def test_connect():
    """
    connects and configures ,
    reqs: 03, 04
    """

    tracker = NDITracker(SETTINGS_DUMMY)
    assert not tracker.use_quaternions
    tracker.close()

def test_connect_quaternions():
    """
    connects and configures ,
    reqs: 03, 04
    """

    tracker = NDITracker(SETTINGS_DUMMY_QUATERNIONS)
    assert tracker.use_quaternions
    assert tracker.buffer_size == 1
    tracker.close()

    SETTINGS_DUMMY_QUATERNIONS['smoothing buffer'] = 3
    tracker = NDITracker(SETTINGS_DUMMY_QUATERNIONS)
    assert tracker.buffer_size == 3



def test_connect_network():
    """
    connects and configures, throws error when no vega
    reqs: 03, 04
    """
    with pytest.raises(IOError):
        tracker = NDITracker(SETTINGS_VEGA)
        del tracker


def test_connect_serial():
    """
    connects and configures, throws error when no serial
    reqs: 03, 04
    """
    tracker = None
    with pytest.raises(IOError):
        tracker = NDITracker(SETTINGS_POLARIS)
        del tracker


def test_configure():
    """
    connects and configures, throws errors when when errors in dictionary
    reqs: 03, 04
    """
    no_rom = {
        "tracker type": "polaris",
        }
    with pytest.raises(KeyError):
        tracker = NDITracker(no_rom)
        del tracker

    bad_tracker = {
        "tracker type": "optotrack",
        }
    with pytest.raises(ValueError):
        tracker = NDITracker(bad_tracker)
        del tracker

    no_ip = {
        "tracker type": "vega",
        "romfiles": "[rom]"
        }
    with pytest.raises(KeyError):
        tracker = NDITracker(no_ip)
        del tracker

    with pytest.raises(IOError) or pytest.raises(OSError):
        no_port = {
            "tracker type": "vega",
            "ip address": "tracker",
            "romfiles": "[rom]"
            }
        tracker = NDITracker(no_port)
        del tracker

    with pytest.raises(KeyError):
        no_tracker_type = {
            "tracker_type": "vega",
            "ip address": "tracker",
            "romfiles": "[rom]"
            }
        tracker = NDITracker(no_tracker_type)
        del tracker

    with pytest.raises(KeyError):
        no_room_files_vega = {
            "tracker type": "vega",
            "ip address": "tracker",
            }
        tracker = NDITracker(no_room_files_vega)
        del tracker

    with pytest.raises(FileNotFoundError):
        no_room_files_in_paths_polaris = {
            "tracker type": "polaris",
            "romfiles" : [
                "data/something_else_rom",
                "data/8700339_rom"]
            }
        tracker = NDITracker(no_room_files_in_paths_polaris)
        del tracker

    with pytest.raises(IOError) or pytest.raises(OSError):
        aurora = {"tracker type": "aurora"}
        tracker = NDITracker(aurora)
        del tracker

    #try with an integer serial port
    with pytest.raises(IOError) or pytest.raises(OSError):
        aurora_sp = {"tracker type": "aurora",
                     "serial port": 0}
        tracker = NDITracker(aurora_sp)
        del tracker

    #try with verbose on
    with pytest.raises(IOError) or pytest.raises(OSError):
        aurora_np = {"tracker type": "aurora",
                     "ports to probe": 10,
                     "verbose": True}
        tracker = NDITracker(aurora_np)
        del tracker

    #with a named serial port on windows
    with pytest.raises(IOError) or pytest.raises(OSError):
        aurora_np = {"tracker type": "aurora",
                     "serial port": "COM2",
                     "verbose": True}
        tracker = NDITracker(aurora_np)
        del tracker



def test_get_frame():
    """
    test get frame returns numpy array
    reqs:05, 06
    """
    tracker = NDITracker(SETTINGS_DUMMY)
    _port_handles, _timestamps, _framenumbers, \
        tracking, _tracking_quality = tracker.get_frame()

    assert not tracking

    del tracker
    dummy_two_rom = {
        "tracker type": "dummy",
        "romfiles" : [
            "data/something_else.rom",
            "data/8700339.rom"]
        }

    tracker = NDITracker(dummy_two_rom)
    _port_handles, _timestamps, _framenumbers, \
        tracking, _tracking_quality = tracker.get_frame()
    assert len(tracking) == 2
    assert tracking[0].shape == (4, 4)
    assert tracking[0].dtype == 'float64'


def test_get_tool_descriptions():
    """
    test get tool descriptions
    reqs:05, 06
    """
    tracker = NDITracker(SETTINGS_DUMMY)
    _port_handles, descriptions = tracker.get_tool_descriptions()
    assert not descriptions
    del tracker

    dummy_two_rom = {
        "tracker type": "dummy",
        "romfiles" : [
            "data/something_else.rom",
            "data/8700339.rom"]
        }

    tracker = NDITracker(dummy_two_rom)
    _port_handles, descriptions = tracker.get_tool_descriptions()
    assert len(descriptions) == 2

def test_throw_file_not_found_error():
    """
    tests that we throw a file not found for no rom file
    """

    dummy_two_rom = {
        "tracker type": "dummy",
        "romfiles" : [
            "notmydata/something_else.rom",
            "data/8700339.rom"]
        }

    with pytest.raises(FileNotFoundError):
        _tracker = NDITracker(dummy_two_rom)


def test_start_tracking():
    """
    test start tracking
    reqs:
    """
    tracker = NDITracker(SETTINGS_DUMMY)
    with pytest.raises(ValueError):
        tracker.start_tracking()
    tracker.close()


def test_stop_tracking():
    """
    test stop tracking
    reqs:
    """
    tracker = NDITracker(SETTINGS_DUMMY)
    with pytest.raises(ValueError):
        tracker.stop_tracking()
    tracker.close()
