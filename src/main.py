from plot import plot
from solve import solve
from lib.output.console import *


results_dir = '../results'

# iyos dekth
h = 14

# Fasma hxhtikhs isxyos
f = [16., 31.5, 63., 125., 250., 500., 1000., 2000., 4000., 8000.][:7]
Lw = [85., 90., 95., 103., 110., 110., 105., 99.5, 97.5, 84.5]

order = 2

print_title()
solve(f, order, results_dir, delete_old=False)
plot(f, Lw, h, results_dir)
