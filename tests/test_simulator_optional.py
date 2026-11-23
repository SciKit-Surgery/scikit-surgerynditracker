"""The basic tracker installation must not require the simulator package."""

import builtins
import pytest
from sksurgerynditracker.nditracker import NDITracker


def test_simulator_missing(mocker):
    """Missing optional functionality gives actionable installation guidance."""
    original_import = builtins.__import__

    def without_simulator(name, *args, **kwargs):
        if name == 'ndicapi_sim':
            raise ModuleNotFoundError('No simulator', name='ndicapi_sim')
        return original_import(name, *args, **kwargs)

    mocker.patch('builtins.__import__', side_effect=without_simulator)
    tracker = NDITracker({'tracker type': 'dummy'})
    tracker.start_tracking()
    tracker.close()
    with pytest.raises(ImportError,
                       match=r'scikit-surgerynditracker\[simulator\]'):
        NDITracker({'tracker type': 'simulator'})


def test_optional_broken_import(mocker):
    """Do not disguise an installed package's internal import failures."""
    original_import = builtins.__import__

    def broken_simulator(name, *args, **kwargs):
        if name == 'ndicapi_sim':
            raise ModuleNotFoundError('Missing internal dependency',
                                      name='broken_internal_dependency')
        return original_import(name, *args, **kwargs)

    mocker.patch('builtins.__import__', side_effect=broken_simulator)
    with pytest.raises(ModuleNotFoundError) as error:
        NDITracker({'tracker type': 'simulator'})
    assert error.value.name == 'broken_internal_dependency'
