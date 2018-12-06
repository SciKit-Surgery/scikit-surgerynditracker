# coding=utf-8

"""scikit-surgerynditracker tests"""

import sksurgerynditracker.nditracker

# Pytest style

def test_Connect():
    #what testing can we do with out being attached to a tracker?
    #What testing can we do when we are attached to a tracker?
    #Do we have we build a fake ndi tracker, that listens on a port
    #and responds appropriately. That could be another scikit
    #library
    assert True

def test_ConnectNetwork():
    assert True

def test_ConnectSerial():
    #could a fake ndi tracker impersonate a serial connection as well?.
    assert True

def test_Configure():
    #here we can pass a variety of configuration dictionaries and check that
    #performance is as expected.
    assert True

def test_Close():
    assert True

def test_ReadSROMSFromFile():
    assert True

def test_InitialisePorts():
    assert True

def test_EnableTools():
    assert True

def test_GetFrame():
    assert True

def test_GetToolDescriptionsAndPortHandles():
    assert True

def test_StartTracking():
    assert True

def test_StopTracking():
    assert True

def test_CheckForErrors():
    assert True

