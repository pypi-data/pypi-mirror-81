"""Data set of optimal circuits.

Data set of optimal circuits for Boolean functions that have
low arity.
"""

import doctest
import math
import logical

# The private dictionary that represents the data set.
class _db(dict):
    """
    Wrapper class for a circuit data set instance.
    """
    _data = {}

for i in range(1, 4):
    _db._data[i] = {
        frozenset([logical.id_, logical.not_, logical.and_, logical.or_]): {},
        frozenset([logical.id_, logical.not_, logical.and_, logical.xor_]): {},
        frozenset(logical.every): {}
    }

_db._data\
    [1]\
    [frozenset([logical.id_, logical.not_, logical.and_, logical.or_])]\
    [frozenset([logical.id_, logical.not_, logical.and_, logical.or_])]\
    = {
        (1, 0): [(logical.id_,), (logical.not_, 0)],
        (0, 1): [(logical.id_,), (logical.id_, 0)],
        (0, 0): [(logical.id_,), (logical.not_, 0), (logical.and_, 0, 1)],
        (1, 1): [(logical.id_,), (logical.not_, 0), (logical.or_, 0, 1)],
    }

_db._data\
    [2]\
    [frozenset([logical.id_, logical.not_, logical.and_, logical.or_])]\
    [frozenset([logical.id_, logical.not_, logical.and_, logical.or_])]\
    = {
        (1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.not_, 0)],
        (1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.not_, 1)],
        (0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_, 0)],
        (0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_, 1)],
        (0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.and_, 0, 1)],
        (0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.or_, 0, 1)],
        (0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 0, 2)],
        (0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 2)],
        (1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.not_, 0), (logical.or_, 0, 2)],
        (1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.not_, 0), (logical.or_, 1, 2)],
        (0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 0, 2)],
        (1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.not_, 1), (logical.or_, 0, 2)],
        (1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.not_, 2)],
        (1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.or_, 0, 1), (logical.not_, 2)],
        (0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.not_, 2), (logical.or_, 0, 1), (logical.and_, 3, 4)],
        (1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.or_, 0, 1), (logical.not_, 3), (logical.or_, 2, 4)],
    }

