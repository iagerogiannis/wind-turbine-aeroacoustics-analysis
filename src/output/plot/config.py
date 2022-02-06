from src.config import config_version


configurations = [{
    "contour_levels": 200,
    "color_map": 'Spectral_r',
    "z_max_percentage": .7,
    "z_max_abs": None,
    "title": 'SPL contour for frequency {}Hz and theta {}deg'
}]

configuration = configurations[config_version - 1]
