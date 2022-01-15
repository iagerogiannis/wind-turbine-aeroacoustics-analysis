from plot import plot
from solve import solve


f = [16., 31.5, 63., 125., 250., 500., 1000., 2000., 4000., 8000.]
f_for_solve = f[:3]

solve(f_for_solve)
plot(f_for_solve)
