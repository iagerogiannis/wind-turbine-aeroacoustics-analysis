# Aeroacoustics Analysis of Wind Turbine

The code was developed to calculate the spectrum of sound pressure level of noise produced by a wind turbine.

The wind turbine is considered as a unipolar source of sound concentrated at the center of the rotor which emits spherical waves.

For the solution we use the axis-symmetrical Helmholtz equation and the Crank-Nicolson scheme.

## Overview

The field of SPL is being calculated for every frequency of the 1/3 octave band.

![alt text](readme/contour.png?raw=true)

Then the A-weighted spectrum and the equivalent SPL get calculated.

![alt text](readme/SPL.png?raw=true)
