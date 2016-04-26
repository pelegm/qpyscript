"""
.. datetools.py

.. rubric:: Available datetime constants

* START_TIME (set to be 1/1/2000 at 00:00)

.. rubric:: Available timedelta constants

* SECOND
* MINUTE
* HOUR
* DAY
* WEEK
"""

## Datetime imports
import datetime
import pytz

## Library imports
import functools as fn


## Datetime constants
START_TIME = datetime.datetime(2000, 1, 1, 0, 0)
MAXTIME = datetime.datetime(year=datetime.MAXYEAR, month=12, day=31)

## Timedelta constants
SECOND = datetime.timedelta(seconds=1)
MINUTE = datetime.timedelta(minutes=1)
HOUR = datetime.timedelta(hours=1)
DAY = datetime.timedelta(days=1)
WEEK = datetime.timedelta(weeks=1)

now = datetime.datetime.now
utcnow = datetime.datetime.utcnow


def datetime_rounder(delta=MINUTE, start=START_TIME):
    """ Return a callable, which, given a datetime object, round it to
    particles of *delta* which are counted from *start*.

    Examples (using :func:`library.functions.is_clean`):

    >>> rounder = datetime_rounder()
    >>> is_clean(datetime.datetime(2000, 1, 1, 1), rounder)
    True
    >>> w_rounder = datetime_rounder(WEEK, datetime.datetime(2000, 1, 1))
    >>> is_clean(datetime.datetime(2000, 1, 6))
    False
    """
    return fn.partial(truncated_datetime, delta=delta, start=start)


def datetime_divmod(dt, delta, start=START_TIME):
    """ Return a pair (n, td) of an int and a timedelta objects, which are the
    quotient and remainder of a and b, using datetime long division.

    Example:

    >>> datetime_divmod(datetime.datetime(2000, 1, 16, 1), WEEK)
    (2, datetime.timedelta(1, 3600))
    """
    dt_seconds = total_seconds(dt, start=start)
    delta_seconds = delta.total_seconds()
    n, s = divmod(dt_seconds, delta_seconds)
    return int(n), datetime.timedelta(seconds=s)


def total_seconds(dt, start=START_TIME):
    """ Return the total seconds of the given datetime object *dt*, compared to
    *start*.

    :param dt: the datetime whose total seconds are returned.
    :type dt: :class:`datetime.datetime`
    :param start: the datetime from which total seconds are counted.
    :type start: :class:`datetime.datetime`
    :rtype: :class:`float`

    Examples:

    >>> total_seconds(datetime.datetime(2000, 1, 1, 1))
    3600.0
    >>> total_seconds(datetime.datetime(2013, 2, 24, 12, 37, 51),
    ...               start=datetime.datetime(2013, 2, 24, 12, 37))
    51.0
    """
    return (dt - start).total_seconds()


BASE = datetime.datetime(1970, 1, 1)


def timestamp(dt):
    """ Return seconds since epoch of the time. """
    return total_seconds(dt, BASE)


def dt(timestamp):
    """ Return the datetime that this timestamp corresponds to. """
    return BASE + datetime.timedelta(seconds=timestamp)


def truncated_datetime(dt, delta=MINUTE, start=START_TIME):
    """ Return the latest datetime object that is an integral multiplication of
    *delta* added to *start*, and that is not later than *dt*.

    :param dt: The datetime whose truncated datetime is returned.
    :type dt: :class:`datetime.datetime`
    :param rounder: The timedelta to multiply by an integer to get the
      truncated value.
    :type rounder: :class:`datetime.timedelta`
    :param start: The datetime from which total seconds are counted.
    :type start: :class:`datetime.datetime`
    :rtype: :class:`datetime.datetime`

    Examples:

    >>> truncated_datetime(datetime.datetime(2013, 2, 24, 12, 37, 51))
    datetime.datetime(2013, 2, 24, 12, 37)
    >>> truncated_datetime(datetime.datetime(2013, 2, 24, 12, 37, 51),
                           datetime.timedelta(seconds=12))
    datetime.datetime(2013, 2, 24, 12, 37, 48)
    """
    r_diff = total_seconds(dt, start=start) % delta.total_seconds()
    return dt - datetime.timedelta(seconds=r_diff)


############################
## ----- Time Zones ----- ##
############################

_tz_utc = pytz.timezone("Etc/UTC")
_tz_ny = pytz.timezone("America/New_York")


def ny_dt(dt=datetime.datetime.now(tz=_tz_utc)):
    """ Return the time at NYC at *dt*. """
    return _tz_ny.fromutc(dt.replace(tzinfo=_tz_ny))


######################################
## ----- Formatting Functions ----- ##
######################################

DATEFORMAT = "%Y-%m-%d %H:%M:%S.%f"


def datetime2str(dt):
    """ Return a string representation of *dt*, which is similar to iso format
    but more consistent.

    :param dt: The datetime to format.
    :type dt: :class:`datetime.datetime`
    :rtype: :class:`str`

    Example:

    >>> datetime2str(datetime.datetime(2013, 2, 24, 12, 37, 51))
    '2013-02-24 12:37:51.000000'
    """
    return dt.strftime(DATEFORMAT)


def str2datetime(s):
    """ Return a :class:`datetime.datetime` object which is parsed from the
    string *s*, using the consistent iso format ``"%Y-%m-%d %H:%M:%S.%f"``.

    :param s: The string to parse.
    :type s: :class:`str`
    :rtype: :class:`datetime.datetime`

    Example:

    >>> str2datetime('2013-02-24 12:37:51.000000')
    datetime.datetime(2013, 2, 24, 12, 37, 51))

    .. seealso:: A faster version of this function:
                 :func:`str2datetime_fast`.
    """
    return datetime.datetime.strptime(s, DATEFORMAT)


def str2datetime_fast(s):
    """ Return a :class:`datetime.datetime` object which is parsed from the
    string *s*, using the consistent iso format ``%Y-%m-%d %H:%M:%S.%f``.

    :param s: The string to parse.
    :type s: :class:`str`
    :rtype: :class:`datetime.datetime`

    Example:

    >>> str2datetime_fast('2013-02-24 12:37:51.000000')
    datetime.datetime(2013, 2, 24, 12, 37, 51)

    .. note:: This is similar to :func:`str2datetime` but about 4-5 times
              faster.
    """
    year = int(s[0:4])
    month = int(s[5:7])
    day = int(s[8:10])
    hour = int(s[11:13])
    minute = int(s[14:16])
    second = int(s[17:19])
    micros = int(s[20:])
    dtup = year, month, day, hour, minute, second, micros
    return datetime.datetime(*dtup)


def utcts2dt(s):
    """ Return a :class:`datetime.datetime` object which is parsed from the
    string *s*, using the following utc format: ``%Y%m%d %H:%M:%S.%f``, but in
    which ``%f`` is miliseconds and not microseconds.

    :param s: The string to parse.
    :type s: :class:`str`
    :rtype: :class:`datetime.datetime`

    Example:

    >>> utcts2dt('20130224 12:37:51.000')
    datetime.datetime(2013, 2, 24, 12, 37, 51))
    """
    year = int(s[0:4])
    month = int(s[4:6])
    day = int(s[6:8])
    hour = int(s[9:11])
    minute = int(s[12:14])
    second = int(s[15:17])
    milis = int(s[18:21])
    micros = milis * 1000
    dtup = year, month, day, hour, minute, second, micros
    return datetime.datetime(*dtup)


def dt2utcts(dt):
    """ Return a string timestamp of a datetime object. """
    return dt.strftime('%Y%m%d-%H:%M:%S.%f')[:-3]

