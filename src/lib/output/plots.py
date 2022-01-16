import numpy as np
from matplotlib import pyplot as plt


def create_plot(ax, title=None, x_label=None, y_label=None, legend=None, filename=None):
    if title:
        ax.set_title(title, fontname='Arial', fontsize=15, fontweight="bold")
    if x_label:
        ax.set_xlabel(x_label, fontname='Arial', fontsize=14)
    if y_label:
        ax.set_ylabel(y_label, fontname='Arial', fontsize=14)
    if legend:
        ax.legend(legend)

    if filename:
        plt.savefig(filename)
    else:
        plt.show()


def plot_contour(x, y, z, levels=20, color_bar=True, title=None, x_label=None,
                 y_label=None, cmap='Spectral_r', filename=None):
    fig, ax = plt.subplots(1, 1)
    cp = ax.contourf(x, y, z, levels, cmap=cmap)
    if color_bar:
        fig.colorbar(cp)
    create_plot(ax, title, x_label, y_label, filename=filename)


def plot_scatter(xy_sets, title=None, x_label=None, y_label=None, legend=None, filename=None):
    fig, ax = plt.subplots()
    ax.plot(*xy_sets)
    create_plot(ax, title, x_label, y_label, legend, filename)