_db._data\
    [3]\
    [frozenset([logical.id_, logical.not_, logical.and_, logical.or_])]\
    [frozenset([logical.id_, logical.not_, logical.and_, logical.or_])]\
    = {
        (1, 1, 1, 1, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0)],
        (1, 1, 0, 0, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1)],
        (1, 0, 1, 0, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2)],
        (0, 0, 0, 0, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.id_, 0)],
        (0, 0, 1, 1, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.id_, 1)],
        (0, 1, 0, 1, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.id_, 2)],
        (0, 0, 0, 0, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1)],
        (0, 0, 0, 0, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2)],
        (0, 0, 0, 1, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2)],
        (0, 0, 1, 1, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 1)],
        (0, 1, 0, 1, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 2)],
        (0, 1, 1, 1, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 1, 2)],
        (0, 0, 0, 0, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 0, 3)],
        (0, 0, 1, 1, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 3)],
        (0, 1, 0, 1, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 2, 3)],
        (1, 1, 1, 1, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.or_, 0, 3)],
        (1, 1, 1, 1, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.or_, 1, 3)],
        (1, 1, 1, 1, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.or_, 2, 3)],
        (0, 0, 0, 0, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 0, 3)],
        (0, 1, 0, 0, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 2, 3)],
        (1, 1, 0, 0, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.or_, 0, 3)],
        (1, 1, 0, 1, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.or_, 2, 3)],
        (0, 0, 0, 0, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.and_, 0, 3)],
        (0, 0, 1, 0, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.and_, 1, 3)],
        (1, 0, 1, 0, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.or_, 0, 3)],
        (1, 0, 1, 1, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.or_, 1, 3)],
        (1, 1, 1, 1, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.not_, 3)],
        (0, 0, 0, 0, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.and_, 2, 3)],
        (0, 1, 0, 1, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.or_, 2, 3)],
        (1, 1, 1, 1, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.not_, 3)],
        (0, 0, 1, 1, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.or_, 1, 3)],
        (1, 1, 1, 0, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.not_, 3)],
        (0, 0, 0, 1, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.or_, 0, 3)],
        (1, 1, 0, 0, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 1), (logical.not_, 3)],
        (0, 0, 0, 1, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 1), (logical.and_, 2, 3)],
        (0, 1, 1, 1, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 1), (logical.or_, 2, 3)],
        (1, 0, 1, 0, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 2), (logical.not_, 3)],
        (0, 0, 0, 1, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 2), (logical.and_, 1, 3)],
        (1, 0, 0, 0, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 1, 2), (logical.not_, 3)],
        (0, 0, 0, 0, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 1, 2), (logical.and_, 0, 3)],
        (0, 0, 0, 1, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 2), (logical.and_, 3, 4)],
        (1, 1, 1, 1, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 2), (logical.or_, 3, 4)],
        (0, 1, 1, 1, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 3), (logical.or_, 2, 4)],
        (0, 1, 1, 1, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 2, 3), (logical.or_, 1, 4)],
        (0, 1, 1, 1, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.or_, 1, 2), (logical.and_, 3, 4)],
        (1, 1, 1, 1, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.or_, 1, 2), (logical.or_, 3, 4)],
        (0, 1, 0, 1, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.or_, 1, 3), (logical.and_, 2, 4)],
        (0, 0, 1, 1, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.or_, 2, 3), (logical.and_, 1, 4)],
        (0, 0, 0, 0, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 0, 2), (logical.and_, 3, 4)],
        (1, 1, 0, 0, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 0, 2), (logical.or_, 3, 4)],
        (0, 1, 0, 1, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 0, 3), (logical.or_, 2, 4)],
        (0, 1, 0, 0, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 2, 3), (logical.or_, 0, 4)],
        (0, 1, 0, 0, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.or_, 0, 2), (logical.and_, 3, 4)],
        (1, 1, 0, 1, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.or_, 0, 2), (logical.or_, 3, 4)],
        (0, 1, 0, 0, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.or_, 0, 3), (logical.and_, 2, 4)],
        (0, 0, 0, 0, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.or_, 2, 3), (logical.and_, 0, 4)],
        (0, 0, 0, 0, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.and_, 0, 1), (logical.and_, 3, 4)],
        (1, 0, 1, 0, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.and_, 0, 1), (logical.or_, 3, 4)],
        (0, 0, 1, 1, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.and_, 0, 3), (logical.or_, 1, 4)],
        (0, 0, 1, 0, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.and_, 1, 3), (logical.or_, 0, 4)],
        (0, 0, 1, 0, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.or_, 0, 1), (logical.and_, 3, 4)],
        (1, 0, 1, 1, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.or_, 0, 1), (logical.or_, 3, 4)],
        (0, 0, 1, 0, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.or_, 0, 3), (logical.and_, 1, 4)],
        (0, 0, 0, 0, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.or_, 1, 3), (logical.and_, 0, 4)],
        (0, 1, 0, 1, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.not_, 3), (logical.and_, 2, 4)],
        (1, 1, 1, 1, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.not_, 3), (logical.or_, 2, 4)],
        (1, 1, 1, 1, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.and_, 2, 3), (logical.not_, 4)],
        (1, 0, 1, 0, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.or_, 2, 3), (logical.not_, 4)],
        (0, 0, 1, 1, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.not_, 3), (logical.and_, 1, 4)],
        (1, 1, 1, 1, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.not_, 3), (logical.or_, 1, 4)],
        (1, 1, 0, 0, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.or_, 1, 3), (logical.not_, 4)],
        (0, 0, 0, 0, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.not_, 3), (logical.and_, 0, 4)],
        (1, 1, 1, 0, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.not_, 3), (logical.or_, 0, 4)],
        (1, 1, 1, 0, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.or_, 0, 3), (logical.not_, 4)],
        (0, 1, 0, 0, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 1), (logical.not_, 3), (logical.and_, 2, 4)],
        (1, 1, 0, 1, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 1), (logical.not_, 3), (logical.or_, 2, 4)],
        (1, 1, 1, 0, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 1), (logical.and_, 2, 3), (logical.not_, 4)],
        (1, 0, 0, 0, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 1), (logical.or_, 2, 3), (logical.not_, 4)],
        (0, 0, 1, 0, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 2), (logical.not_, 3), (logical.and_, 1, 4)],
        (1, 0, 1, 1, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 2), (logical.not_, 3), (logical.or_, 1, 4)],
        (1, 1, 1, 0, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 2), (logical.and_, 1, 3), (logical.not_, 4)],
        (0, 0, 0, 0, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 1, 2), (logical.not_, 3), (logical.and_, 0, 4)],
        (1, 0, 0, 0, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 1, 2), (logical.not_, 3), (logical.or_, 0, 4)],
        (1, 1, 1, 1, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 1, 2), (logical.and_, 0, 3), (logical.not_, 4)],
        (1, 1, 0, 1, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 1), (logical.and_, 2, 3), (logical.or_, 4, 5)],
        (1, 1, 1, 1, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 1), (logical.and_, 2, 4), (logical.or_, 3, 5)],
        (1, 1, 0, 0, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 1), (logical.or_, 2, 3), (logical.and_, 4, 5)],
        (1, 1, 0, 1, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 1), (logical.or_, 2, 4), (logical.and_, 3, 5)],
        (1, 0, 1, 1, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 2), (logical.and_, 1, 3), (logical.or_, 4, 5)],
        (1, 1, 1, 1, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 2), (logical.and_, 1, 4), (logical.or_, 3, 5)],
        (1, 0, 1, 0, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 2), (logical.or_, 1, 3), (logical.and_, 4, 5)],
        (1, 0, 1, 1, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 2), (logical.or_, 1, 4), (logical.and_, 3, 5)],
        (0, 1, 0, 1, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 0, 1), (logical.and_, 2, 3), (logical.or_, 4, 5)],
        (0, 0, 1, 1, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 0, 2), (logical.and_, 1, 3), (logical.or_, 4, 5)],
        (1, 0, 0, 0, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 3), (logical.or_, 2, 4), (logical.not_, 5)],
        (1, 0, 0, 0, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 2, 3), (logical.or_, 1, 4), (logical.not_, 5)],
        (1, 0, 1, 0, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.or_, 1, 3), (logical.and_, 2, 4), (logical.not_, 5)],
        (1, 1, 0, 0, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.or_, 2, 3), (logical.and_, 1, 4), (logical.not_, 5)],
        (0, 1, 0, 0, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 0, 1), (logical.and_, 2, 3), (logical.or_, 4, 5)],
        (0, 0, 0, 1, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 0, 3), (logical.and_, 1, 2), (logical.or_, 4, 5)],
        (0, 0, 1, 0, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.and_, 0, 2), (logical.and_, 1, 3), (logical.or_, 4, 5)],
        (0, 0, 0, 1, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.and_, 0, 3), (logical.and_, 1, 2), (logical.or_, 4, 5)],
        (0, 0, 1, 1, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.not_, 3), (logical.or_, 0, 1), (logical.and_, 4, 5)],
        (0, 1, 0, 1, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.not_, 3), (logical.or_, 0, 2), (logical.and_, 4, 5)],
        (0, 1, 1, 1, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.not_, 3), (logical.or_, 1, 2), (logical.and_, 4, 5)],
        (1, 1, 0, 0, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.or_, 0, 1), (logical.not_, 4), (logical.or_, 3, 5)],
        (0, 0, 0, 1, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.or_, 0, 1), (logical.and_, 2, 4), (logical.or_, 3, 5)],
        (1, 0, 1, 0, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.or_, 0, 2), (logical.not_, 4), (logical.or_, 3, 5)],
        (1, 0, 0, 0, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.or_, 1, 2), (logical.not_, 4), (logical.or_, 3, 5)],
        (0, 0, 1, 1, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.not_, 3), (logical.or_, 0, 1), (logical.and_, 4, 5)],
        (0, 1, 0, 1, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.not_, 3), (logical.or_, 0, 2), (logical.and_, 4, 5)],
        (0, 1, 1, 1, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.not_, 3), (logical.or_, 1, 2), (logical.and_, 4, 5)],
        (1, 1, 0, 0, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.or_, 0, 1), (logical.not_, 4), (logical.or_, 3, 5)],
        (1, 0, 1, 0, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.or_, 0, 2), (logical.not_, 4), (logical.or_, 3, 5)],
        (1, 0, 0, 0, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.or_, 1, 2), (logical.not_, 4), (logical.or_, 3, 5)],
        (0, 0, 1, 0, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.not_, 3), (logical.or_, 0, 1), (logical.and_, 4, 5)],
        (0, 1, 0, 0, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.not_, 3), (logical.or_, 0, 2), (logical.and_, 4, 5)],
        (0, 1, 1, 0, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.not_, 3), (logical.or_, 1, 2), (logical.and_, 4, 5)],
        (1, 1, 0, 1, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.or_, 0, 1), (logical.not_, 4), (logical.or_, 3, 5)],
        (1, 0, 1, 1, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.or_, 0, 2), (logical.not_, 4), (logical.or_, 3, 5)],
        (1, 0, 0, 1, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.or_, 1, 2), (logical.not_, 4), (logical.or_, 3, 5)],
        (1, 0, 1, 0, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 0, 1), (logical.and_, 2, 3), (logical.or_, 4, 5), (logical.not_, 6)],
        (1, 1, 0, 0, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 0, 2), (logical.and_, 1, 3), (logical.or_, 4, 5), (logical.not_, 6)],
        (1, 1, 1, 0, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 2), (logical.not_, 4), (logical.or_, 1, 3), (logical.and_, 5, 6)],
        (1, 1, 1, 0, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 2), (logical.not_, 4), (logical.or_, 2, 3), (logical.and_, 5, 6)],
        (0, 1, 1, 1, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 2), (logical.or_, 1, 2), (logical.and_, 3, 5), (logical.or_, 4, 6)],
        (1, 0, 1, 1, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 3), (logical.or_, 1, 2), (logical.not_, 5), (logical.or_, 4, 6)],
        (1, 1, 0, 1, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 2, 3), (logical.or_, 1, 2), (logical.not_, 5), (logical.or_, 4, 6)],
        (0, 1, 0, 0, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 0, 2), (logical.or_, 0, 2), (logical.and_, 3, 5), (logical.or_, 4, 6)],
        (0, 0, 1, 0, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.and_, 0, 1), (logical.or_, 0, 1), (logical.and_, 3, 5), (logical.or_, 4, 6)],
        (0, 0, 1, 1, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.not_, 3), (logical.and_, 0, 2), (logical.or_, 1, 5), (logical.and_, 4, 6)],
        (0, 0, 0, 1, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.not_, 3), (logical.and_, 1, 2), (logical.or_, 0, 5), (logical.and_, 4, 6)],
        (0, 0, 0, 1, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.not_, 3), (logical.and_, 2, 4), (logical.or_, 0, 1), (logical.and_, 5, 6)],
        (0, 1, 1, 1, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.not_, 3), (logical.or_, 0, 1), (logical.and_, 4, 5), (logical.or_, 2, 6)],
        (0, 0, 1, 1, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.not_, 3), (logical.or_, 0, 1), (logical.or_, 2, 4), (logical.and_, 5, 6)],
        (0, 1, 1, 1, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.not_, 3), (logical.or_, 0, 1), (logical.or_, 2, 5), (logical.and_, 4, 6)],
        (0, 1, 0, 1, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.and_, 0, 2), (logical.not_, 4), (logical.or_, 2, 3), (logical.and_, 5, 6)],
        (1, 1, 0, 0, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.and_, 0, 2), (logical.or_, 1, 4), (logical.not_, 5), (logical.or_, 3, 6)],
        (1, 0, 1, 0, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.and_, 0, 2), (logical.or_, 2, 3), (logical.not_, 5), (logical.or_, 4, 6)],
        (0, 1, 0, 0, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.and_, 1, 2), (logical.not_, 4), (logical.or_, 2, 3), (logical.and_, 5, 6)],
        (1, 1, 1, 0, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.and_, 1, 2), (logical.or_, 0, 4), (logical.not_, 5), (logical.or_, 3, 6)],
        (1, 0, 1, 1, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.and_, 1, 2), (logical.or_, 2, 3), (logical.not_, 5), (logical.or_, 4, 6)],
        (0, 0, 1, 1, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.and_, 2, 3), (logical.not_, 4), (logical.or_, 0, 1), (logical.and_, 5, 6)],
        (0, 1, 0, 1, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.and_, 2, 3), (logical.not_, 4), (logical.or_, 0, 2), (logical.and_, 5, 6)],
        (0, 1, 1, 1, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.and_, 2, 3), (logical.not_, 4), (logical.or_, 1, 2), (logical.and_, 5, 6)],
        (0, 1, 0, 1, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.and_, 2, 3), (logical.not_, 4), (logical.or_, 2, 3), (logical.and_, 5, 6)],
        (1, 1, 0, 0, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.and_, 2, 3), (logical.or_, 0, 1), (logical.not_, 5), (logical.or_, 4, 6)],
        (1, 0, 1, 0, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.and_, 2, 3), (logical.or_, 0, 2), (logical.not_, 5), (logical.or_, 4, 6)],
        (1, 0, 0, 0, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.and_, 2, 3), (logical.or_, 1, 2), (logical.not_, 5), (logical.or_, 4, 6)],
        (1, 0, 1, 0, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.and_, 2, 3), (logical.or_, 2, 3), (logical.not_, 5), (logical.or_, 4, 6)],
        (0, 1, 0, 0, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.or_, 0, 1), (logical.not_, 4), (logical.and_, 2, 5), (logical.or_, 3, 6)],
        (1, 1, 0, 1, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.or_, 0, 1), (logical.not_, 4), (logical.or_, 2, 3), (logical.or_, 5, 6)],
        (0, 1, 0, 0, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.or_, 0, 1), (logical.not_, 4), (logical.or_, 3, 5), (logical.and_, 2, 6)],
        (1, 1, 1, 0, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.or_, 0, 1), (logical.and_, 2, 4), (logical.not_, 5), (logical.or_, 3, 6)],
        (1, 1, 1, 0, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.or_, 0, 1), (logical.and_, 2, 4), (logical.or_, 3, 5), (logical.not_, 6)],
        (0, 0, 1, 0, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.or_, 0, 1), (logical.or_, 2, 3), (logical.not_, 5), (logical.and_, 4, 6)],
        (1, 0, 0, 0, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.or_, 0, 1), (logical.or_, 2, 4), (logical.not_, 5), (logical.or_, 3, 6)],
        (0, 0, 0, 1, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.not_, 3), (logical.and_, 1, 2), (logical.or_, 0, 5), (logical.and_, 4, 6)],
        (0, 0, 0, 1, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.not_, 3), (logical.and_, 1, 4), (logical.or_, 0, 2), (logical.and_, 5, 6)],
        (0, 1, 1, 1, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.not_, 3), (logical.or_, 0, 1), (logical.or_, 2, 5), (logical.and_, 4, 6)],
        (0, 1, 1, 1, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.not_, 3), (logical.or_, 0, 2), (logical.and_, 4, 5), (logical.or_, 1, 6)],
        (0, 1, 0, 1, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.not_, 3), (logical.or_, 0, 2), (logical.or_, 1, 4), (logical.and_, 5, 6)],
        (0, 0, 1, 0, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.and_, 1, 2), (logical.not_, 4), (logical.or_, 1, 3), (logical.and_, 5, 6)],
        (1, 1, 1, 0, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.and_, 1, 2), (logical.or_, 0, 4), (logical.not_, 5), (logical.or_, 3, 6)],
        (1, 1, 0, 1, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.and_, 1, 2), (logical.or_, 1, 3), (logical.not_, 5), (logical.or_, 4, 6)],
        (0, 0, 1, 1, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.and_, 1, 3), (logical.not_, 4), (logical.or_, 1, 3), (logical.and_, 5, 6)],
        (1, 1, 0, 0, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.and_, 1, 3), (logical.or_, 1, 3), (logical.not_, 5), (logical.or_, 4, 6)],
        (1, 0, 0, 0, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.or_, 0, 1), (logical.or_, 2, 4), (logical.not_, 5), (logical.or_, 3, 6)],
        (0, 0, 1, 0, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.or_, 0, 2), (logical.not_, 4), (logical.and_, 1, 5), (logical.or_, 3, 6)],
        (1, 0, 1, 1, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.or_, 0, 2), (logical.not_, 4), (logical.or_, 1, 3), (logical.or_, 5, 6)],
        (0, 0, 1, 0, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.or_, 0, 2), (logical.not_, 4), (logical.or_, 3, 5), (logical.and_, 1, 6)],
        (1, 1, 1, 0, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.or_, 0, 2), (logical.and_, 1, 4), (logical.not_, 5), (logical.or_, 3, 6)],
        (0, 1, 0, 0, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.or_, 0, 2), (logical.or_, 1, 3), (logical.not_, 5), (logical.and_, 4, 6)],
        (0, 0, 0, 0, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.not_, 3), (logical.and_, 0, 4), (logical.or_, 1, 2), (logical.and_, 5, 6)],
        (0, 1, 1, 0, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.not_, 3), (logical.or_, 0, 1), (logical.or_, 2, 5), (logical.and_, 4, 6)],
        (0, 1, 1, 0, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.not_, 3), (logical.or_, 0, 4), (logical.or_, 1, 2), (logical.and_, 5, 6)],
        (0, 1, 1, 0, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.not_, 3), (logical.or_, 1, 2), (logical.and_, 4, 5), (logical.or_, 0, 6)],
        (0, 0, 0, 1, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.and_, 0, 3), (logical.not_, 4), (logical.or_, 0, 3), (logical.and_, 5, 6)],
        (1, 1, 1, 0, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.and_, 0, 3), (logical.or_, 0, 3), (logical.not_, 5), (logical.or_, 4, 6)],
        (1, 0, 0, 1, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.or_, 0, 1), (logical.or_, 2, 4), (logical.not_, 5), (logical.or_, 3, 6)],
        (0, 1, 1, 0, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.or_, 0, 3), (logical.not_, 4), (logical.or_, 1, 2), (logical.and_, 5, 6)],
        (1, 0, 0, 1, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.or_, 0, 3), (logical.or_, 1, 2), (logical.not_, 5), (logical.or_, 4, 6)],
        (0, 0, 0, 1, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.or_, 1, 2), (logical.not_, 4), (logical.and_, 0, 5), (logical.or_, 3, 6)],
        (0, 0, 0, 0, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.or_, 1, 2), (logical.not_, 4), (logical.or_, 3, 5), (logical.and_, 0, 6)],
        (1, 1, 1, 1, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.or_, 1, 2), (logical.and_, 0, 4), (logical.not_, 5), (logical.or_, 3, 6)],
        (1, 1, 0, 1, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 1), (logical.not_, 3), (logical.or_, 0, 2), (logical.and_, 1, 5), (logical.or_, 4, 6)],
        (1, 1, 0, 0, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 1), (logical.not_, 3), (logical.or_, 1, 2), (logical.and_, 0, 5), (logical.or_, 4, 6)],
        (0, 1, 0, 0, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 1), (logical.and_, 2, 3), (logical.not_, 4), (logical.or_, 0, 2), (logical.and_, 5, 6)],
        (0, 1, 1, 0, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 1), (logical.and_, 2, 3), (logical.not_, 4), (logical.or_, 1, 2), (logical.and_, 5, 6)],
        (0, 1, 1, 0, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 1), (logical.and_, 2, 3), (logical.not_, 4), (logical.or_, 2, 3), (logical.and_, 5, 6)],
        (1, 0, 1, 1, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 1), (logical.and_, 2, 3), (logical.or_, 0, 2), (logical.not_, 5), (logical.or_, 4, 6)],
        (1, 0, 0, 1, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 1), (logical.and_, 2, 3), (logical.or_, 1, 2), (logical.not_, 5), (logical.or_, 4, 6)],
        (1, 0, 0, 1, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 1), (logical.and_, 2, 3), (logical.or_, 2, 3), (logical.not_, 5), (logical.or_, 4, 6)],
        (0, 0, 1, 0, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 1), (logical.or_, 0, 2), (logical.and_, 1, 4), (logical.not_, 5), (logical.and_, 3, 6)],
        (0, 0, 1, 1, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 1), (logical.or_, 1, 2), (logical.and_, 0, 4), (logical.not_, 5), (logical.and_, 3, 6)],
        (1, 0, 1, 0, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 2), (logical.not_, 3), (logical.or_, 1, 2), (logical.and_, 0, 5), (logical.or_, 4, 6)],
        (0, 1, 1, 0, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 2), (logical.and_, 1, 3), (logical.not_, 4), (logical.or_, 1, 2), (logical.and_, 5, 6)],
        (0, 1, 1, 0, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 2), (logical.and_, 1, 3), (logical.not_, 4), (logical.or_, 1, 3), (logical.and_, 5, 6)],
        (1, 0, 0, 1, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 2), (logical.and_, 1, 3), (logical.or_, 1, 2), (logical.not_, 5), (logical.or_, 4, 6)],
        (1, 0, 0, 1, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 2), (logical.and_, 1, 3), (logical.or_, 1, 3), (logical.not_, 5), (logical.or_, 4, 6)],
        (0, 1, 0, 1, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 2), (logical.or_, 1, 2), (logical.and_, 0, 4), (logical.not_, 5), (logical.and_, 3, 6)],
        (0, 1, 1, 1, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 1, 2), (logical.and_, 0, 3), (logical.not_, 4), (logical.or_, 0, 3), (logical.and_, 5, 6)],
        (1, 0, 0, 0, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 1, 2), (logical.and_, 0, 3), (logical.or_, 0, 3), (logical.not_, 5), (logical.or_, 4, 6)],
        (1, 1, 0, 1, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 1), (logical.and_, 2, 3), (logical.or_, 2, 3), (logical.and_, 4, 6), (logical.or_, 5, 7)],
        (1, 0, 1, 1, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 2), (logical.and_, 1, 3), (logical.or_, 1, 3), (logical.and_, 4, 6), (logical.or_, 5, 7)],
        (1, 1, 1, 1, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 2), (logical.not_, 4), (logical.or_, 1, 2), (logical.and_, 5, 6), (logical.or_, 3, 7)],
        (1, 1, 1, 0, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 2), (logical.not_, 4), (logical.or_, 1, 2), (logical.or_, 3, 6), (logical.and_, 5, 7)],
        (1, 0, 0, 1, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 2), (logical.and_, 3, 4), (logical.or_, 1, 2), (logical.not_, 6), (logical.or_, 5, 7)],
        (1, 0, 0, 1, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 2), (logical.or_, 1, 2), (logical.not_, 5), (logical.or_, 4, 6), (logical.and_, 3, 7)],
        (1, 0, 0, 0, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 2), (logical.or_, 1, 2), (logical.and_, 3, 5), (logical.or_, 4, 6), (logical.not_, 7)],
        (1, 0, 1, 1, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 3), (logical.and_, 2, 3), (logical.or_, 1, 5), (logical.not_, 6), (logical.or_, 4, 7)],
        (1, 1, 0, 1, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 3), (logical.and_, 2, 3), (logical.or_, 2, 4), (logical.not_, 6), (logical.or_, 5, 7)],
        (0, 1, 1, 0, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 3), (logical.and_, 2, 4), (logical.not_, 5), (logical.or_, 2, 4), (logical.and_, 6, 7)],
        (1, 0, 0, 1, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 3), (logical.and_, 2, 4), (logical.or_, 2, 4), (logical.not_, 6), (logical.or_, 5, 7)],
        (1, 0, 1, 1, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 3), (logical.or_, 1, 3), (logical.and_, 2, 5), (logical.not_, 6), (logical.or_, 4, 7)],
        (1, 0, 0, 0, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 3), (logical.or_, 1, 3), (logical.or_, 2, 4), (logical.not_, 6), (logical.and_, 5, 7)],
        (0, 1, 1, 0, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 2, 3), (logical.and_, 1, 4), (logical.not_, 5), (logical.or_, 1, 4), (logical.and_, 6, 7)],
        (1, 0, 0, 1, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 2, 3), (logical.and_, 1, 4), (logical.or_, 1, 4), (logical.not_, 6), (logical.or_, 5, 7)],
        (1, 0, 0, 0, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 2, 3), (logical.or_, 1, 4), (logical.not_, 5), (logical.or_, 2, 3), (logical.and_, 6, 7)],
        (1, 1, 0, 1, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 2, 3), (logical.or_, 2, 3), (logical.and_, 1, 5), (logical.not_, 6), (logical.or_, 4, 7)],
        (1, 0, 1, 0, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.or_, 1, 3), (logical.and_, 2, 4), (logical.not_, 5), (logical.or_, 2, 3), (logical.and_, 6, 7)],
        (1, 0, 1, 0, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.or_, 1, 3), (logical.and_, 2, 4), (logical.not_, 5), (logical.or_, 2, 4), (logical.and_, 6, 7)],
        (0, 1, 0, 1, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.or_, 1, 3), (logical.and_, 2, 4), (logical.or_, 2, 4), (logical.not_, 6), (logical.or_, 5, 7)],
        (1, 1, 0, 0, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.or_, 1, 3), (logical.or_, 2, 3), (logical.and_, 1, 5), (logical.not_, 6), (logical.and_, 4, 7)],
        (1, 1, 0, 0, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.or_, 2, 3), (logical.and_, 1, 4), (logical.not_, 5), (logical.or_, 1, 4), (logical.and_, 6, 7)],
        (0, 0, 1, 1, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.or_, 2, 3), (logical.and_, 1, 4), (logical.or_, 1, 4), (logical.not_, 6), (logical.or_, 5, 7)],
        (0, 1, 0, 0, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 2, 3), (logical.and_, 0, 4), (logical.not_, 5), (logical.or_, 0, 4), (logical.and_, 6, 7)],
        (1, 0, 1, 1, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 2, 3), (logical.and_, 0, 4), (logical.or_, 0, 4), (logical.not_, 6), (logical.or_, 5, 7)],
        (1, 1, 0, 1, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.or_, 2, 3), (logical.and_, 0, 4), (logical.not_, 5), (logical.or_, 0, 4), (logical.and_, 6, 7)],
        (0, 0, 1, 0, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.or_, 2, 3), (logical.and_, 0, 4), (logical.or_, 0, 4), (logical.not_, 6), (logical.or_, 5, 7)],
        (0, 1, 1, 1, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.and_, 2, 3), (logical.not_, 4), (logical.or_, 0, 1), (logical.or_, 2, 6), (logical.and_, 5, 7)],
        (1, 0, 0, 0, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.and_, 2, 3), (logical.or_, 0, 1), (logical.or_, 2, 5), (logical.not_, 6), (logical.or_, 4, 7)],
        (0, 1, 0, 0, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.or_, 0, 1), (logical.and_, 2, 4), (logical.not_, 5), (logical.or_, 2, 3), (logical.and_, 6, 7)],
        (1, 0, 1, 1, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.or_, 0, 1), (logical.and_, 2, 4), (logical.or_, 2, 3), (logical.not_, 6), (logical.or_, 5, 7)],
        (0, 0, 1, 0, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.or_, 0, 2), (logical.and_, 1, 4), (logical.not_, 5), (logical.or_, 1, 3), (logical.and_, 6, 7)],
        (1, 1, 0, 1, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.or_, 0, 2), (logical.and_, 1, 4), (logical.or_, 1, 3), (logical.not_, 6), (logical.or_, 5, 7)],
        (1, 1, 1, 0, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.or_, 0, 3), (logical.not_, 4), (logical.or_, 1, 2), (logical.and_, 0, 6), (logical.or_, 5, 7)],
        (0, 0, 0, 1, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.or_, 0, 3), (logical.or_, 1, 2), (logical.and_, 0, 5), (logical.not_, 6), (logical.and_, 4, 7)],
        (0, 0, 0, 1, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.and_, 2, 3), (logical.not_, 4), (logical.or_, 0, 1), (logical.and_, 2, 6), (logical.or_, 3, 7), (logical.and_, 5, 8)],
        (1, 1, 1, 0, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.and_, 2, 3), (logical.or_, 0, 1), (logical.and_, 2, 5), (logical.or_, 3, 6), (logical.not_, 7), (logical.or_, 4, 8)],
        (0, 0, 1, 0, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.and_, 2, 3), (logical.or_, 0, 1), (logical.or_, 2, 3), (logical.not_, 6), (logical.and_, 5, 7), (logical.or_, 4, 8)],
        (0, 1, 1, 0, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.or_, 0, 1), (logical.and_, 2, 4), (logical.not_, 5), (logical.or_, 2, 4), (logical.and_, 6, 7), (logical.or_, 3, 8)],
        (1, 0, 0, 1, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.or_, 0, 1), (logical.and_, 2, 4), (logical.or_, 2, 4), (logical.not_, 6), (logical.or_, 3, 5), (logical.or_, 7, 8)],
        (0, 1, 1, 0, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.or_, 0, 1), (logical.and_, 2, 4), (logical.or_, 2, 4), (logical.or_, 3, 5), (logical.not_, 7), (logical.and_, 6, 8)],
        (0, 1, 0, 0, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.and_, 1, 3), (logical.or_, 0, 2), (logical.or_, 1, 3), (logical.not_, 6), (logical.and_, 5, 7), (logical.or_, 4, 8)],
        (0, 1, 1, 0, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.or_, 0, 2), (logical.and_, 1, 4), (logical.not_, 5), (logical.or_, 1, 4), (logical.and_, 6, 7), (logical.or_, 3, 8)],
        (0, 1, 1, 0, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.and_, 0, 3), (logical.or_, 0, 3), (logical.not_, 5), (logical.or_, 1, 2), (logical.and_, 6, 7), (logical.or_, 4, 8)],
        (0, 1, 1, 1, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.or_, 1, 2), (logical.and_, 0, 4), (logical.not_, 5), (logical.or_, 0, 4), (logical.and_, 6, 7), (logical.or_, 3, 8)],
        (1, 0, 1, 1, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.and_, 1, 3), (logical.or_, 0, 2), (logical.or_, 1, 3), (logical.not_, 6), (logical.and_, 5, 7), (logical.or_, 4, 8), (logical.not_, 9)],
        (1, 0, 0, 1, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.and_, 0, 3), (logical.or_, 0, 3), (logical.not_, 5), (logical.or_, 1, 2), (logical.and_, 6, 7), (logical.or_, 4, 8), (logical.not_, 9)],
        (1, 0, 0, 1, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.or_, 0, 2), (logical.and_, 1, 4), (logical.not_, 5), (logical.or_, 1, 4), (logical.and_, 6, 7), (logical.or_, 3, 8), (logical.not_, 9)],
        (1, 0, 0, 1, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.or_, 0, 1), (logical.and_, 2, 4), (logical.not_, 5), (logical.or_, 2, 4), (logical.and_, 6, 7), (logical.or_, 3, 8), (logical.not_, 9)],
        (1, 0, 0, 0, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.or_, 1, 2), (logical.and_, 0, 4), (logical.not_, 5), (logical.or_, 0, 4), (logical.and_, 6, 7), (logical.or_, 3, 8), (logical.not_, 9)],
        (1, 1, 0, 1, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.and_, 2, 3), (logical.or_, 0, 1), (logical.or_, 2, 3), (logical.not_, 6), (logical.and_, 5, 7), (logical.or_, 4, 8), (logical.not_, 9)],
        (0, 1, 1, 0, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.not_, 3), (logical.or_, 0, 1), (logical.and_, 4, 5), (logical.and_, 2, 6), (logical.not_, 7), (logical.or_, 2, 6), (logical.and_, 8, 9)],
        (1, 0, 0, 1, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.or_, 1, 2), (logical.not_, 4), (logical.or_, 3, 5), (logical.and_, 0, 6), (logical.not_, 7), (logical.or_, 0, 6), (logical.and_, 8, 9)],
    }

