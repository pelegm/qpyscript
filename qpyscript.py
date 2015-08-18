"""
.. qpyscript.py

General framework for quick scripts.
"""

## System
import sys

## Argument parsing
import argparse as ap
from .pyslext.argparsing import HelpFormatter, StoreDatetime

## Console output
from .pyslext.console import csi, xcolor, nocolor


class Argument(object):
    """ A command line argument data holder. """
    def __init__(self, flags, action=None, nargs=None, const=None,
        default=None, type=None, choices=None, required=None, help=None,
        metavar=None, dest=None, group=None):
        self.flags = flags
        self.action = action
        self.nargs = nargs
        self.const = const
        self.default = default
        self.type = type
        self.choices = choices
        self.required = required
        self.help = help
        self.metavar = metavar
        self.dest = dest
        self.group = group

    @property
    def args(self):
        return self.flags

    @property
    def kwargs(self):
        _kwargs = {}
        for key in ['action', 'nargs', 'const', 'default', 'type', 'choices',
                    'required', 'help', 'metavar', 'dest']:
            value = getattr(self, key)
            if value is None:
                continue
            _kwargs[key] = value
        return _kwargs


## Main class
class Script(object):
    DEBUG_COL = 37
    INFO_COL = 61
    WARNING_COL = 125
    ERROR_COL = 160
    OK_COL = 64

    prog = None
    description = None
    epilog = None
    version = None
    arguments = []

    def __init__(self):
        ## Set and parse command line arguments
        ap_kwargs = {}
        ap_kwargs['prog'] = self.prog
        ap_kwargs['description'] = self.description
        ap_kwargs['epilog'] = self.epilog
        ap_kwargs['version'] = self.version
        arg_parser = ap.ArgumentParser(
            formatter_class=HelpFormatter, **ap_kwargs)
        for arg in self.arguments:
            arg_parser.add_argument(*arg.args, **arg.kwargs)

        ## Parse
        for key, value in dict(vars(arg_parser.parse_args())).viewitems():
            setattr(self, key, value)

    def exit(self, exit_code=None):
        sys.exit(exit_code)

    def _prompt(self, msg, title, color):
        print(xcolor(color) + title[0].upper() + " :: " + nocolor() + msg)

    def debug(self, msg):
        self._prompt(msg, "debug", self.DEBUG_COL)

    def info(self, msg):
        self._prompt(msg, "info", self.INFO_COL)

    def warning(self, msg):
        self._prompt(msg, "warning", self.WARNING_COL)

    def error(self, msg):
        self._prompt(msg, "error", self.ERROR_COL)

    def critical(self, msg, exit_code=1):
        self.error(msg)
        self.exit(exit_code)

    def ok(self, msg):
        self._prompt(msg, 'k', self.OK_COL)

    def run(self):
        pass
