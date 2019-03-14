# coding=utf-8

"""scikit-surgerynditracker tests"""

import pytest
from sksurgerynditracker.nditracker import NDITracker

#configuration.
SETTINGS_VEGA = {
        "tracker type": "vega",
        "ip address" : "192.168.2.17",
        "port" : 8765,
        "romfiles" : [
            "../data/something_else.rom",
            "../data/8700339.rom"]
        }

SETTINGS_POLARIS = {
        "tracker type": "polaris",
        "romfiles" : [
            "../data/something_else.rom",
            "../data/8700339.rom"]
        }

SETTINGS_AURORA = {
        "tracker type": "aurora"
        }

SETTINGS_DUMMY = {
        "tracker type": "dummy",
        }

def test_connect():
    #what testing can we do with out being attached to a tracker?
    #What testing can we do when we are attached to a tracker?
    #We could build a fake ndi tracker, that listens on a port
    #and responds appropriately.
    tracker = NDITracker(SETTINGS_DUMMY)
    tracker.close()

def test_connect_network():
    with pytest.raises(IOError):
        tracker = NDITracker(SETTINGS_VEGA)
        del tracker

def test_connect_serial():
    tracker = None
    with pytest.raises(IOError):
        tracker = NDITracker(SETTINGS_POLARIS)
        del tracker

def test_configure():
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
        tracker = NDITracker (bad_tracker)
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

    with pytest.raises(IOError) or pytest.raises(OSError):
        aurora = { "tracker type": "aurora" }
        tracker = NDITracker(aurora)
        del tracker

    with pytest.raises(IOError) or pytest.raises(OSError):
        aurora_sp = { "tracker type": "aurora",
                      "serial_port": "1" }
        tracker = NDITracker(aurora_sp)
        del tracker

    with pytest.raises(IOError) or pytest.raises(OSError):
        aurora_np = { "tracker type": "aurora",
                      "ports to probe": "50" }
        tracker = NDITracker(aurora_np)
        del tracker

def test_close():
    tracker = NDITracker(SETTINGS_DUMMY)
    tracker.close()
    del tracker

def test_read_sroms_from_file():
    tracker = NDITracker(SETTINGS_DUMMY)
    with pytest.raises(ValueError):
        tracker._read_sroms_from_file()
    tracker.close()

def test_initialise_ports():
    tracker = NDITracker(SETTINGS_DUMMY)
    tracker._device = None
    with pytest.raises(ValueError):
        tracker._initialise_ports()
    with pytest.raises(ValueError):
        tracker.close()

def test_enable_tools():
    tracker = NDITracker(SETTINGS_DUMMY)
    tracker._device = None
    with pytest.raises(ValueError):
        tracker._enable_tools()
    with pytest.raises(ValueError):
        tracker.close()

def test_get_frame():
    tracker = NDITracker(SETTINGS_DUMMY)
    port_handles, timestamps, framenumbers, \
        tracking, tracking_quality = tracker.get_frame()

    assert len(tracking) == 0

    del tracker
    dummy_two_rom = {
        "tracker type": "dummy",
        "romfiles" : [
            "../data/something_else.rom",
            "../data/8700339.rom"]
        }

    tracker = NDITracker(dummy_two_rom)
    port_handles, timestamps, framenumbers, \
        tracking, tracking_quality = tracker.get_frame()
    assert len(tracking) == 2
    assert tracking[0].shape == (4,4)
    assert tracking[0].dtype == 'float64'

def test_get_tool_descriptions():
    tracker = NDITracker(SETTINGS_DUMMY)
    descriptions = tracker.get_tool_descriptions()
    assert len(descriptions) == 0
    del tracker

    dummy_two_rom = {
        "tracker type": "dummy",
        "romfiles" : [
            "../data/something_else.rom",
            "../data/8700339.rom"]
        }

    tracker = NDITracker(dummy_two_rom)
    descriptions = tracker.get_tool_descriptions()
    assert len(descriptions) == 2

def test_start_tracking():
    tracker = NDITracker(SETTINGS_DUMMY)
    with pytest.raises(ValueError):
        tracker.start_tracking()
    tracker.close()

def test_stop_tracking():
    tracker = NDITracker(SETTINGS_DUMMY)
    with pytest.raises(ValueError):
        tracker.stop_tracking()
    tracker.close()

def test_check_for_errors():
    tracker = NDITracker(SETTINGS_DUMMY)
    with pytest.raises(ValueError):
        tracker._check_for_errors("dummy error")
    tracker.close()