_db._data\
    [1]\
    [frozenset([logical.id_, logical.not_, logical.and_, logical.xor_])]\
    [frozenset([logical.and_])]\
    = {
        (1, 0): [(logical.id_,), (logical.not_, 0)],
        (0, 1): [(logical.id_,), (logical.id_, 0)],
        (0, 0): [(logical.id_,), (logical.not_, 0), (logical.not_, 0), (logical.xor_, 1, 2)],
        (1, 1): [(logical.id_,), (logical.not_, 0), (logical.xor_, 0, 1)],
    }

_db._data\
    [2]\
    [frozenset([logical.id_, logical.not_, logical.and_, logical.xor_])]\
    [frozenset([logical.and_])]\
    = {
        (1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.not_, 0)],
        (1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.not_, 1)],
        (0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_, 0)],
        (0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_, 1)],
        (0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.and_, 0, 1)],
        (0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.xor_, 0, 1)],
        (0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 0), (logical.xor_, 2, 3)],
        (0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 2)],
        (1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.not_, 0), (logical.xor_, 0, 2)],
        (1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.not_, 0), (logical.xor_, 1, 2)],
        (0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 0, 2)],
        (1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.not_, 2)],
        (1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 1), (logical.and_, 2, 3)],
        (1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 0, 1), (logical.xor_, 2, 3)],
        (1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 2), (logical.not_, 3)],
        (0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 2), (logical.xor_, 0, 3)],
    }

