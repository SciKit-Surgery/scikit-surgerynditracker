# coding=utf-8

"""scikit-surgerynditracker tests"""

#what testing can we do with out being attached to a tracker?
#What testing can we do when we are attached to a tracker?
#We could build a fake ndi tracker, that listens on a port
#and responds appropriately.

import pytest
from pytest_mock import MockerFixture
from serial.tools import list_ports
from sksurgerynditracker.nditracker import NDITracker
import ndicapy

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
    "ports to probe": 20,
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

class mockPort:
    device = 'bad port'

def mockndiProbe(port_name):
    if port_name == 'good port':
        return ndicapy.NDI_OKAY 

def mockndiOpen(port_name):
    if port_name == 'good port':
        return True

def mockndiGetError(device):
    return ndicapy.NDI_OKAY

def mockComports():
    mockPorts = [mockPort]*20
    mockPorts[5].device = 'good port'
    return mockPorts

def test_connect_serial_mock(mocker):
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
    tracker = NDITracker(SETTINGS_POLARIS)
    del tracker

