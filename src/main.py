from plot import plot
from solve import solve
from lib.output import *


results_dir = '../results'

# Fasma hxhtikhs isxyos
f = [16., 31.5, 63., 125., 250., 500., 1000., 2000., 4000., 8000.][:2]
Lw = [85., 90., 95., 103., 110., 110., 105., 99.5, 97.5, 84.5]

print_title()
solve(f, results_dir, delete_old=False)
plot(f, results_dir)
