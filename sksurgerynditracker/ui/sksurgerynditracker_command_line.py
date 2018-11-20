# coding=utf-8

"""Command line processing"""


import argparse
from sksurgerynditracker import __version__
from sksurgerynditracker.ui.sksurgerynditracker_demo import run_demo


def main(args=None):
    """Entry point for scikit-surgerynditracker application"""

    parser = argparse.ArgumentParser(description='scikit-surgerynditracker')

    parser.add_argument("-t", "--text",
                        required=False,
                        default="This is scikit-surgerynditracker",
                        type=str,
                        help="Text to display")

    parser.add_argument("--console", required=False,
                        action='store_true',
                        help="If set, scikit-surgerynditracker "
                             "will not bring up a graphical user interface")

    version_string = __version__
    friendly_version_string = version_string if version_string else 'unknown'
    parser.add_argument(
        "-v", "--version",
        action='version',
        version='scikit-surgerynditracker version ' + friendly_version_string)

    args = parser.parse_args(args)

    run_demo(args.console, args.text)