_db._data\
    [3]\
    [frozenset([logical.id_, logical.not_, logical.and_, logical.xor_])]\
    [frozenset([logical.and_])]\
    = {
        (1, 1, 1, 1, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0)],
        (1, 1, 0, 0, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1)],
        (1, 0, 1, 0, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2)],
        (0, 0, 0, 0, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.id_, 0)],
        (0, 0, 1, 1, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.id_, 1)],
        (0, 1, 0, 1, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.id_, 2)],
        (0, 0, 0, 0, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1)],
        (0, 0, 0, 0, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2)],
        (0, 0, 0, 1, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2)],
        (0, 0, 1, 1, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1)],
        (0, 1, 0, 1, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 2)],
        (0, 1, 1, 0, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 1, 2)],
        (0, 0, 0, 0, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 0), (logical.xor_, 3, 4)],
        (0, 0, 1, 1, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 3)],
        (0, 1, 0, 1, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 2, 3)],
        (1, 1, 1, 1, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.xor_, 0, 3)],
        (1, 1, 0, 0, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.xor_, 1, 3)],
        (1, 0, 1, 0, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.xor_, 2, 3)],
        (0, 0, 0, 0, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 0, 3)],
        (0, 1, 0, 0, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 2, 3)],
        (1, 0, 0, 1, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.xor_, 2, 3)],
        (0, 0, 0, 0, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.and_, 0, 3)],
        (0, 0, 1, 0, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.and_, 1, 3)],
        (1, 1, 1, 1, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.not_, 3)],
        (0, 0, 0, 0, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.and_, 2, 3)],
        (0, 1, 0, 1, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.xor_, 2, 3)],
        (1, 1, 1, 1, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.not_, 3)],
        (0, 0, 1, 1, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.xor_, 1, 3)],
        (1, 1, 1, 0, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.not_, 3)],
        (0, 0, 0, 1, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.xor_, 0, 3)],
        (0, 0, 0, 1, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.and_, 2, 3)],
        (0, 1, 1, 0, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.xor_, 2, 3)],
        (0, 0, 0, 1, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 2), (logical.and_, 1, 3)],
        (0, 0, 0, 0, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 1, 2), (logical.and_, 0, 3)],
        (1, 1, 0, 0, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 1), (logical.and_, 3, 4)],
        (1, 0, 1, 0, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 2), (logical.and_, 3, 4)],
        (1, 1, 1, 1, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 0, 1), (logical.xor_, 3, 4)],
        (1, 1, 1, 1, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 0, 2), (logical.xor_, 3, 4)],
        (0, 0, 0, 1, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 2), (logical.and_, 3, 4)],
        (1, 1, 1, 0, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 2), (logical.xor_, 3, 4)],
        (1, 1, 0, 0, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 3), (logical.not_, 4)],
        (0, 0, 1, 1, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 3), (logical.xor_, 0, 4)],
        (0, 1, 1, 0, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 3), (logical.xor_, 2, 4)],
        (1, 0, 1, 0, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 2, 3), (logical.not_, 4)],
        (0, 1, 0, 1, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 2, 3), (logical.xor_, 0, 4)],
        (0, 1, 1, 0, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 2, 3), (logical.xor_, 1, 4)],
        (0, 1, 1, 0, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.xor_, 1, 2), (logical.and_, 3, 4)],
        (1, 0, 0, 1, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.xor_, 1, 2), (logical.xor_, 3, 4)],
        (0, 1, 0, 0, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.xor_, 1, 3), (logical.and_, 2, 4)],
        (0, 0, 1, 0, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.xor_, 2, 3), (logical.and_, 1, 4)],
        (1, 0, 0, 0, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.not_, 2), (logical.and_, 3, 4)],
        (0, 0, 0, 0, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 0, 2), (logical.and_, 3, 4)],
        (1, 1, 0, 0, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 0, 2), (logical.xor_, 3, 4)],
        (0, 1, 0, 1, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 0, 3), (logical.xor_, 2, 4)],
        (1, 1, 0, 1, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 1, 2), (logical.xor_, 3, 4)],
        (1, 0, 1, 1, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 2, 3), (logical.not_, 4)],
        (0, 1, 0, 0, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 2, 3), (logical.xor_, 0, 4)],
        (0, 1, 1, 1, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 2, 3), (logical.xor_, 1, 4)],
        (0, 1, 0, 0, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.xor_, 0, 2), (logical.and_, 3, 4)],
        (0, 0, 0, 0, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.xor_, 2, 3), (logical.and_, 0, 4)],
        (0, 0, 0, 0, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.and_, 0, 1), (logical.and_, 3, 4)],
        (1, 0, 1, 0, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.and_, 0, 1), (logical.xor_, 3, 4)],
        (0, 0, 1, 1, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.and_, 0, 3), (logical.xor_, 1, 4)],
        (0, 0, 1, 0, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.and_, 1, 3), (logical.xor_, 0, 4)],
        (0, 0, 1, 0, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.xor_, 0, 1), (logical.and_, 3, 4)],
        (0, 1, 0, 1, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.not_, 3), (logical.and_, 2, 4)],
        (1, 1, 1, 1, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.and_, 2, 3), (logical.not_, 4)],
        (0, 0, 0, 0, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.and_, 2, 3), (logical.xor_, 0, 4)],
        (0, 0, 1, 1, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.and_, 2, 3), (logical.xor_, 1, 4)],
        (1, 1, 1, 0, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.and_, 2, 3), (logical.not_, 4)],
        (0, 0, 0, 1, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.and_, 2, 3), (logical.xor_, 0, 4)],
        (0, 0, 1, 0, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.and_, 2, 3), (logical.xor_, 1, 4)],
        (0, 0, 0, 1, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.xor_, 0, 2), (logical.and_, 3, 4)],
        (0, 0, 1, 0, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.xor_, 1, 2), (logical.and_, 3, 4)],
        (1, 1, 1, 0, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 2), (logical.and_, 1, 3), (logical.not_, 4)],
        (0, 0, 0, 1, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 2), (logical.and_, 1, 3), (logical.xor_, 0, 4)],
        (0, 1, 0, 0, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 2), (logical.and_, 1, 3), (logical.xor_, 2, 4)],
        (0, 1, 0, 0, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 2), (logical.xor_, 1, 2), (logical.and_, 3, 4)],
        (1, 1, 1, 1, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 1, 2), (logical.and_, 0, 3), (logical.not_, 4)],
        (0, 0, 1, 1, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 1, 2), (logical.and_, 0, 3), (logical.xor_, 1, 4)],
        (0, 1, 0, 1, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 1, 2), (logical.and_, 0, 3), (logical.xor_, 2, 4)],
        (0, 1, 0, 0, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 1), (logical.and_, 2, 3), (logical.and_, 4, 5)],
        (1, 0, 0, 1, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 1), (logical.and_, 2, 3), (logical.xor_, 4, 5)],
        (1, 0, 1, 1, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 1), (logical.and_, 2, 4), (logical.xor_, 3, 5)],
        (1, 0, 0, 1, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 1), (logical.and_, 3, 4), (logical.xor_, 2, 5)],
        (1, 0, 0, 0, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 1), (logical.xor_, 2, 3), (logical.and_, 4, 5)],
        (1, 0, 0, 1, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 1), (logical.xor_, 2, 4), (logical.and_, 3, 5)],
        (0, 0, 1, 0, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 2), (logical.and_, 1, 3), (logical.and_, 4, 5)],
        (1, 0, 0, 1, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 2), (logical.and_, 1, 3), (logical.xor_, 4, 5)],
        (1, 1, 0, 1, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 2), (logical.and_, 1, 4), (logical.xor_, 3, 5)],
        (1, 0, 0, 1, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 2), (logical.and_, 3, 4), (logical.xor_, 1, 5)],
        (1, 0, 0, 0, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 2), (logical.xor_, 1, 3), (logical.and_, 4, 5)],
        (1, 1, 1, 1, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 0, 1), (logical.and_, 2, 4), (logical.xor_, 3, 5)],
        (1, 0, 1, 0, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 0, 1), (logical.xor_, 2, 3), (logical.xor_, 4, 5)],
        (0, 1, 0, 1, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 0, 1), (logical.xor_, 3, 4), (logical.and_, 2, 5)],
        (1, 1, 0, 0, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 0, 2), (logical.xor_, 1, 3), (logical.xor_, 4, 5)],
        (0, 0, 1, 1, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 0, 2), (logical.xor_, 3, 4), (logical.and_, 1, 5)],
        (1, 1, 1, 0, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 2), (logical.not_, 4), (logical.and_, 3, 5)],
        (1, 1, 1, 0, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 2), (logical.and_, 3, 4), (logical.not_, 5)],
        (0, 0, 0, 1, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 2), (logical.and_, 3, 4), (logical.xor_, 0, 5)],
        (0, 0, 1, 0, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 2), (logical.and_, 3, 4), (logical.xor_, 1, 5)],
        (0, 1, 0, 0, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 2), (logical.and_, 3, 4), (logical.xor_, 2, 5)],
        (0, 1, 1, 0, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 3), (logical.xor_, 0, 2), (logical.xor_, 4, 5)],
        (0, 0, 0, 1, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 3), (logical.xor_, 0, 4), (logical.and_, 2, 5)],
        (0, 1, 1, 0, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 2, 3), (logical.xor_, 0, 1), (logical.xor_, 4, 5)],
        (0, 0, 0, 1, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 2, 3), (logical.xor_, 0, 4), (logical.and_, 1, 5)],
        (1, 1, 1, 0, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.xor_, 0, 1), (logical.and_, 2, 4), (logical.xor_, 3, 5)],
        (1, 1, 1, 0, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.xor_, 0, 2), (logical.and_, 1, 4), (logical.xor_, 3, 5)],
        (1, 1, 1, 1, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.xor_, 1, 2), (logical.and_, 0, 4), (logical.xor_, 3, 5)],
        (1, 0, 0, 1, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.xor_, 1, 2), (logical.and_, 3, 4), (logical.not_, 5)],
        (0, 1, 1, 0, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.xor_, 1, 2), (logical.and_, 3, 4), (logical.xor_, 0, 5)],
        (1, 0, 1, 1, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.xor_, 1, 3), (logical.and_, 2, 4), (logical.not_, 5)],
        (0, 1, 0, 0, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.xor_, 1, 3), (logical.and_, 2, 4), (logical.xor_, 0, 5)],
        (0, 1, 1, 1, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.xor_, 1, 3), (logical.and_, 2, 4), (logical.xor_, 1, 5)],
        (1, 0, 1, 1, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.xor_, 1, 3), (logical.and_, 2, 4), (logical.xor_, 3, 5)],
        (1, 0, 0, 0, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.xor_, 1, 3), (logical.xor_, 2, 3), (logical.and_, 4, 5)],
        (1, 1, 0, 1, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.xor_, 2, 3), (logical.and_, 1, 4), (logical.not_, 5)],
        (0, 0, 1, 0, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.xor_, 2, 3), (logical.and_, 1, 4), (logical.xor_, 0, 5)],
        (0, 1, 1, 1, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.xor_, 2, 3), (logical.and_, 1, 4), (logical.xor_, 2, 5)],
        (1, 1, 0, 1, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.xor_, 2, 3), (logical.and_, 1, 4), (logical.xor_, 3, 5)],
        (0, 0, 0, 0, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.not_, 2), (logical.and_, 0, 3), (logical.and_, 4, 5)],
        (1, 0, 0, 0, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.not_, 2), (logical.and_, 3, 4), (logical.xor_, 0, 5)],
        (1, 1, 0, 0, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 0, 1), (logical.and_, 2, 4), (logical.xor_, 3, 5)],
        (1, 1, 0, 0, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 0, 2), (logical.not_, 4), (logical.and_, 3, 5)],
        (1, 1, 1, 1, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 0, 2), (logical.and_, 3, 4), (logical.not_, 5)],
        (0, 0, 0, 0, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 0, 2), (logical.and_, 3, 4), (logical.xor_, 0, 5)],
        (0, 0, 1, 1, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 0, 2), (logical.and_, 3, 4), (logical.xor_, 1, 5)],
        (0, 0, 0, 0, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 1, 2), (logical.xor_, 3, 4), (logical.and_, 0, 5)],
        (0, 1, 1, 1, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 2, 3), (logical.xor_, 0, 1), (logical.xor_, 4, 5)],
        (0, 0, 0, 0, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 2, 3), (logical.xor_, 1, 4), (logical.and_, 0, 5)],
        (1, 1, 0, 1, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.xor_, 0, 1), (logical.and_, 2, 4), (logical.xor_, 3, 5)],
        (1, 0, 1, 1, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.xor_, 0, 2), (logical.and_, 3, 4), (logical.not_, 5)],
        (0, 1, 1, 1, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.xor_, 0, 2), (logical.and_, 3, 4), (logical.xor_, 1, 5)],
        (1, 0, 0, 0, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.xor_, 0, 3), (logical.and_, 2, 4), (logical.xor_, 3, 5)],
        (1, 1, 0, 0, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.xor_, 1, 2), (logical.and_, 0, 4), (logical.xor_, 3, 5)],
        (0, 0, 1, 1, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.xor_, 2, 3), (logical.and_, 0, 4), (logical.xor_, 1, 5)],
        (0, 1, 0, 1, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.xor_, 2, 3), (logical.and_, 0, 4), (logical.xor_, 2, 5)],
        (1, 1, 0, 0, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.xor_, 2, 3), (logical.and_, 0, 4), (logical.xor_, 3, 5)],
        (1, 0, 1, 0, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.and_, 0, 1), (logical.not_, 4), (logical.and_, 3, 5)],
        (1, 0, 1, 0, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.and_, 0, 1), (logical.and_, 2, 4), (logical.xor_, 3, 5)],
        (1, 1, 1, 1, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.and_, 0, 1), (logical.and_, 3, 4), (logical.not_, 5)],
        (0, 1, 0, 1, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.and_, 0, 1), (logical.and_, 3, 4), (logical.xor_, 2, 5)],
        (1, 1, 0, 1, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.xor_, 0, 1), (logical.and_, 3, 4), (logical.not_, 5)],
        (0, 1, 1, 1, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.xor_, 0, 1), (logical.and_, 3, 4), (logical.xor_, 2, 5)],
        (1, 0, 1, 1, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.xor_, 0, 2), (logical.and_, 1, 4), (logical.xor_, 3, 5)],
        (1, 0, 0, 0, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.xor_, 0, 3), (logical.and_, 1, 4), (logical.xor_, 3, 5)],
        (1, 0, 1, 0, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.xor_, 1, 2), (logical.and_, 0, 4), (logical.xor_, 3, 5)],
        (1, 0, 1, 0, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.xor_, 1, 3), (logical.and_, 0, 4), (logical.xor_, 3, 5)],
        (0, 1, 0, 1, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.not_, 3), (logical.and_, 2, 4), (logical.xor_, 0, 5)],
        (0, 1, 1, 0, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.not_, 3), (logical.and_, 2, 4), (logical.xor_, 1, 5)],
        (0, 1, 0, 1, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.not_, 3), (logical.xor_, 0, 2), (logical.and_, 4, 5)],
        (0, 1, 1, 0, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.not_, 3), (logical.xor_, 1, 2), (logical.and_, 4, 5)],
        (0, 0, 1, 1, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.and_, 2, 3), (logical.xor_, 0, 1), (logical.xor_, 4, 5)],
        (0, 0, 0, 1, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.xor_, 0, 2), (logical.and_, 3, 4), (logical.xor_, 0, 5)],
        (0, 1, 0, 1, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.xor_, 0, 2), (logical.xor_, 2, 3), (logical.and_, 4, 5)],
        (0, 1, 0, 0, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.xor_, 1, 2), (logical.xor_, 2, 3), (logical.and_, 4, 5)],
        (0, 0, 1, 1, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.not_, 3), (logical.xor_, 0, 1), (logical.and_, 4, 5)],
        (0, 1, 1, 0, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.not_, 3), (logical.xor_, 1, 2), (logical.and_, 4, 5)],
        (0, 0, 1, 1, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.xor_, 0, 1), (logical.xor_, 1, 3), (logical.and_, 4, 5)],
        (0, 0, 1, 0, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.xor_, 1, 2), (logical.xor_, 1, 3), (logical.and_, 4, 5)],
        (0, 0, 1, 0, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.not_, 3), (logical.xor_, 0, 1), (logical.and_, 4, 5)],
        (0, 1, 0, 0, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.not_, 3), (logical.xor_, 0, 2), (logical.and_, 4, 5)],
        (0, 0, 0, 1, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.xor_, 0, 1), (logical.xor_, 0, 3), (logical.and_, 4, 5)],
        (0, 0, 0, 1, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.xor_, 0, 2), (logical.xor_, 0, 3), (logical.and_, 4, 5)],
        (1, 1, 1, 0, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.xor_, 0, 2), (logical.and_, 3, 4), (logical.not_, 5)],
        (0, 0, 1, 0, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.xor_, 0, 2), (logical.and_, 3, 4), (logical.xor_, 1, 5)],
        (0, 1, 0, 0, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.xor_, 0, 2), (logical.and_, 3, 4), (logical.xor_, 2, 5)],
        (1, 1, 0, 1, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.xor_, 1, 2), (logical.and_, 3, 4), (logical.not_, 5)],
        (0, 1, 1, 1, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.xor_, 1, 2), (logical.and_, 3, 4), (logical.xor_, 2, 5)],
        (1, 0, 1, 1, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 2), (logical.xor_, 1, 2), (logical.and_, 3, 4), (logical.not_, 5)],
        (1, 0, 0, 0, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 1), (logical.not_, 2), (logical.and_, 3, 4), (logical.and_, 5, 6)],
        (1, 1, 1, 1, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 1), (logical.and_, 0, 2), (logical.and_, 4, 5), (logical.xor_, 3, 6)],
        (1, 1, 0, 0, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 1), (logical.and_, 0, 2), (logical.xor_, 3, 5), (logical.and_, 4, 6)],
        (1, 1, 0, 1, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 1), (logical.and_, 1, 2), (logical.and_, 3, 5), (logical.xor_, 4, 6)],
        (1, 1, 0, 1, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 1), (logical.and_, 1, 2), (logical.xor_, 4, 5), (logical.and_, 3, 6)],
        (1, 0, 0, 0, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 1), (logical.and_, 2, 3), (logical.not_, 5), (logical.and_, 4, 6)],
        (1, 0, 1, 1, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 1), (logical.and_, 2, 3), (logical.and_, 4, 5), (logical.not_, 6)],
        (0, 1, 0, 0, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 1), (logical.and_, 2, 3), (logical.and_, 4, 5), (logical.xor_, 0, 6)],
        (0, 1, 1, 1, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 1), (logical.and_, 2, 3), (logical.and_, 4, 5), (logical.xor_, 1, 6)],
        (1, 0, 1, 1, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 1), (logical.and_, 2, 3), (logical.and_, 4, 5), (logical.xor_, 3, 6)],
        (0, 1, 0, 0, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 1), (logical.and_, 2, 3), (logical.xor_, 0, 5), (logical.and_, 4, 6)],
        (0, 1, 1, 1, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 1), (logical.and_, 2, 4), (logical.xor_, 1, 5), (logical.and_, 3, 6)],
        (1, 1, 1, 1, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 2), (logical.and_, 0, 1), (logical.and_, 4, 5), (logical.xor_, 3, 6)],
        (1, 0, 1, 0, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 2), (logical.and_, 0, 1), (logical.xor_, 3, 5), (logical.and_, 4, 6)],
        (1, 0, 1, 1, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 2), (logical.and_, 1, 2), (logical.and_, 3, 5), (logical.xor_, 4, 6)],
        (1, 0, 0, 0, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 2), (logical.and_, 1, 3), (logical.not_, 5), (logical.and_, 4, 6)],
        (1, 1, 0, 1, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 2), (logical.and_, 1, 3), (logical.and_, 4, 5), (logical.not_, 6)],
        (0, 0, 1, 0, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 2), (logical.and_, 1, 3), (logical.and_, 4, 5), (logical.xor_, 0, 6)],
        (0, 1, 1, 1, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 2), (logical.and_, 1, 3), (logical.and_, 4, 5), (logical.xor_, 2, 6)],
        (0, 0, 1, 0, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 2), (logical.and_, 1, 3), (logical.xor_, 0, 5), (logical.and_, 4, 6)],
        (1, 0, 1, 0, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 0, 1), (logical.not_, 4), (logical.and_, 2, 5), (logical.xor_, 3, 6)],
        (1, 1, 0, 0, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 0, 1), (logical.and_, 2, 4), (logical.xor_, 1, 3), (logical.xor_, 5, 6)],
        (1, 0, 1, 0, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 0, 1), (logical.xor_, 2, 3), (logical.xor_, 3, 4), (logical.and_, 5, 6)],
        (1, 0, 1, 0, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 0, 1), (logical.xor_, 3, 4), (logical.and_, 2, 5), (logical.not_, 6)],
        (0, 1, 0, 1, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 0, 1), (logical.xor_, 3, 4), (logical.and_, 2, 5), (logical.xor_, 0, 6)],
        (1, 1, 0, 0, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 0, 2), (logical.xor_, 1, 3), (logical.xor_, 3, 4), (logical.and_, 5, 6)],
        (1, 1, 0, 0, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 0, 2), (logical.xor_, 3, 4), (logical.and_, 1, 5), (logical.not_, 6)],
        (0, 0, 1, 1, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 0, 2), (logical.xor_, 3, 4), (logical.and_, 1, 5), (logical.xor_, 0, 6)],
        (1, 1, 0, 1, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 2), (logical.not_, 4), (logical.and_, 3, 5), (logical.xor_, 1, 6)],
        (1, 0, 1, 1, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 2), (logical.not_, 4), (logical.and_, 3, 5), (logical.xor_, 2, 6)],
        (0, 1, 1, 1, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 2), (logical.and_, 3, 4), (logical.xor_, 1, 2), (logical.xor_, 5, 6)],
        (1, 0, 0, 0, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 3), (logical.not_, 4), (logical.xor_, 2, 3), (logical.and_, 5, 6)],
        (1, 1, 1, 0, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 3), (logical.xor_, 0, 4), (logical.and_, 2, 5), (logical.not_, 6)],
        (1, 1, 1, 0, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 3), (logical.xor_, 0, 4), (logical.and_, 2, 5), (logical.xor_, 3, 6)],
        (0, 0, 1, 0, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 3), (logical.xor_, 0, 4), (logical.and_, 2, 5), (logical.xor_, 4, 6)],
        (1, 0, 0, 0, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 2, 3), (logical.not_, 4), (logical.xor_, 1, 3), (logical.and_, 5, 6)],
        (1, 1, 1, 0, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 2, 3), (logical.xor_, 0, 4), (logical.and_, 1, 5), (logical.not_, 6)],
        (1, 1, 1, 0, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 2, 3), (logical.xor_, 0, 4), (logical.and_, 1, 5), (logical.xor_, 3, 6)],
        (0, 1, 0, 0, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 2, 3), (logical.xor_, 0, 4), (logical.and_, 1, 5), (logical.xor_, 4, 6)],
        (1, 1, 1, 0, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.xor_, 0, 1), (logical.xor_, 0, 2), (logical.and_, 4, 5), (logical.xor_, 3, 6)],
        (1, 1, 0, 1, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.xor_, 0, 1), (logical.xor_, 1, 2), (logical.and_, 4, 5), (logical.xor_, 3, 6)],
        (1, 0, 1, 1, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.xor_, 0, 2), (logical.xor_, 1, 2), (logical.and_, 4, 5), (logical.xor_, 3, 6)],
        (0, 1, 1, 1, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.xor_, 1, 3), (logical.xor_, 2, 3), (logical.and_, 4, 5), (logical.not_, 6)],
        (1, 0, 0, 0, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.xor_, 1, 3), (logical.xor_, 2, 3), (logical.and_, 4, 5), (logical.xor_, 0, 6)],
        (1, 1, 1, 1, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.not_, 2), (logical.and_, 0, 3), (logical.and_, 4, 5), (logical.not_, 6)],
        (0, 0, 1, 1, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.not_, 2), (logical.and_, 0, 3), (logical.and_, 4, 5), (logical.xor_, 1, 6)],
        (0, 1, 0, 1, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.not_, 2), (logical.and_, 0, 3), (logical.and_, 4, 5), (logical.xor_, 2, 6)],
        (1, 0, 0, 1, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 0, 1), (logical.not_, 4), (logical.and_, 2, 5), (logical.xor_, 3, 6)],
        (1, 0, 0, 0, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 0, 1), (logical.xor_, 2, 3), (logical.xor_, 3, 4), (logical.and_, 5, 6)],
        (1, 1, 0, 0, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 0, 2), (logical.not_, 4), (logical.and_, 3, 5), (logical.xor_, 0, 6)],
        (1, 0, 0, 1, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 0, 2), (logical.not_, 4), (logical.and_, 3, 5), (logical.xor_, 2, 6)],
        (1, 0, 0, 1, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 0, 3), (logical.not_, 4), (logical.xor_, 2, 3), (logical.and_, 5, 6)],
        (1, 1, 0, 1, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 0, 3), (logical.xor_, 1, 4), (logical.and_, 2, 5), (logical.xor_, 3, 6)],
        (0, 0, 0, 1, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 0, 3), (logical.xor_, 1, 4), (logical.and_, 2, 5), (logical.xor_, 4, 6)],
        (1, 1, 1, 1, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 2, 3), (logical.xor_, 1, 4), (logical.and_, 0, 5), (logical.not_, 6)],
        (1, 1, 0, 0, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 2, 3), (logical.xor_, 1, 4), (logical.and_, 0, 5), (logical.xor_, 3, 6)],
        (1, 0, 1, 0, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.and_, 0, 1), (logical.not_, 4), (logical.and_, 3, 5), (logical.xor_, 0, 6)],
        (1, 0, 0, 1, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.and_, 0, 1), (logical.not_, 4), (logical.and_, 3, 5), (logical.xor_, 1, 6)],
        (1, 0, 1, 1, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.and_, 0, 3), (logical.xor_, 2, 4), (logical.and_, 1, 5), (logical.xor_, 3, 6)],
        (1, 0, 1, 0, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.and_, 1, 3), (logical.xor_, 2, 4), (logical.and_, 0, 5), (logical.xor_, 3, 6)],
        (0, 1, 1, 0, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.not_, 3), (logical.and_, 2, 4), (logical.xor_, 0, 1), (logical.xor_, 5, 6)],
        (0, 1, 1, 0, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.not_, 3), (logical.xor_, 0, 2), (logical.and_, 4, 5), (logical.xor_, 1, 6)],
        (0, 0, 0, 1, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.xor_, 0, 1), (logical.xor_, 2, 3), (logical.xor_, 3, 4), (logical.and_, 5, 6)],
        (0, 0, 1, 0, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.xor_, 0, 1), (logical.xor_, 2, 4), (logical.xor_, 3, 4), (logical.and_, 5, 6)],
        (0, 1, 0, 0, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.xor_, 0, 2), (logical.xor_, 1, 4), (logical.xor_, 3, 4), (logical.and_, 5, 6)],
        (0, 1, 1, 0, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.xor_, 0, 2), (logical.xor_, 2, 3), (logical.and_, 4, 5), (logical.xor_, 1, 6)],
        (0, 1, 1, 0, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.not_, 3), (logical.xor_, 0, 1), (logical.and_, 4, 5), (logical.xor_, 2, 6)],
        (0, 1, 1, 1, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.not_, 3), (logical.xor_, 0, 1), (logical.and_, 4, 5), (logical.xor_, 2, 6)],
        (0, 1, 1, 1, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 1), (logical.not_, 2), (logical.and_, 3, 4), (logical.and_, 5, 6), (logical.not_, 7)],
        (1, 0, 0, 0, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 1), (logical.not_, 2), (logical.and_, 3, 4), (logical.and_, 5, 6), (logical.xor_, 0, 7)],
        (1, 0, 1, 1, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 1), (logical.not_, 2), (logical.and_, 3, 4), (logical.and_, 5, 6), (logical.xor_, 1, 7)],
        (1, 1, 0, 1, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 1), (logical.not_, 2), (logical.and_, 3, 4), (logical.and_, 5, 6), (logical.xor_, 2, 7)],
        (0, 1, 1, 1, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 1), (logical.and_, 2, 3), (logical.not_, 5), (logical.and_, 4, 6), (logical.xor_, 3, 7)],
        (1, 0, 1, 1, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 1), (logical.and_, 2, 3), (logical.xor_, 0, 5), (logical.and_, 4, 6), (logical.xor_, 3, 7)],
        (0, 1, 1, 1, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 2), (logical.and_, 1, 3), (logical.not_, 5), (logical.and_, 4, 6), (logical.xor_, 3, 7)],
        (1, 1, 0, 1, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 2), (logical.and_, 1, 3), (logical.xor_, 0, 5), (logical.and_, 4, 6), (logical.xor_, 3, 7)],
        (1, 0, 0, 1, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 0, 1), (logical.not_, 4), (logical.and_, 2, 5), (logical.xor_, 1, 3), (logical.xor_, 6, 7)],
        (1, 0, 0, 1, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 0, 1), (logical.not_, 4), (logical.xor_, 1, 2), (logical.and_, 5, 6), (logical.xor_, 3, 7)],
        (1, 0, 1, 1, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 0, 1), (logical.xor_, 1, 2), (logical.xor_, 2, 4), (logical.and_, 5, 6), (logical.xor_, 3, 7)],
        (1, 0, 0, 1, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 0, 1), (logical.xor_, 1, 2), (logical.xor_, 3, 4), (logical.and_, 5, 6), (logical.xor_, 3, 7)],
        (1, 0, 0, 0, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 0, 1), (logical.xor_, 2, 3), (logical.xor_, 1, 5), (logical.xor_, 4, 5), (logical.and_, 6, 7)],
        (1, 1, 0, 1, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 0, 2), (logical.xor_, 1, 2), (logical.xor_, 1, 4), (logical.and_, 5, 6), (logical.xor_, 3, 7)],
        (0, 1, 1, 0, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.not_, 2), (logical.and_, 0, 3), (logical.not_, 5), (logical.and_, 4, 6), (logical.xor_, 3, 7)],
        (1, 1, 1, 0, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.not_, 2), (logical.and_, 0, 3), (logical.xor_, 1, 5), (logical.and_, 4, 6), (logical.xor_, 3, 7)],
        (1, 0, 0, 1, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 0, 1), (logical.xor_, 0, 2), (logical.xor_, 2, 4), (logical.and_, 5, 6), (logical.xor_, 3, 7)],
        (1, 1, 1, 0, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.not_, 3), (logical.xor_, 0, 1), (logical.xor_, 3, 5), (logical.and_, 2, 6), (logical.xor_, 4, 7)],
    }

