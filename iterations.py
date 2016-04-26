"""
.. iterations.py

This module implements a number of :term:`iterator` building blocks,
inspired by Python's built-in module `itertools`_.

.. _itertools: http://docs.python.org/2/library/itertools.html
"""

## Framework
import itertools as it
import operator as op


## Infinity
inf = float('inf')


###################################
## ----- General functions ----- ##
###################################

def accumulate(iterable, func=op.add):
    """ Return running totals (partial sum :term:`generator`).

    :param iterable: the iterable to accumulate.
    :type iterable: :term:`iterable`
    :param func: the function to accumulate with.
    :type func: :class:`~.Callable`
    :rtype: :term:`generator`

    Examples:

    >>> accumulate([1, 2, 3, 4, 5])  # --> 1 3 6 10 15
    >>> accumulate([1, 2, 3, 4, 5], op.mul)  # --> 1 2 6 24 120
    """
    it = iter(iterable)
    total = next(it)
    yield total
    for element in it:
        total = func(total, element)
        yield total


def append(iterable, element):
    """ Append *element* to the "end" of *iterable*. """
    return chain(iterable, (element,))


def grouper(iterable, n):
    """ Collect data into fixed-length chunks or blocks.

    :param iterable: the iterable from which fixed-length chunks should be
       taken.
    :type iterable: :term:`iterable`
    :param n: the length of the chunks.
    :type n: :class:`int`
    :rtype: :term:`generator`

    Example:

    >>> grouper('ABCDEFG', 3)  # --> ABC DEF
    """
    args = [iter(iterable)] * n
    return it.izip(*args)


def mzip(mapping):
    """ Return a zipped version of a mapping of iterables, as an iterable
    (like :func:`it.izip`).

    :param mapping: the mapping to be zipped
    :type iterable: :term:`mapping`
    :rtype: :term:`generator`

    Example:

    >>> list(mzip({"a": [1, 2, 3], "b": (2, 3), "c": [3, 4, 5, 6]}))
    [{'a': 1, 'b': 2, 'c': 3}, {'a': 2, 'b': 3, 'c': 4}]
    """
    keys, values = unzip(mapping.iteritems())
    return (dict(it.izip(keys, val_tup)) for val_tup in it.izip(*values))


def pairwise(iterable):
    """ Return a :term:`generator` of pairs of following items of iterable.

    :param iterable: the iterable from which pairs of items should be taken.
    :type iterable: :term:`iterable`
    :rtype: :term:`generator`

    Example:

    >>> pairwise([0, 1, 2, 3])  # --> (0, 1), (1, 2), (2, 3)
    """
    a, b = it.tee(iterable)
    next(b, None)
    return it.izip(a, b)


def powerset(sequence, minsize=0, maxsize=inf):
    maxsize = min(maxsize, len(sequence))
    return chain.from_iterable(combinations(sequence, r)
                               for r in xrange(minsize, maxsize+1))


def roundrobin(*iterables):
    """ roundrobin('ABC', 'D', 'EF') --> A D E B F C """
    ## Recipe credited to George Sakkis
    pending = len(iterables)
    nexts = it.cycle(iter(iterable).next for iterable in iterables)
    while pending:
        try:
            for next in nexts:
                yield next()
        except StopIteration:
            pending -= 1
            nexts = it.cycle(islice(nexts, pending))


def sfilter(predicate, *iterables):
    """ Return a :term:`generator` of :term`tuples <tuple>` that are filtered
    simultaneously according to a given *predicate*, which operates on the
    zipped tuples of the given *iterables*.

    :param predicate: the filtering predicate.
    :type predicate: boolean function
    :param iterables: the family of iterables that should be filtered
        simultaneously.
    :type iterables: ``*args``

    Example:

    >>> without_None = lambda t: None not in t
    >>> x = [None, 1, 2, 3]; y = [2, 7, 3, 4]; z = [3, 4, 5, None]
    >>> x1, y1, z1 = sfilter(without_None, x, y, z)
    >>> x1, y1, z1
    ((1, 2), (7, 3), (4, 5))
    """
    return unzip(t for t in zip(*iterables) if predicate(t))


def substrings(string, maxlen=inf):
    ps = powerset(string, maxsize=maxlen)
    return ("".join(s) for s in ps)


def subtuples(tup, maxlen=inf):
    ps = powerset(tup, maxsize=maxlen)
    return (tuple(t) for t in ps)


def triwise(iterable):
    """ Return a :term:`generator` of triples of following items of iterable.

    :param iterable: the iterable from which triples of items should be taken.
    :type iterable: :term:`iterable`
    :rtype: :term:`generator`

    Example:

    >>> triwise([0, 1, 2, 3, 4])  # --> (0, 1, 2), (1, 2, 3), (2, 3, 4)
    """
    a, b, c = it.tee(iterable, 3)
    next(b, None)
    next(c, None)
    next(c, None)
    return it.izip(a, b, c)


def nwise(iterable, n=2):
    iters = it.tee(iterable, n)
    for i, j in enumerate(iters):
        next(islice(j, i, i), None)
    return it.izip(*iters)


def uniquify(iterable):
    """ Return a :term:`generator` of elements of *iterable*, without repeating
    any element. This function is order-preserving.

    :param iterable: the iterable to uniquify.
    :type iterable: :term:`iterable`
    :rtype: :term:`generator`

    Example:

    >>> list(uniquify([1, 2, 2, 3, 3, 5, 1, 4, 5, 4]))
    [1, 2, 3, 5, 4]

    .. warning:: any non-hashable element of the given *iterable* will be
                 generated, even if appears in the iterable more than once.
    """
    seen = set()
    for x in iterable:
        try:
            if x not in seen:
                seen.add(x)
                yield x
        except TypeError:
            yield x


def unzip(zipped):
    """ Return a :term:`generator` reverses the work of zip/it.izip.

    :param zipped: the iterable to unzip.
    :type zipped: :term:`iterable` of :term:`iterables <iterable>`.
    :rtype: :term:`generator`

    Examples:

    >>> list(unzip(zip(xrange(3), xrange(2, 5))))
    [(0, 1, 2), (2, 3, 4)]
    >>> list(unzip(it.izip(xrange(3), xrange(2, 5))))
    [(0, 1, 2), (2, 3, 4)]

    .. note:: The returned elements of the generator are always tuples.
              This is a result of how :func:`zip` works.
    """
    return it.izip(*zipped)


def transpose(zipped, n):
    """ Return *n* generators, where *n* is the number of elements in each of
    the zipped generators (they can have more, but only these will be
    considered).  """
    teed = it.tee(zipped, n)
    for i in xrange(n):
        gen = lambda teed, i=i: (e[i] for e in teed[i])
        yield gen(teed)
