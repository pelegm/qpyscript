"""
.. console.py
"""

## Screen manipulation.
import os

## Formatting text
import collections as col

## For cleaning up the terminal at the end of the run

## Non-blocking input.
import sys
import fcntl
import termios

## Constants
NAN = '--'


## General functions
def read_noblock(size=-1):
    """ Read at most 'size' chars from stdin, if they are already present.  If
    less than 'size' are present, return what is available at the moment.  If
    none are available, return ''.  Finally if size is negative then return all
    that is available. """

    fd = sys.stdin.fileno()

    oldterm = termios.tcgetattr(fd)
    newattr = termios.tcgetattr(fd)
    newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
    termios.tcsetattr(fd, termios.TCSANOW, newattr)

    oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

    try:
        try:
            c = sys.stdin.read(size)
        except IOError:
            c = ''
    finally:
        termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
        fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)

    return c


def _clear_screen():
    """ Works only on Linux! """
    os.system("clear")


def clear_repr(item):
    ## Item is callable
    if isinstance(item, (col.Callable)):
        ## Try to return the callable's name
        try:
            return "<{name}>".format(name=item.__name__)
        except AttributeError:
            pass

        ## Try to access an inner name
        try:
            return "<{name}>".format(name=item.func.__name__)
        except AttributeError:
            pass

        ## Fall to repr
        return repr(item)

    ## Item is a mapping
    if isinstance(item, col.Mapping):
        return repr(dict((k, clear_repr(v)) for k, v in item.iteritems()))

    ## Item is a sequence
    if isinstance(item, col.MutableSequence):
        try:
            return repr(list(clear_repr(x) for x in item))
        except RuntimeError:
            raise RuntimeError(item)

    ## Fall to repr
    return str(item)


########################################
## ----- Terminal Control Codes ----- ##
########################################
## See: http://en.wikipedia.org/wiki/ANSI_escape_code

def csi(n, x):
    return '\x1b[{n}{x}'.format(n=n, x=x)


## Movement
def up(n=1):
    return csi(n, 'A')


def down(n=1):
    return csi(n, 'B')


def right(n=1):
    return csi(n, 'C')


def left(n=1):
    return csi(n, 'D')


def next(n=1):
    return csi(n, 'E')


def prev(n=1):
    return csi(n, 'F')


## Colors
def bold():
    return csi(1, 'm')


_colors = dict(black=0, red=1, green=2, yellow=3, blue=4, magenta=5, cyan=6,
               white=7)


def color(clr, bold=False):
    """ *clr* may be either an integer from 0 to 7 or a known name. """
    try:
        clr_i = int(clr)
    except ValueError:
        clr_i = _colors[clr]
    n = str(30 + clr_i)
    k = ';1m' if bold else 'm'
    return csi(n, k)


def nocolor():
    return csi(0, 'm')


normal = reset = nocolor


def underline():
    return csi(4, 'm')


def xcolor(clr):
    """ *clr* may be an integer from 0 to 255. """
    k = ";5;{}m".format(clr)
    return csi(38, k)


## This fixes a bug with readline and color prompts
def color_prompt(s, clr):
    return "\001" + xcolor(clr) + "\002" + s + "\001" + nocolor() + "\002"


## Actions
def clear_line():
    return csi(0, 'K')


def clear_screen():
    return csi(2, 'J')


#############################
## ----- Decorations ----- ##
#############################

def plusminus(plus, minus, maxt, width, padded=False):
    pluses = min(int(width * 1.0 * plus / maxt), plus)
    minuses = min(int(width * 1.0 * minus / maxt), minus)
    plus_str = color('green') + "+" * pluses + nocolor()
    minus_str = color('red') + "-" * minuses + nocolor()
    string = plus_str + minus_str
    if padded:
        string += " " * (width - (pluses + minuses))
    return string