_db._data\
    [1]\
    [frozenset(logical.every)]\
    [frozenset(logical.every)]\
    = {
        (0, 0): [(logical.id_,), (logical.uf_, 0)],
        (0, 1): [(logical.id_,), (logical.id_, 0)],
        (1, 0): [(logical.id_,), (logical.not_, 0)],
        (1, 1): [(logical.id_,), (logical.ut_, 0)],
    }

_db._data\
    [2]\
    [frozenset(logical.every)]\
    [frozenset(logical.every)]\
    = {
        (0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.fst_, 0, 1)],
        (0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.snd_, 0, 1)],
        (1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.nfst_, 0, 1)],
        (1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.nsnd_, 0, 1)],
        (0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.bf_, 0, 1)],
        (1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.bt_, 0, 1)],
        (0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.and_, 0, 1)],
        (0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.nimp_, 0, 1)],
        (1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.if_, 0, 1)],
        (0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.nif_, 0, 1)],
        (0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.xor_, 0, 1)],
        (1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.nor_, 0, 1)],
        (0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.or_, 0, 1)],
        (1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.nand_, 0, 1)],
        (1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.xnor_, 0, 1)],
        (1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.imp_, 0, 1)],
    }

_db._data\
    [3]\
    [frozenset(logical.every)]\
    [frozenset(logical.every)]\
    = {
        (0, 0, 0, 0, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.id_, 0)],
        (0, 0, 1, 1, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.id_, 1)],
        (0, 1, 0, 1, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.id_, 2)],
        (1, 1, 1, 1, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0)],
        (1, 1, 0, 0, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1)],
        (1, 0, 1, 0, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2)],
        (0, 0, 0, 0, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.uf_, 0)],
        (1, 1, 1, 1, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.ut_, 0)],
        (0, 0, 0, 0, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1)],
        (0, 0, 0, 0, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2)],
        (0, 0, 0, 1, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2)],
        (0, 0, 0, 0, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 0, 1)],
        (0, 0, 0, 0, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 0, 2)],
        (0, 0, 1, 0, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 1, 2)],
        (1, 1, 0, 0, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 0, 1)],
        (1, 0, 1, 0, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 0, 2)],
        (1, 0, 1, 1, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 1, 2)],
        (0, 0, 1, 1, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nif_, 0, 1)],
        (0, 1, 0, 1, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nif_, 0, 2)],
        (0, 1, 0, 0, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nif_, 1, 2)],
        (0, 0, 1, 1, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1)],
        (0, 1, 0, 1, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 2)],
        (0, 1, 1, 0, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 1, 2)],
        (1, 1, 0, 0, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nor_, 0, 1)],
        (1, 0, 1, 0, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nor_, 0, 2)],
        (1, 0, 0, 0, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nor_, 1, 2)],
        (0, 0, 1, 1, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 1)],
        (0, 1, 0, 1, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 2)],
        (0, 1, 1, 1, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 1, 2)],
        (1, 1, 1, 1, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nand_, 0, 1)],
        (1, 1, 1, 1, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nand_, 0, 2)],
        (1, 1, 1, 0, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nand_, 1, 2)],
        (1, 1, 0, 0, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xnor_, 0, 1)],
        (1, 0, 1, 0, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xnor_, 0, 2)],
        (1, 0, 0, 1, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xnor_, 1, 2)],
        (1, 1, 1, 1, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.imp_, 0, 1)],
        (1, 1, 1, 1, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.imp_, 0, 2)],
        (1, 1, 0, 1, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.imp_, 1, 2)],
        (0, 0, 0, 0, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.and_, 2, 3)],
        (0, 1, 0, 1, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.nimp_, 2, 3)],
        (1, 1, 1, 1, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.if_, 2, 3)],
        (0, 0, 0, 0, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.nif_, 2, 3)],
        (0, 1, 0, 1, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.xor_, 2, 3)],
        (1, 0, 1, 0, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.nor_, 2, 3)],
        (0, 1, 0, 1, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.or_, 2, 3)],
        (1, 1, 1, 1, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.nand_, 2, 3)],
        (1, 0, 1, 0, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.xnor_, 2, 3)],
        (1, 0, 1, 0, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.imp_, 2, 3)],
        (0, 0, 1, 1, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.nimp_, 1, 3)],
        (1, 1, 1, 1, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.if_, 1, 3)],
        (0, 0, 0, 0, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.nif_, 1, 3)],
        (0, 0, 1, 1, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.xor_, 1, 3)],
        (1, 1, 0, 0, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.nor_, 1, 3)],
        (0, 0, 1, 1, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.or_, 1, 3)],
        (1, 1, 0, 0, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.xnor_, 1, 3)],
        (1, 1, 0, 0, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.imp_, 1, 3)],
        (0, 0, 0, 0, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.nimp_, 0, 3)],
        (1, 1, 1, 0, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.if_, 0, 3)],
        (0, 0, 0, 1, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.nif_, 0, 3)],
        (0, 0, 0, 1, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.xor_, 0, 3)],
        (1, 1, 1, 0, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.nor_, 0, 3)],
        (0, 0, 0, 1, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.or_, 0, 3)],
        (1, 1, 1, 0, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.xnor_, 0, 3)],
        (1, 1, 1, 1, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.imp_, 0, 3)],
        (0, 1, 0, 1, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 0, 1), (logical.nimp_, 2, 3)],
        (1, 1, 1, 1, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 0, 1), (logical.if_, 2, 3)],
        (0, 0, 0, 0, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 0, 1), (logical.nif_, 2, 3)],
        (0, 1, 0, 1, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 0, 1), (logical.xor_, 2, 3)],
        (1, 0, 1, 0, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 0, 1), (logical.nor_, 2, 3)],
        (0, 1, 0, 1, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 0, 1), (logical.or_, 2, 3)],
        (1, 0, 1, 0, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 0, 1), (logical.xnor_, 2, 3)],
        (1, 0, 1, 0, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 0, 1), (logical.imp_, 2, 3)],
        (0, 0, 1, 1, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 0, 2), (logical.nimp_, 1, 3)],
        (0, 0, 1, 1, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 0, 2), (logical.xor_, 1, 3)],
        (1, 1, 0, 0, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 0, 2), (logical.nor_, 1, 3)],
        (0, 0, 1, 1, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 0, 2), (logical.or_, 1, 3)],
        (1, 1, 0, 0, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 0, 2), (logical.xnor_, 1, 3)],
        (1, 1, 0, 0, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 0, 2), (logical.imp_, 1, 3)],
        (0, 0, 0, 0, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 1, 2), (logical.nimp_, 0, 3)],
        (1, 1, 0, 1, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 1, 2), (logical.if_, 0, 3)],
        (0, 0, 1, 0, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 1, 2), (logical.nif_, 0, 3)],
        (0, 0, 1, 0, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 1, 2), (logical.xor_, 0, 3)],
        (1, 1, 0, 1, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 1, 2), (logical.nor_, 0, 3)],
        (0, 0, 1, 0, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 1, 2), (logical.or_, 0, 3)],
        (1, 1, 0, 1, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 1, 2), (logical.xnor_, 0, 3)],
        (1, 1, 1, 1, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 1, 2), (logical.imp_, 0, 3)],
        (0, 1, 0, 0, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 0, 1), (logical.and_, 2, 3)],
        (0, 1, 1, 1, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 0, 1), (logical.if_, 2, 3)],
        (1, 0, 0, 0, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 0, 1), (logical.nif_, 2, 3)],
        (1, 0, 0, 1, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 0, 1), (logical.xor_, 2, 3)],
        (1, 0, 1, 1, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 0, 1), (logical.nand_, 2, 3)],
        (0, 1, 1, 0, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 0, 1), (logical.xnor_, 2, 3)],
        (0, 0, 1, 0, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 0, 2), (logical.and_, 1, 3)],
        (0, 1, 1, 1, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 0, 2), (logical.if_, 1, 3)],
        (1, 0, 0, 0, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 0, 2), (logical.nif_, 1, 3)],
        (1, 0, 0, 1, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 0, 2), (logical.xor_, 1, 3)],
        (0, 1, 0, 0, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 0, 2), (logical.nor_, 1, 3)],
        (1, 0, 1, 1, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 0, 2), (logical.or_, 1, 3)],
        (1, 1, 0, 1, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 0, 2), (logical.nand_, 1, 3)],
        (0, 1, 1, 0, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 0, 2), (logical.xnor_, 1, 3)],
        (0, 0, 0, 0, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 1, 2), (logical.and_, 0, 3)],
        (0, 1, 0, 0, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 1, 2), (logical.if_, 0, 3)],
        (1, 0, 1, 1, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 1, 2), (logical.nif_, 0, 3)],
        (1, 0, 1, 1, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 1, 2), (logical.xor_, 0, 3)],
        (1, 1, 1, 1, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 1, 2), (logical.nand_, 0, 3)],
        (0, 1, 0, 0, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 1, 2), (logical.xnor_, 0, 3)],
        (0, 0, 0, 1, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.and_, 2, 3)],
        (0, 1, 0, 0, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.nimp_, 2, 3)],
        (1, 1, 0, 1, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.if_, 2, 3)],
        (0, 0, 1, 0, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.nif_, 2, 3)],
        (0, 1, 1, 0, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.xor_, 2, 3)],
        (1, 0, 0, 0, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.nor_, 2, 3)],
        (0, 1, 1, 1, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.or_, 2, 3)],
        (1, 1, 1, 0, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.nand_, 2, 3)],
        (1, 0, 0, 1, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.xnor_, 2, 3)],
        (1, 0, 1, 1, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.imp_, 2, 3)],
        (0, 0, 0, 1, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 2), (logical.and_, 1, 3)],
        (0, 0, 1, 0, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 2), (logical.nimp_, 1, 3)],
        (1, 0, 1, 1, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 2), (logical.if_, 1, 3)],
        (0, 1, 0, 0, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 2), (logical.nif_, 1, 3)],
        (1, 0, 0, 0, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 2), (logical.nor_, 1, 3)],
        (0, 1, 1, 1, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 2), (logical.or_, 1, 3)],
        (1, 1, 1, 0, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 2), (logical.nand_, 1, 3)],
        (1, 1, 0, 1, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 2), (logical.imp_, 1, 3)],
        (0, 0, 0, 0, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 1, 2), (logical.and_, 0, 3)],
        (0, 0, 0, 0, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 1, 2), (logical.nimp_, 0, 3)],
        (1, 0, 0, 1, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 1, 2), (logical.if_, 0, 3)],
        (0, 1, 1, 0, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 1, 2), (logical.nif_, 0, 3)],
        (1, 0, 0, 1, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 1, 2), (logical.nor_, 0, 3)],
        (0, 1, 1, 0, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 1, 2), (logical.or_, 0, 3)],
        (1, 1, 1, 1, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 1, 2), (logical.nand_, 0, 3)],
        (1, 1, 1, 1, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 1, 2), (logical.imp_, 0, 3)],
        (0, 0, 0, 1, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nor_, 0, 1), (logical.nimp_, 2, 3)],
        (0, 1, 1, 1, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nor_, 0, 1), (logical.if_, 2, 3)],
        (1, 0, 0, 0, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nor_, 0, 1), (logical.nif_, 2, 3)],
        (1, 0, 0, 1, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nor_, 0, 1), (logical.xor_, 2, 3)],
        (0, 0, 1, 0, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nor_, 0, 1), (logical.nor_, 2, 3)],
        (1, 1, 0, 1, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nor_, 0, 1), (logical.or_, 2, 3)],
        (0, 1, 1, 0, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nor_, 0, 1), (logical.xnor_, 2, 3)],
        (1, 1, 1, 0, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nor_, 0, 1), (logical.imp_, 2, 3)],
        (0, 0, 0, 1, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nor_, 0, 2), (logical.nimp_, 1, 3)],
        (1, 0, 0, 1, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nor_, 0, 2), (logical.xor_, 1, 3)],
        (0, 1, 0, 0, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nor_, 0, 2), (logical.nor_, 1, 3)],
        (1, 0, 1, 1, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nor_, 0, 2), (logical.or_, 1, 3)],
        (0, 1, 1, 0, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nor_, 0, 2), (logical.xnor_, 1, 3)],
        (1, 1, 1, 0, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nor_, 0, 2), (logical.imp_, 1, 3)],
        (0, 0, 0, 0, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nor_, 1, 2), (logical.nimp_, 0, 3)],
        (1, 0, 0, 0, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nor_, 1, 2), (logical.xor_, 0, 3)],
        (0, 1, 1, 1, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nor_, 1, 2), (logical.nor_, 0, 3)],
        (1, 0, 0, 0, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nor_, 1, 2), (logical.or_, 0, 3)],
        (0, 1, 1, 1, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nor_, 1, 2), (logical.xnor_, 0, 3)],
        (1, 1, 1, 1, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nor_, 1, 2), (logical.imp_, 0, 3)],
        (0, 1, 0, 1, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.nimp_, 2, 3), (logical.xor_, 0, 4)],
        (0, 1, 1, 0, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.nimp_, 2, 3), (logical.xor_, 1, 4)],
        (1, 0, 1, 0, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.nimp_, 2, 3), (logical.xnor_, 0, 4)],
        (1, 0, 0, 1, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.nimp_, 2, 3), (logical.xnor_, 1, 4)],
        (0, 1, 0, 1, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.if_, 0, 2), (logical.if_, 3, 4)],
        (1, 0, 1, 0, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.if_, 0, 2), (logical.nif_, 3, 4)],
        (0, 1, 0, 0, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.if_, 1, 2), (logical.if_, 3, 4)],
        (1, 0, 1, 1, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.if_, 1, 2), (logical.nif_, 3, 4)],
        (1, 0, 1, 0, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.xor_, 0, 2), (logical.if_, 3, 4)],
        (0, 1, 0, 1, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.xor_, 0, 2), (logical.nif_, 3, 4)],
        (1, 0, 0, 1, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.xor_, 1, 2), (logical.if_, 3, 4)],
        (0, 1, 1, 0, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.xor_, 1, 2), (logical.nif_, 3, 4)],
        (1, 0, 1, 0, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.nor_, 0, 2), (logical.xor_, 3, 4)],
        (0, 1, 0, 1, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.nor_, 0, 2), (logical.nor_, 3, 4)],
        (1, 0, 0, 0, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.nor_, 1, 2), (logical.xor_, 3, 4)],
        (0, 1, 1, 1, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.nor_, 1, 2), (logical.nor_, 3, 4)],
        (0, 0, 1, 0, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.nimp_, 1, 2), (logical.xor_, 3, 4)],
        (1, 1, 0, 1, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.nimp_, 1, 2), (logical.nor_, 3, 4)],
        (0, 0, 1, 1, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.nimp_, 1, 3), (logical.xor_, 0, 4)],
        (1, 1, 0, 0, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.nimp_, 1, 3), (logical.xnor_, 0, 4)],
        (0, 0, 1, 1, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.if_, 0, 1), (logical.if_, 3, 4)],
        (1, 1, 0, 0, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.if_, 0, 1), (logical.nif_, 3, 4)],
        (1, 1, 0, 0, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.xor_, 0, 1), (logical.if_, 3, 4)],
        (0, 0, 1, 1, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.xor_, 0, 1), (logical.nif_, 3, 4)],
        (1, 0, 0, 1, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.xor_, 1, 2), (logical.if_, 3, 4)],
        (0, 1, 1, 0, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.xor_, 1, 2), (logical.nif_, 3, 4)],
        (1, 1, 0, 0, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.nor_, 0, 1), (logical.xor_, 3, 4)],
        (0, 0, 1, 1, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.nor_, 0, 1), (logical.nor_, 3, 4)],
        (1, 0, 0, 0, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.nor_, 1, 2), (logical.xor_, 3, 4)],
        (0, 1, 1, 1, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.nor_, 1, 2), (logical.nor_, 3, 4)],
        (0, 0, 0, 1, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.nimp_, 0, 1), (logical.xor_, 3, 4)],
        (1, 1, 1, 0, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.nimp_, 0, 1), (logical.nor_, 3, 4)],
        (0, 0, 0, 1, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.nimp_, 0, 2), (logical.xor_, 3, 4)],
        (1, 1, 1, 0, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.nimp_, 0, 2), (logical.nor_, 3, 4)],
        (1, 1, 0, 1, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.xor_, 0, 1), (logical.if_, 3, 4)],
        (0, 0, 1, 0, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.xor_, 0, 1), (logical.nif_, 3, 4)],
        (1, 0, 1, 1, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.xor_, 0, 2), (logical.if_, 3, 4)],
        (0, 1, 0, 0, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.xor_, 0, 2), (logical.nif_, 3, 4)],
        (1, 1, 0, 1, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.nor_, 0, 1), (logical.xor_, 3, 4)],
        (0, 0, 1, 0, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.nor_, 0, 1), (logical.nor_, 3, 4)],
        (1, 0, 1, 1, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.nor_, 0, 2), (logical.xor_, 3, 4)],
        (0, 1, 0, 0, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.nor_, 0, 2), (logical.nor_, 3, 4)],
        (0, 1, 0, 1, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 0, 1), (logical.nimp_, 2, 3), (logical.xor_, 0, 4)],
        (1, 0, 1, 0, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 0, 1), (logical.nimp_, 2, 3), (logical.xnor_, 0, 4)],
        (1, 0, 1, 0, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 0, 1), (logical.xor_, 0, 2), (logical.if_, 3, 4)],
        (0, 1, 0, 1, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 0, 1), (logical.xor_, 0, 2), (logical.nif_, 3, 4)],
        (1, 0, 0, 1, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 0, 1), (logical.xor_, 1, 2), (logical.nor_, 3, 4)],
        (0, 1, 1, 0, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 0, 1), (logical.xor_, 1, 2), (logical.or_, 3, 4)],
        (0, 0, 1, 1, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 0, 2), (logical.nimp_, 1, 3), (logical.xor_, 0, 4)],
        (1, 1, 0, 0, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 0, 2), (logical.nimp_, 1, 3), (logical.xnor_, 0, 4)],
        (1, 1, 0, 0, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 0, 2), (logical.xor_, 0, 1), (logical.if_, 3, 4)],
        (0, 0, 1, 1, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 0, 2), (logical.xor_, 0, 1), (logical.nif_, 3, 4)],
        (1, 1, 1, 0, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 1, 2), (logical.xor_, 0, 1), (logical.if_, 3, 4)],
        (0, 0, 0, 1, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 1, 2), (logical.xor_, 0, 1), (logical.nif_, 3, 4)],
        (1, 0, 0, 0, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 1, 2), (logical.xor_, 0, 2), (logical.nor_, 3, 4)],
        (0, 1, 1, 1, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 1, 2), (logical.xor_, 0, 2), (logical.or_, 3, 4)],
        (0, 1, 1, 1, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 0, 1), (logical.and_, 2, 3), (logical.xor_, 1, 4)],
        (1, 0, 0, 0, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 0, 1), (logical.and_, 2, 3), (logical.xnor_, 1, 4)],
        (0, 1, 0, 0, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 0, 1), (logical.if_, 2, 3), (logical.xor_, 1, 4)],
        (1, 0, 1, 1, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 0, 1), (logical.if_, 2, 3), (logical.xnor_, 1, 4)],
        (0, 1, 1, 1, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 0, 2), (logical.if_, 1, 3), (logical.xor_, 0, 4)],
        (0, 0, 1, 0, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 0, 2), (logical.if_, 1, 3), (logical.xor_, 2, 4)],
        (1, 0, 0, 0, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 0, 2), (logical.if_, 1, 3), (logical.xnor_, 0, 4)],
        (1, 1, 0, 1, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 0, 2), (logical.if_, 1, 3), (logical.xnor_, 2, 4)],
        (0, 0, 0, 1, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 1, 2), (logical.if_, 0, 3), (logical.xor_, 2, 4)],
        (1, 1, 1, 0, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 1, 2), (logical.if_, 0, 3), (logical.xnor_, 2, 4)],
        (0, 0, 0, 1, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.xor_, 0, 2), (logical.and_, 3, 4)],
        (0, 0, 1, 0, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.xor_, 0, 2), (logical.nimp_, 3, 4)],
        (1, 0, 1, 1, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.xor_, 0, 2), (logical.if_, 3, 4)],
        (0, 1, 0, 0, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.xor_, 0, 2), (logical.nif_, 3, 4)],
        (1, 0, 0, 0, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.xor_, 0, 2), (logical.nor_, 3, 4)],
        (0, 1, 1, 1, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.xor_, 0, 2), (logical.or_, 3, 4)],
        (1, 1, 1, 0, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.xor_, 0, 2), (logical.nand_, 3, 4)],
        (1, 1, 0, 1, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.xor_, 0, 2), (logical.imp_, 3, 4)],
        (0, 1, 0, 0, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.nor_, 0, 2), (logical.nor_, 3, 4)],
        (1, 0, 1, 1, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.nor_, 0, 2), (logical.or_, 3, 4)],
        (0, 0, 1, 0, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 2), (logical.nor_, 0, 1), (logical.nor_, 3, 4)],
        (1, 1, 0, 1, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 2), (logical.nor_, 0, 1), (logical.or_, 3, 4)],
        (0, 0, 0, 1, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 1, 2), (logical.nor_, 0, 1), (logical.nor_, 3, 4)],
        (1, 1, 1, 0, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 1, 2), (logical.nor_, 0, 1), (logical.or_, 3, 4)],
        (0, 1, 1, 0, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.nimp_, 2, 3), (logical.xor_, 0, 1), (logical.xor_, 4, 5)],
        (1, 0, 0, 1, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.nimp_, 2, 3), (logical.xor_, 0, 1), (logical.xnor_, 4, 5)],
        (1, 0, 0, 1, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.nimp_, 2, 3), (logical.nor_, 0, 1), (logical.xor_, 4, 5)],
        (0, 0, 1, 0, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.nimp_, 2, 3), (logical.nor_, 0, 1), (logical.nor_, 4, 5)],
        (1, 1, 0, 1, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.nimp_, 2, 3), (logical.nor_, 0, 1), (logical.or_, 4, 5)],
        (0, 1, 1, 0, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.nimp_, 2, 3), (logical.nor_, 0, 1), (logical.xnor_, 4, 5)],
        (0, 0, 0, 1, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.xor_, 0, 1), (logical.and_, 2, 4), (logical.xor_, 3, 5)],
        (1, 1, 1, 0, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.xor_, 0, 1), (logical.and_, 2, 4), (logical.nor_, 3, 5)],
        (0, 0, 0, 1, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.xor_, 2, 3), (logical.nor_, 0, 1), (logical.nimp_, 4, 5)],
        (0, 0, 1, 0, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.xor_, 2, 3), (logical.nor_, 0, 1), (logical.nor_, 4, 5)],
        (1, 1, 0, 1, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.xor_, 2, 3), (logical.nor_, 0, 1), (logical.or_, 4, 5)],
        (1, 1, 1, 0, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.xor_, 2, 3), (logical.nor_, 0, 1), (logical.imp_, 4, 5)],
        (1, 0, 0, 1, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.nimp_, 1, 3), (logical.nor_, 0, 2), (logical.xor_, 4, 5)],
        (0, 1, 0, 0, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.nimp_, 1, 3), (logical.nor_, 0, 2), (logical.nor_, 4, 5)],
        (1, 0, 1, 1, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.nimp_, 1, 3), (logical.nor_, 0, 2), (logical.or_, 4, 5)],
        (0, 1, 1, 0, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.nimp_, 1, 3), (logical.nor_, 0, 2), (logical.xnor_, 4, 5)],
        (0, 1, 0, 0, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.xor_, 1, 3), (logical.nor_, 0, 2), (logical.nor_, 4, 5)],
        (1, 0, 1, 1, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.xor_, 1, 3), (logical.nor_, 0, 2), (logical.or_, 4, 5)],
        (1, 0, 0, 0, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.nimp_, 0, 3), (logical.nor_, 1, 2), (logical.xor_, 4, 5)],
        (0, 1, 1, 1, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.nimp_, 0, 3), (logical.nor_, 1, 2), (logical.nor_, 4, 5)],
        (1, 0, 0, 0, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.nimp_, 0, 3), (logical.nor_, 1, 2), (logical.or_, 4, 5)],
        (0, 1, 1, 1, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.nimp_, 0, 3), (logical.nor_, 1, 2), (logical.xnor_, 4, 5)],
        (0, 1, 1, 0, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.xor_, 0, 3), (logical.nor_, 1, 2), (logical.nor_, 4, 5)],
        (1, 0, 0, 1, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.xor_, 0, 3), (logical.nor_, 1, 2), (logical.or_, 4, 5)],
    }

