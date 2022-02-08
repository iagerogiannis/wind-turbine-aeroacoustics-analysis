from src.algorithms import flatten_2d_list, bubble_sort_dicts
from src.output.plot.lib import plot_scatter


def plot_SPL_of_r(totals_dir, data, f_to_plot):

    thetas = list(set([item['theta'] for item in data if 'theta' in item]))
    bubble_sort_dicts(data, 'frequency')

    for theta in thetas:
        total_results_dir = '{}/theta{}'.format(totals_dir, str(int(theta)))

        if not f_to_plot:
            f_to_plot = [item['frequency'] for item in data if item['theta'] == theta]

        SPL_of_r = flatten_2d_list([[item['r'], item['SPL_of_r']]
                                    for item in data if item['theta'] == theta and item['frequency'] in f_to_plot])

        plot_scatter(SPL_of_r,
                     x_label='r [m]', y_label='SPL [dB]',
                     legend=['f = {}Hz'.format(f_i) for f_i in f_to_plot],
                     title='Sound Pressure Level according to r for theta {}deg'.format(str(int(theta))),
                     filename='{}/SPL_of_r.png'.format(total_results_dir))
