from matplotlib import pyplot as plt

from .create_plot import create_plot


def plot_contour(x, y, z, levels=20, z_max_abs=None, z_max_percentage=None, y_max=None, color_bar=True, title=None,
                 x_label=None, y_label=None, z_label=None, cmap='Spectral_r', filename=None):
    fig, ax = plt.subplots(1, 1)
    if z_max_abs:
        z_min = z.min()
        z = np.clip(z, a_min=z_min, a_max=z_max_abs)
    if z_max_percentage:
        z_min = z.min()
        z_max = z.max()
        z_max_new = z_min + (z_max - z_min) * z_max_percentage
        z = np.clip(z, a_min=z_min, a_max=z_max_new)
    if y_max:
        index = np.argwhere(y > y_max)[0][0]
        y = y[:index]
        z = z[:index]
    cp = ax.contourf(x, y, z, levels, cmap=cmap)
    if color_bar:
        cbar = fig.colorbar(cp)
        if z_label:
            cbar.set_label(z_label, rotation=90, fontname='Arial', fontsize=14, labelpad=10)
    create_plot(ax, title, x_label, y_label, filename=filename)
    plt.close(fig)
