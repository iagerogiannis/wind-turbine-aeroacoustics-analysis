import math

from src.units import *


h = 14                  # Height of receiver

z_s = 50.               # Height of hub
r_max = 350.            # Horizontal distance from W/T

Temp = C_to_K(20.)      # Temperature
hr = .7                 # Relative humidity
ps = atm_to_pa(1.)      # Atmospheric Pressure
sigma_ = 3.e5           # Flow resistance of ground
z0 = .01                # Asperity
u_star = .4             # Friction velocity

f = [16., 31.5, 63., 125., 250., 500., 1000., 2000., 4000., 8000.]      # Frequency
Lw = [85., 90., 95., 103., 110., 110., 105., 99.5, 97.5, 84.5]          # Sound Power Level of Source

theta = [0., math.pi]
