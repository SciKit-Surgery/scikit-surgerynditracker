# coding=utf-8

"""scikit-surgerynditracker tests"""

from sksurgerynditracker.ui.sksurgerynditracker_demo import run_demo

import six

# Pytest style

def test_using_pytest_sksurgerynditracker():
    console = True
    assert run_demo(console, "Hello World") == True

# Disable this test if root.mainloop is uncommented in
# run_demo()
def test_using_pytest_cookienewwithgitinit_withTK():
    try:
        import tkinter
        try:
            console=False
            assert run_demo(console, "Hello World") == True
        except tkinter.TclError:
            six.print_("Got TCL error, probably no DISPLAY set, that's OK.")
            assert True
        except:
            six.print_("Got another error (not TCL), that's not OK.")
            assert False

    except ModuleNotFoundError:
        six.print_("Got module not found on tkinter, please check your python installation")
        #we're not trying to test whether we have tkinter so this is ok
        assert True
    except ImportError:
        six.print_("Got import error on tkinter, please check your python installation")
        #we're not trying to test whether we have tkinter so this is ok
        assert True
    except:
        assert False

