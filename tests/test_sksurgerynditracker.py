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
    tracker = NDITracker()
    tracker.connect(SETTINGS_DUMMY)
    tracker.close()

def test_connect_network():
    tracker = NDITracker()
    with pytest.raises(IOError):
        tracker.connect(SETTINGS_VEGA)
    with pytest.raises(ValueError):
        tracker.close()

def test_connect_serial():
    tracker = NDITracker()
    with pytest.raises(IOError):
        tracker.connect(SETTINGS_POLARIS)
    with pytest.raises(ValueError):
        tracker.close()

def test_configure():
    tracker = NDITracker()
    no_rom = {
        "tracker type": "polaris",
        }
    with pytest.raises(KeyError):
        tracker._configure(no_rom)

    bad_tracker = {
        "tracker type": "optotrack",
        }
    with pytest.raises(ValueError):
        tracker._configure(bad_tracker)

    no_ip = {
        "tracker type": "vega",
        "romfiles": "[rom]"
        }
    with pytest.raises(KeyError):
        tracker._configure(no_ip)

    no_port = {
        "tracker type": "vega",
        "ip address": "tracker",
        "romfiles": "[rom]"
        }
    tracker._configure(no_port)

    aurora = { "tracker type": "aurora" }
    tracker._configure(aurora)

    aurora_sp = { "tracker type": "aurora",
                  "serial_port": "1" }
    tracker._configure(aurora_sp)

    aurora_np = { "tracker type": "aurora",
                  "ports to probe": "50" }
    tracker._configure(aurora_np)

def test_close():
    with pytest.raises(ValueError):
        tracker = NDITracker()
        tracker.close()

def test_read_sroms_from_file():
    tracker = NDITracker()
    tracker.connect(SETTINGS_DUMMY)
    with pytest.raises(ValueError):
        tracker._read_sroms_from_file()
    tracker.close()

def test_initialise_ports():
    tracker = NDITracker()
    tracker._device = None
    with pytest.raises(ValueError):
        tracker._initialise_ports()
    with pytest.raises(ValueError):
        tracker.close()

def test_enable_tools():
    tracker = NDITracker()
    tracker._device = None
    with pytest.raises(ValueError):
        tracker._enable_tools()
    with pytest.raises(ValueError):
        tracker.close()

def test_get_frame():
    tracker = NDITracker()
    tracker.connect(SETTINGS_DUMMY)
    port_handles, timestamps, framenumbers, \
        tracking, tracking_quality = tracker.get_frame()

    assert len(tracking) == 0

    dummy_two_rom = {
        "tracker type": "dummy",
        "romfiles" : [
            "../data/something_else.rom",
            "../data/8700339.rom"]
        }

    tracker.connect(dummy_two_rom)
    port_handles, timestamps, framenumbers, \
        tracking, tracking_quality = tracker.get_frame()
    assert len(tracking) == 2
    assert tracking[0].shape == (4,4)
    assert tracking[0].dtype == 'float64'

def test_get_tool_descriptions():
    tracker = NDITracker()
    tracker.connect(SETTINGS_DUMMY)
    descriptions = tracker.get_tool_descriptions()
    assert len(descriptions) == 0

    dummy_two_rom = {
        "tracker type": "dummy",
        "romfiles" : [
            "../data/something_else.rom",
            "../data/8700339.rom"]
        }

    tracker.connect(dummy_two_rom)
    descriptions = tracker.get_tool_descriptions()
    assert len(descriptions) == 2

def test_start_tracking():
    tracker = NDITracker()
    tracker.connect(SETTINGS_DUMMY)
    with pytest.raises(ValueError):
        tracker.start_tracking()
    tracker.close()

def test_stop_tracking():
    tracker = NDITracker()
    tracker.connect(SETTINGS_DUMMY)
    with pytest.raises(ValueError):
        tracker.stop_tracking()
    tracker.close()

def test_check_for_errors():
    tracker = NDITracker()
    tracker.connect(SETTINGS_DUMMY)
    with pytest.raises(ValueError):
        tracker._check_for_errors("dummy error")
    tracker.close()

