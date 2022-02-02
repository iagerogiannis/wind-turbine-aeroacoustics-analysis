# -- Configuration Version --
config_version = 1

# -- Solver configuration --
f_to_calculate = [16., 31.5, 63., 125., 250., 500., 1000., 2000., 4000., 8000.]
f_to_plot = [250., 1000., 4000.]

order = 2
absorbing_layer = True


# -- Results Files configuration --
should_delete_old_results = False

results_directory = '../results/config{}'.format(config_version)

results_dir_with_absorbing_layer = '{}/with_absorbing_layer'.format(results_directory)
results_dir_without_absorbing_layer = '{}/without_absorbing_layer'.format(results_directory)

if absorbing_layer:
    results_dir = results_dir_with_absorbing_layer
else:
    results_dir = results_dir_without_absorbing_layer

totals_dir = '{}/total'.format(results_dir)
