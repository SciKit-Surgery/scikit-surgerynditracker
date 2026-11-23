"""Integration checks, enabled only when the optional simulator is installed."""

import copy
import importlib
import importlib.util
import numpy as np
import pytest
from sksurgerynditracker.nditracker import NDITracker


@pytest.fixture(name='simulator')
def simulator_fixture():
    """Skip absent packages, but let broken installed packages fail normally."""
    if importlib.util.find_spec('ndicapi_sim') is None:
        pytest.skip('Optional ndicapi-sim package is not installed')
    return importlib.import_module('ndicapi_sim')


@pytest.fixture(autouse=True)
def no_hardware(mocker):
    """Simulation must never probe hardware or use the native API."""
    for target in ('serial.tools.list_ports.comports',
                   'sksurgerynditracker.nditracker.call',
                   'ndicapy.ndiProbe', 'ndicapy.ndiOpen',
                   'ndicapy.ndiOpenNetwork', 'ndicapy.ndiCommand'):
        mocker.patch(target, side_effect=AssertionError('Hardware API called'))


@pytest.mark.parametrize('options, descriptions', [
    ({'romfiles': ['missing/a.rom', 'missing/b.rom', 'missing/c.rom']},
     ['missing/a.rom', 'missing/b.rom', 'missing/c.rom']),
    ({'serial port': 'offline'}, ['simulator tool 1', 'simulator tool 2']),
    ({'romfiles': ['a.rom'], 'simulation': {'tool count': 2}},
     ['a.rom', 'simulator tool 2']),
    ({'romfiles': ['a.rom', 'b.rom'], 'simulation': {'tool count': 1}},
     ['a.rom']),
    ({'romfiles': []}, []),
    ({'romfiles': ['a.rom'], 'simulation': {'tool count': 0}}, []),
])
def test_configuration(simulator, options, descriptions):
    """Original settings infer tools, overridden only by explicit options."""
    del simulator  # The fixture verifies the optional dependency is available.
    settings = {'tracker type': 'simulator', 'ip address': 'offline',
                'foo1': 'bar1', **options}
    original = copy.deepcopy(settings)
    tracker = NDITracker(settings)
    try:
        tracker.start_tracking()
        handles, actual = tracker.get_tool_descriptions()
        assert actual == descriptions
        assert handles == list(range(1, len(descriptions) + 1))
        assert all(len(part) == len(descriptions)
                   for part in tracker.get_frame())
    finally:
        tracker.close()
    assert settings == original


@pytest.mark.parametrize('quaternions', [False, True])
def test_output_and_visibility(simulator, mocker, quaternions):
    """Existing formats and missing-data conversion apply to virtual tools."""
    clock = mocker.patch.object(simulator, 'monotonic', return_value=100.0)
    tracker = NDITracker({'tracker type': 'simulator',
                          'use quaternions': quaternions,
                          'simulation': {'seed': 42}})
    try:
        tracker.start_tracking()
        handles, _, frames, poses, quality = tracker.get_frame()
        assert handles == [1, 2]
        assert frames == [1, 1]
        assert all(pose.shape == ((1, 7) if quaternions else (4, 4))
                   for pose in poses)
        assert all(np.isfinite(pose).all() for pose in poses)
        assert all(0.01 <= value <= 0.2 for value in quality)
        clock.return_value = 104.0
        _, _, frames, poses, quality = tracker.get_frame()
        assert frames == [2, 2]
        assert np.isnan(quality).all()
        for pose in poses:
            assert np.isnan(pose if quaternions else pose[:3, :]).all()
        clock.return_value = 108.0
        assert all(np.isfinite(pose).all() for pose in tracker.get_frame()[3])
        tracker.stop_tracking()
        tracker.start_tracking()
        assert tracker.get_frame()[2] == [1, 1]
    finally:
        tracker.close()


def test_smoothing(simulator, mocker):
    """Simulator samples pass through the existing translation buffer."""
    clock = mocker.patch.object(simulator, 'monotonic', return_value=0.0)
    tracker = NDITracker({'tracker type': 'simulator', 'smoothing buffer': 2,
                          'simulation': {'seed': 42,
                                         'visibility interval': 0}})
    raw_tracker = NDITracker({'tracker type': 'simulator',
                              'simulation': {'seed': 42,
                                             'visibility interval': 0}})
    try:
        tracker.start_tracking()
        raw_tracker.start_tracking()
        first = tracker.get_frame()[3][0][:3, 3].copy()
        clock.return_value = 1.0
        smoothed = tracker.get_frame()[3][0][:3, 3]
        raw_second = raw_tracker.get_frame()[3][0][:3, 3]
        np.testing.assert_allclose(smoothed, (first + raw_second) / 2)
    finally:
        tracker.close()
        raw_tracker.close()


def test_playback_reserved(simulator):
    """Reserved playback must not silently generate circular data."""
    del simulator
    with pytest.raises(NotImplementedError, match='Playback'):
        NDITracker({'tracker type': 'simulator',
                    'simulation': {'mode': 'playback',
                                   'file': 'session.ndirec'}})
