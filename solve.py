# coding: utf-8

"""
Throughout this program we have:
  d is a digit,  e.g. '9'
  
  r is a row,    e.g. 'A'
  c is a column, e.g. '3'
  s is a square, e.g. 'A3'
  u is a unit,   e.g. ['A1','B1','C1','D1','E1','F1','G1','H1','I1']
  
  grid is a grid, e.g. 81 non-blank chars, e.g. starting with '.18...7...
  values is a dict of possible values, e.g. {'A1':'12349', 'A2':'8', ...}
"""
import random
import time
from util import some, shuffled, ensure_list, get_all


def cross(A, B):
    """Cross product of elements in A and elements in B."""
    return [a + b for a in A for b in B]


digits = '123456789'
# 行
rows = 'ABCDEFGHI'
# 列
cols = digits
# 宫格
squares = cross(rows, cols)
# 域
unit_list = ([cross(rows, c) for c in cols] +
             [cross(r, cols) for r in rows] +
             [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')])
# 宫格：行列宫三域列表
units = dict((s, [u for u in unit_list if s in u]) for s in squares)
# 宫格：相关宫格集合
peers = dict((s, set(sum(units[s], [])) - {s}) for s in squares)


def parse_grid(grid):
    """Convert grid to a dict of possible values, {square: digits}, or
    return False if a contradiction is detected."""
    values = dict((s, digits) for s in squares)
    for s, d in grid_values(grid).items():
        if d in digits and not assign(values, s, d):
            # Fail if we can't assign d to square s.
            return False
    return values


def grid_values(grid):
    """Convert grid into a dict of {square: char} with '0' or '.' for empties."""
    chars = [c for c in grid if c in digits or c in '0.']
    assert len(chars) == 81
    return dict(zip(squares, chars))


def assign(values, s, d):
    """Eliminate all the other values (except d) from values[s] and propagate.
    Return values, except return False if a contradiction is detected."""
    other_values = values[s].replace(d, '')
    if all(eliminate(values, s, d2) for d2 in other_values):
        return values
    else:
        return False


def eliminate(values, s, d):
    """Eliminate d from values[s]; propagate when values or places <= 2.
    Return values, except return False if a contradiction is detected.
    d is the possible digit. """
    if d not in values[s]:
        return values  # Already eliminated

    # remove possible digit d
    values[s] = values[s].replace(d, '')

    if len(values[s]) == 0:
        # Contradiction: removed last value
        return False
    elif len(values[s]) == 1:
        # (1) If a square s is reduced to one value d2, then eliminate d2 from the peers.
        if not all(eliminate(values, s2, values[s]) for s2 in peers[s]):
            return False

    for unit in units[s]:
        possible_places = [s for s in unit if d in values[s]]
        if len(possible_places) == 0:
            return False  # Contradiction: no place for this value
        elif len(possible_places) == 1:
            # (2) If a unit is reduced to only one place for a value d, then put it there.
            # d can only be in one place in unit; assign it there
            if not assign(values, possible_places[0], d):
                return False
    return values


def display(values):
    """Display these values as a 2-D grid."""
    width = 1 + max(len(values[s]) for s in squares)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print ''.join(values[r + c].center(width) + ('|' if c in '36' else '') for c in cols)
        if r in 'CF':
            print line
    print


def to_text(values):
    """Translate these values to a 2-D grid string."""
    rv = []
    width = 1 + max(len(values[s]) for s in squares)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        rv.append(''.join(values[r + c].center(width) + ('|' if c in '36' else '') for c in cols))
        if r in 'CF':
            rv.append(line)
    rv.append('\n')
    return '\n'.join(rv)


def search(values, multi=False):
    """Using depth-first search and propagation, try all possible values."""
    if values is False:
        # Failed earlier
        return False
    if all(len(values[s]) == 1 for s in squares):
        # Solved!
        return values
    # Chose the unfilled square s with the fewest possibilities
    n, s = min((len(values[s]), s) for s in squares if len(values[s]) > 1)
    if multi:
        return get_all(search(assign(values.copy(), s, d)) for d in values[s])
    else:
        return some(search(assign(values.copy(), s, d)) for d in values[s])


def solve(grid, multi=False):
    return search(parse_grid(grid), multi=multi)


def solve_all(grids, name='', show_min_time=0.0, multi=False, show_multi=False, return_unique=True):
    """Attempt to solve a sequence of grids. Report results.
    When showif is a number of seconds, display puzzles that take longer.
    When showif is None, don't display any puzzles."""

    def time_solve(grid):
        start = time.clock()
        _values = solve(grid, multi=multi)
        all_values = ensure_list(_values)
        t = time.clock() - start
        # Display puzzles that take long enough
        if (show_min_time is not None and t > show_min_time) or (show_multi and len(all_values) > 1):
            display(grid_values(grid))
            for values in all_values:
                if values:
                    display(values)
            print '(%.2f seconds)\n' % t
        return grid, t, filter(solved, all_values)

    grid, times, results = zip(*[time_solve(grid) for grid in grids])
    solved_count = [len(x) for x in results]
    all_results = dict(zip(grid, results))

    N = len(grids)
    if N > 1:
        print "Solved %d of %d %s puzzles (avg %.4f secs (%.2f Hz), max %.4f secs)." % (
            sum(solved_count), N, name, sum(times) / N, N / sum(times), max(times))

    if return_unique:
        rv = {}
        for _g, _r in all_results.items():
            if len(_r) == 1:
                rv[_g] = _r
        return rv
    return all_results


def solved(values):
    """A puzzle is solved if each unit is a permutation of the digits 1 to 9."""

    def unit_solved(unit):
        return set(values[s] for s in unit) == set(digits)

    return values is not False and all(unit_solved(unit) for unit in unit_list)


def random_puzzle(N=17):
    """Make a random puzzle with N or more assignments. Restart on contradictions.
    Note the resulting puzzle is not guaranteed to be solvable, but empirically about 99.8% of them are solvable.
    Some have multiple solutions."""
    values = dict((s, digits) for s in squares)
    for s in shuffled(squares):
        if not assign(values, s, random.choice(values[s])):
            break
        ds = [values[s] for s in squares if len(values[s]) == 1]
        if len(ds) >= N and len(set(ds)) >= 8:
            return ''.join(values[s] if len(values[s]) == 1 else '.' for s in squares)
    # Give up and make a new puzzle
    return random_puzzle(N)
