from matplotlib import pyplot as plt

from .create_plot import create_plot


def plot_scatter(xy_sets, title=None, x_label=None, y_label=None, legend=None, filename=None):
    fig, ax = plt.subplots()
    ax.plot(*xy_sets)
    create_plot(ax, title, x_label, y_label, legend, filename)
    plt.close(fig)
