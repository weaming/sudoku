from __future__ import print_function
import random
import sys


def some(seq):
    """Return some element of seq that is true."""
    for e in seq:
        if e:
            return e
    return False


def get_all(seq):
    rv = []
    for e in seq:
        if e:
            rv.append(e)
    if len(rv) > 1:
        print('Warning: multiple solves', file=sys.stderr)
    return rv


def from_file(filename, sep='\n'):
    """Parse a file into a list of strings, separated by sep."""
    return file(filename).read().strip().split(sep)


def shuffled(seq):
    "Return a randomly shuffled copy of the input sequence."
    seq = list(seq)
    random.shuffle(seq)
    return seq


def ensure_list(e):
    if not isinstance(e, (list, tuple, set)):
        return [e]
    return list(e)