class circuitdb(dict):
    """
    Wrapper class for the circuit data set that supports both
    a dictionary-like interface and a function-like interface.
    """

    def __call__(self, truthtable, operators=None, minimize=None):
        """
        Function-like interface with user-friendly defaults to retrieve circuit data.

        >>> _d = _db._data
        >>> all(len(_d[1][o][m].keys()) == 4 for o in _d[1] for m in _d[1][o])
        True
        >>> all(len(_d[2][o][m].keys()) == 16 for o in _d[2] for m in _d[2][o])
        True
        >>> all(len(_d[3][o][m].keys()) == 256 for o in _d[3] for m in _d[3][o])
        True

        >>> circuitdb((0, 0))
        [((0, 1),), ((0, 0), 0)]
        >>> circuitdb((False, False))
        [((0, 1),), ((0, 0), 0)]
        >>> circuitdb((0, 0, 0, 0, 0, 0, 0, 0), [logical.id_, logical.not_, logical.and_, logical.or_])
        [((0, 1),), ((0, 1),), ((0, 1),), ((1, 0), 0), ((0, 0, 0, 1), 0, 3)]

        >>> from itertools import product
        >>> def eval(c, v):
        ...     m = list(v)
        ...     for e in c[len(m):]:
        ...         m.append(e[0](*[m[e[i]] for i in range(1, len(e))]))
        ...     return m[-1]
        >>> evals = lambda c, a: tuple([eval(c, v) for v in product(*[[0,1]]*a)])
        >>> aoms = [(a, o, m) for a in _d for o in _d[a] for m in _d[a][o]]
        >>> all(all(t == evals(circuitdb(t, o, m), a) for t in product(*[[0, 1]]*(2**a))) for (a, o, m) in aoms)
        True

        >>> circuitdb([0, 0, 0, 0])
        Traceback (most recent call last):
          ...
        TypeError: truth table must be a tuple
        >>> circuitdb((0, 0, 0))
        Traceback (most recent call last):
          ...
        ValueError: truth table must have a length that is a power of two
        >>> circuitdb(('abc', 'xyz'))
        Traceback (most recent call last):
          ...
        TypeError: truth table must contain boolean values or integers
        >>> circuitdb((0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
        Traceback (most recent call last):
          ...
        ValueError: no entries for functions of arity 4
        >>> circuitdb((0, 0, 0, 0, 0, 0, 0, 0), 132)
        Traceback (most recent call last):
          ...
        TypeError: collection of operators must be a set, frozenset, list, or tuple
        >>> circuitdb((0, 0, 0, 0, 0, 0, 0, 0), 132)
        Traceback (most recent call last):
          ...
        TypeError: collection of operators must be a set, frozenset, list, or tuple
        >>> circuitdb((0, 0, 0, 0, 0, 0, 0, 0), [(0, 1, 0)])
        Traceback (most recent call last):
          ...
        ValueError: collection of operators must only contain valid operators
        >>> circuitdb((0, 0, 0, 0, 0, 0, 0, 0), [(0, 1)])
        Traceback (most recent call last):
          ...
        ValueError: no entries for functions of arity 3 that have only the specified operators
        >>> id_not_and_or = [logical.id_, logical.not_, logical.and_, logical.or_]
        >>> circuitdb((0, 0, 0, 0, 0, 0, 0, 0), id_not_and_or, 123)
        Traceback (most recent call last):
          ...
        TypeError: collection of operators the number of which to minimize must be a set, frozenset, list, or tuple
        >>> circuitdb((0, 0, 0, 0, 0, 0, 0, 0), id_not_and_or, [(0, 1, 0)])
        Traceback (most recent call last):
          ...
        ValueError: collection of operators the number of which to minimize must contain only valid operators
        >>> circuitdb((0, 0, 0, 0, 0, 0, 0, 0), id_not_and_or, [(0, 1)])
        Traceback (most recent call last):
          ...
        ValueError: no entries for functions of arity 3 for specified operators and minimization criteria

        >>> list(sorted(list(circuitdb.keys()))) == [1, 2, 3]
        True
        >>> ks = list(sorted(list(circuitdb[1].keys())))
        >>> ks[0] == frozenset({logical.and_, logical.or_, logical.not_, logical.id_})
        True
        >>> circuitdb[2][ks[0]][ks[0]][(1,1,1,1)]
        [((0, 1),), ((0, 1),), ((1, 0), 0), ((0, 1, 1, 1), 0, 2)]
        """
        # Ensure the truth table is a tuple of booleans or integers  of the correct size.
        if not isinstance(truthtable, tuple):
            raise TypeError('truth table must be a tuple')

        # Ensure that data for functions of the requested arity is available.
        if len(truthtable) < 1 or 2**int(math.log2(len(truthtable))) != len(truthtable):
            raise ValueError('truth table must have a length that is a power of two')

        arity = int(math.log2(len(truthtable)))

        if arity not in _db._data:
            raise ValueError('no entries for functions of arity ' + str(arity))

        # Ensure that the function truth table is a valid truth table.
        if not all(isinstance(value, (int, bool)) for value in truthtable):
            raise TypeError('truth table must contain boolean values or integers')

        truthtable = tuple(map(int, truthtable))

        # Allow all operators by default or check that data is present for given operators.
        operators = frozenset(logical.every) if operators is None else operators

        if not isinstance(operators, (set, frozenset, list, tuple)):
            raise TypeError('collection of operators must be a set, frozenset, list, or tuple')

        if not frozenset(operators).issubset(logical.every):
            raise ValueError('collection of operators must only contain valid operators')

        if frozenset(operators) not in _db._data[arity]:
            raise ValueError(
                'no entries for functions of arity ' + str(arity) + ' ' +\
                'that have only the specified operators'
            )

        # Minimize the total number of operators of any available kind by default.
        minimize_ = list(sorted(list(_db._data[arity][frozenset(operators)].keys())))[0]
        minimize = minimize_ if minimize is None else minimize

        # Check that the operators to minimize are valid and corresponding data exists.
        if not isinstance(minimize, (set, frozenset, list, tuple)):
            raise TypeError(
                'collection of operators the number of which to minimize ' +\
                'must be a set, frozenset, list, or tuple'
            )

        if not frozenset(minimize).issubset(logical.every):
            raise ValueError(
                'collection of operators the number of which to minimize ' +\
                'must contain only valid operators'
            )

        if frozenset(minimize) not in _db._data[arity][frozenset(operators)]:
            raise ValueError(
                'no entries for functions of arity ' + str(arity) + ' ' +\
                'for specified operators and minimization criteria'
            )

        # Wrapping result in list constructor ensures that users do not inadvertently
        # modify the data set entries.
        return list(_db._data[arity][frozenset(operators)][frozenset(minimize)][truthtable])

# Exported object with function-like and dictionary-like interfaces
# hides the local class definition that is used to construct it.
circuitdb_ = circuitdb
circuitdb = circuitdb_(_db._data)

if __name__ == "__main__":
    doctest.testmod() # pragma: no cover
