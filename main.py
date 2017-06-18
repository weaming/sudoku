# coding: utf-8

from __future__ import print_function
import sys
import os
from solve import *
from util import from_file

grid1 = '003020600900305001001806400008102900700000008006708200002609500800203009005010300'
grid2 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
hard1 = '.....6....59.....82....8....45........3........6..3.54...325..6..................'

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('参数数量不正确', file=sys.stderr)
        sys.exit(4)
    t = sys.argv[1]

    if t == 'files':
        solve_all(from_file("puzzles/easy50.txt"), "easy", None)
        solve_all(from_file("puzzles/top95.txt"), "hard", None)
        solve_all(from_file("puzzles/hardest.txt"), "hardest", None, multi=True)
    elif t == 'random':
        if len(sys.argv) > 2:
            N = int(sys.argv[2])
        else:
            N = 30
        with open('output.txt', 'w') as f:
            for g, rr in solve_all([random_puzzle(N=N) for _ in range(99)], "random", 0.05,
                                   multi=True, return_unique=True).items():
                assert len(rr) == 1
                if g.count('.') == 0:
                    continue

                text = to_text(grid_values(g))
                print(text)
                f.write(text)
                for r in rr:
                    text = to_text(r)
                    print(text)
                    f.write(text)
                f.write('='*25 + '\n\n')
    else:
        if not os.path.isfile(t):
            print('File %s not exist!' % t, file=sys.stderr)
            sys.exit(5)
        solve_all(from_file(t), t, 0, multi=True)
