"""
.. argparsing.py

Extensions to the builtin argparse module.
"""

## Framework
import argparse as ap

## Parsing datetimes
import dateutil.parser as dp


################################
## ----- Custom Actions ----- ##
################################

class ProxyCount(ap.Action):
    def __init__(self, option_strings, dest, default=None, required=False,
                 help=None, proxy=lambda x: x):
        super(ProxyCount, self).__init__(
            option_strings=option_strings, dest=dest, nargs=0, default=default,
            required=required, help=help)
        self.proxy = proxy
        self.private = "_{}".format(self.dest)

    def __call__(self, parser, namespace, values, option_string=None):
        old_count = getattr(self, self.private, 0)
        setattr(self, self.private, old_count + 1)
        setattr(namespace, self.dest, self.proxy(getattr(self, self.private)))


class StoreDatetime(ap.Action):
    def __init__(self, option_strings, dest, default=None, required=False,
                 help=None, metavar=None):
        super(StoreDatetime, self).__init__(
            option_strings=option_strings, dest=dest, nargs=None,
            default=default, required=required, help=help, metavar=metavar)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, dp.parse(values))


###################################
## ----- Custom Formatters ----- ##
###################################

class HelpFormatter(ap.HelpFormatter):
    """ A simple Help Formatter which obeys the 79 chars convention. """
    def __init__(self, *args, **kwargs):
        kwargs.update(width=79)
        super(HelpFormatter, self).__init__(*args, **kwargs)
