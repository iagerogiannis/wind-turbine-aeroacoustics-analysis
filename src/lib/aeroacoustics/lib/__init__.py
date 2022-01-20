import math
import numpy as np
from src.lib.units import *

g = 1.4
R = 287.
K_von_Karman = 0.35

T0 = 293.15
T_01 = 273.16
p_s0 = atm_to_pa(1.)


"""
Ypologismos At: xrhsimopoietai ston oro poy ypeiserxetai mesa
ston kymatiko arithmo twn komvwn toy aporrofitikoy stromatos
"""
A_t_ = [.2, .2, .4, .5, 1., 10.]
f_ = [0., 30., 125., 500., 1000., 10000.]


def A_t(f):
    global f_, A_t_
    return np.interp(f, f_, A_t_)


def nominal_speed_of_sound(T):
    return math.sqrt(g * R * T)


def wave_length(f, c):
    return c / f


def reduced_sound_impedance(f, sigma_):
    return 1. + 9.08 * (1000. * f / sigma_) ** (-0.75) + (11.9 * (1000. * f / sigma_) ** (-0.73)) * 1j


def alpha(k0):
    return 1j / (2. * k0)


def betta(k, k0):
    return alpha(k0) * (k ** 2 - k0 ** 2)


def kappa(c, f, z=None, z_t=None, z_M=None, atmospheric_absorption_term=None, check_absorbing_layer=True):
    def absorbing_layer_term():
        nonlocal f, z, z_t, z_M
        return 1j * A_t(f) * ((z - z_t) / (z_M - z_t)) ** 2

    omega = 2. * math.pi * f
    k = omega / c

    if check_absorbing_layer and z_t < z < z_M:
        k += absorbing_layer_term()

    if atmospheric_absorption_term:
        k += 1j * atmospheric_absorption_term / (20. * math.log10(math.e))

    return k


def wind_velocity(z, u, z0):
    if z < 1.e-16:
        return 0.
    else:
        return u * math.log(z / z0) / K_von_Karman


def c_effective(u_w, theta, c0):
    return c0 + u_w * math.cos(theta)


def sigma(k0, Dz, Z, order=1):
    if order == 1:
        sigma_1 = 1. / (1. - (k0 * Dz / Z) * 1j)
        sigma_2 = 0.
    elif order == 2:
        sigma_1 = 4. / (3. - (2. * k0 * Dz / Z) * 1j)
        sigma_2 = -1. / (3. - (2. * k0 * Dz / Z) * 1j)
    else:
        return
    return [sigma_1, sigma_2]


def tau(k0, Dz, order=1):
    if order == 1:
        tau_1 = 1. / (1. + k0 * Dz * 1j)
        tau_2 = 0.
    elif order == 2:
        tau_1 = 4. / (3. + 2. * k0 * Dz * 1j)
        tau_2 = -1. / (3. + 2. * k0 * Dz * 1j)
    else:
        return
    return [tau_1, tau_2]


def atmospheric_attenuation_coefficient(f, T, p_s, hr):
    global p_s0, T0

    def saturation_pressure():
        global p_s0, T_01
        nonlocal T
        return p_s0 * 10. ** (-6.8346 * (T_01 / T) ** 1.261 + 4.6151)

    def relative_to_absolute_humidity():
        global p_s0
        nonlocal hr, T, p_rel
        p_sat = saturation_pressure()
        return hr * (p_sat / p_s0) / p_rel

    def Fr_O():
        nonlocal h, p_rel
        return p_rel * (24. + 4.04e4 * h * (.02 + h) / (.391 + h))

    def Fr_N():
        nonlocal h, p_rel, T_rel
        return p_rel / math.sqrt(T_rel) * (9. + 280. * h * math.exp(-4.17 * (T_rel ** (-1 / 3) - 1.)))

    p_rel = p_s / p_s0
    T_rel = T / T0

    h = 100. * relative_to_absolute_humidity()
    Fr_O_ = Fr_O()
    Fr_N_ = Fr_N()

    x_c = 1.84e-11 / p_rel * math.sqrt(T / T0)
    x_o = 0.01275 * math.exp(-2239.1 / T) / (Fr_O_ + f ** 2 / Fr_O_)
    x_n = 0.1068 * math.exp(-3352. / T) / (Fr_N_ + f ** 2 / Fr_N_)

    a = 20. * math.log10(math.e) * f ** 2 * (x_c + T_rel ** (-2.5) * (x_o + x_n))

    return a


def sound_pressure_level(DL, Lw, R_):
    return Lw - 10. * math.log10(4 * math.pi * R_ ** 2) + DL
