def atm_to_pa(p):
    return 101325. * p


def pa_to_atm(p):
    return p / 101325.


def C_to_K(Temp):
    return 273.15 + Temp
