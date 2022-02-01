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
        plt.savefig(filename, dpi=200)
    else:
        plt.show()
