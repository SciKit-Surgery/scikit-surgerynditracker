# coding=utf-8

"""scikit-surgerynditracker tests"""

import sksurgerynditracker.nditracker

# Pytest style

def test_connect():
    #what testing can we do with out being attached to a tracker?
    #What testing can we do when we are attached to a tracker?
    #Do we have we build a fake ndi tracker, that listens on a port
    #and responds appropriately. That could be another scikit
    #library
    assert True

def test_connect_network():
    assert True

def test_connect_serial():
    #could a fake ndi tracker impersonate a serial connection as well?.
    assert True

def test_configure():
    #here we can pass a variety of configuration dictionaries and check that
    #performance is as expected.
    assert True

def test_close():
    assert True

def test_read_SROMS_from_file():
    assert True

def test_initialise_ports():
    assert True

def test_enable_tools():
    assert True

def test_get_frame():
    assert True

def test_get_tool_descriptions():
    assert True

def test_StartTracking():
    assert True

def test_StopTracking():
    assert True

def test_CheckForErrors():
    assert True

