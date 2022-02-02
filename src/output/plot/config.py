from src.config import config_version


configurations = [{
    "contour_levels": 200,
    "color_map": 'Spectral_r',
    "z_max_percentage": .7,
    "z_max_abs": None,
    "title": 'SPL contour for frequency {}Hz and theta {}deg'
}, {
    "contour_levels": 20,
    "color_map": 'coolwarm',
    "z_max_percentage": None,
    "z_max_abs": 80.,
    "title": ''
}, {
    "contour_levels": 20,
    "color_map": 'PRGn_r',
    "z_max_percentage": None,
    "z_max_abs": 85.,
    "title": ""
}]

configuration = configurations[config_version - 1]
