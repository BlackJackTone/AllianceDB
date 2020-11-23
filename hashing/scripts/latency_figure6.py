import itertools as it
import os

import matplotlib
import matplotlib.pyplot as plt
import pylab
from matplotlib import rc
from matplotlib.font_manager import FontProperties
from matplotlib.ticker import MaxNLocator, LinearLocator, ScalarFormatter

OPT_FONT_NAME = 'Helvetica'
TICK_FONT_SIZE = 20
LABEL_FONT_SIZE = 24
LEGEND_FONT_SIZE = 26
LABEL_FP = FontProperties(style='normal', size=LABEL_FONT_SIZE)
LEGEND_FP = FontProperties(style='normal', size=LEGEND_FONT_SIZE)
TICK_FP = FontProperties(style='normal', size=TICK_FONT_SIZE)

MARKERS = (["", 'o', 's', 'v', "^", "", "h", "v", ">", "x", "d", "<", "|", "", "+", "_"])
# you may want to change the color map for different figures
COLOR_MAP = ('#FFFFFF', '#B03A2E', '#2874A6', '#239B56', '#7D3C98', '#FFFFFF', '#F1C40F', '#F5CBA7', '#82E0AA', '#AEB6BF', '#AA4499')
# you may want to change the patterns for different figures
PATTERNS = (["", "////", "\\\\", "//", "o", "", "||", "-", "//", "\\", "o", "O", "////", ".", "|||", "o", "---", "+", "\\\\", "*"])
LABEL_WEIGHT = 'bold'
LINE_COLORS = COLOR_MAP
LINE_WIDTH = 3.0
MARKER_SIZE = 13.0
MARKER_FREQUENCY = 1000

matplotlib.rcParams['ps.useafm'] = True
matplotlib.rcParams['pdf.use14corefonts'] = True
matplotlib.rcParams['xtick.labelsize'] = TICK_FONT_SIZE
matplotlib.rcParams['ytick.labelsize'] = TICK_FONT_SIZE
matplotlib.rcParams['font.family'] = OPT_FONT_NAME
rc('text.latex', preamble=r'\usepackage[cm]{sfmath}')
rc('font', **{'family': 'sans-serif',
              'sans-serif': ['Helvetica'],
              'weight': 'bold',
              'size': 22
              }
   )
rc('text', usetex=True)

exp_dir = "/data1/xtra"

FIGURE_FOLDER = exp_dir + '/results/figure'


# there are some embedding problems if directly exporting the pdf figure using matplotlib.
# so we generate the eps format first and convert it to pdf.
def ConvertEpsToPdf(dir_filename):
    os.system("epstopdf --outfile " + dir_filename + ".pdf " + dir_filename + ".eps")
    os.system("rm -rf " + dir_filename + ".eps")


def DrawLegend(legend_labels, filename):
    fig = pylab.figure()
    ax1 = fig.add_subplot(111)
    FIGURE_LABEL = legend_labels
    LINE_WIDTH = 8.0
    MARKER_SIZE = 20.0
    LEGEND_FP = FontProperties(style='normal', size=26)

    figlegend = pylab.figure(figsize=(16, 0.4))
    idx = 0
    lines = [None] * (len(FIGURE_LABEL))
    data = [1]
    x_values = [1]

    idx = 0
    for group in range(len(FIGURE_LABEL)):
        lines[idx], = ax1.plot(x_values, data,
                               color=LINE_COLORS[idx], linewidth=LINE_WIDTH,
                               marker=MARKERS[idx], markersize=MARKER_SIZE, label=str(group),
                               markeredgewidth=2, markeredgecolor='k'
                               )

        idx = idx + 1

    # LEGEND
    figlegend.legend(lines, FIGURE_LABEL, prop=LEGEND_FP,
                     loc=1, ncol=len(FIGURE_LABEL), mode="expand", shadow=False,
                     frameon=False, borderaxespad=-0.2, handlelength=1.2)

    if not os.path.exists(FIGURE_FOLDER):
        os.makedirs(FIGURE_FOLDER)
    # no need to export eps in this case.
    figlegend.savefig(FIGURE_FOLDER + '/' + filename + '.pdf')

class ScalarFormatterForceFormat(ScalarFormatter):
    def _set_format(self):  # Override function that finds format to use.
        self.format = "%1.1f"  # Give format here

# draw a line chart
def DrawFigure(xvalues, yvalues, legend_labels, x_label, y_label, x_min, x_max, filename, allow_legend):
    # you may change the figure size on your own.
    fig = plt.figure(figsize=(10, 3))
    figure = fig.add_subplot(111)

    FIGURE_LABEL = legend_labels

    if not os.path.exists(FIGURE_FOLDER):
        os.makedirs(FIGURE_FOLDER)

    x_values = xvalues
    y_values = yvalues

    print(x_values)
    print(y_values)

    lines = [None] * (len(FIGURE_LABEL))
    for i in range(len(y_values)):
        lines[i], = figure.plot(x_values, y_values[i], color=LINE_COLORS[i], \
                                linewidth=LINE_WIDTH, marker=MARKERS[i], \
                                markersize=MARKER_SIZE, label=FIGURE_LABEL[i],
                                markeredgewidth=2, markeredgecolor='k')

    # sometimes you may not want to draw legends.
    if allow_legend == True:
        plt.legend(lines,
                   FIGURE_LABEL,
                   prop=LEGEND_FP,
                   loc='upper center',
                   ncol=3,
                   #                     mode='expand',
                   bbox_to_anchor=(0.55, 1.5), shadow=False,
                   columnspacing=0.1,
                   frameon=True, borderaxespad=0.0, handlelength=1.5,
                   handletextpad=0.1,
                   labelspacing=0.1)
    plt.xscale('log')
    # plt.yscale('log')
    plt.xticks(x_values)
    # you may control the limits on your own.
    # plt.xlim(x_min, x_max)
    plt.ylim(bottom=0)
    yfmt = ScalarFormatterForceFormat()
    yfmt.set_powerlimits((0,0))

    figure.get_yaxis().set_major_formatter(yfmt)
    # plt.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
    plt.grid(axis='y', color='gray')
    figure.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    figure.yaxis.set_major_locator(LinearLocator(3))
    # figure.xaxis.set_major_locator(FixedLocator(x_values, nbins=len(x_values)))
    # figure.yaxis.set_major_locator(LogLocator(base=10))
    # figure.xaxis.set_major_locator(LogLocator(base=10))
    # figure.xaxis.set_major_locator(MaxNLocator(integer=True))

    # figure.get_xaxis().set_tick_params(direction='in', pad=10)
    # figure.get_yaxis().set_tick_params(direction='in', pad=10)

    plt.xlabel(x_label, fontproperties=LABEL_FP)
    plt.ylabel(y_label, fontproperties=LABEL_FP)
    plt.savefig(FIGURE_FOLDER + "/" + filename + ".pdf", bbox_inches='tight')


# example for reading csv file
def ReadFile():
    y = []
    col1 = []
    col2 = []
    col3 = []
    col4 = []
    col5 = []
    col6 = []
    col7 = []
    col8 = []
    col9 = []

    for id in it.chain(range(0, 4)):
        col9.append(0)
    y.append(col9)
    for id in it.chain(range(25, 29)):
        print(id)
        file = exp_dir + '/results/latency/NPJ_{}.txt'.format(id)
        f = open(file, "r")
        read = f.readlines()
        x = float(read.pop(int(len(read) * 0.95)).strip("\n"))  # get the 99th timestamp
        col1.append(x)
    y.append(col1)

    for id in it.chain(range(25, 29)):
        file = exp_dir + '/results/latency/PRJ_{}.txt'.format(id)
        f = open(file, "r")
        read = f.readlines()
        x = float(read.pop(int(len(read) * 0.95)).strip("\n"))  # get the 99th timestamp
        col2.append(x)
    y.append(col2)

    for id in it.chain(range(25, 29)):
        file = exp_dir + '/results/latency/MWAY_{}.txt'.format(id)
        f = open(file, "r")
        read = f.readlines()
        x = float(read.pop(int(len(read) * 0.95)).strip("\n"))  # get the 99th timestamp
        col3.append(x)
    y.append(col3)

    for id in it.chain(range(25, 29)):
        file = exp_dir + '/results/latency/MPASS_{}.txt'.format(id)
        f = open(file, "r")
        read = f.readlines()
        x = float(read.pop(int(len(read) * 0.95)).strip("\n"))  # get the 99th timestamp
        col4.append(x)
    y.append(col4)

    y.append(col9)  # this is a fake empty line to separate eager and lazy.

    for id in it.chain(range(25, 29)):
        file = exp_dir + '/results/latency/SHJ_JM_NP_{}.txt'.format(id)
        f = open(file, "r")
        read = f.readlines()
        x = float(read.pop(int(len(read) * 0.95)).strip("\n"))  # get last timestamp
        col5.append(x)
    y.append(col5)

    for id in it.chain(range(25, 29)):
        file = exp_dir + '/results/latency/SHJ_JBCR_NP_{}.txt'.format(id)
        f = open(file, "r")
        read = f.readlines()
        x = float(read.pop(int(len(read) * 0.95)).strip("\n"))  # get last timestamp
        col6.append(x)
    y.append(col6)

    for id in it.chain(range(25, 29)):
        file = exp_dir + '/results/latency/PMJ_JM_NP_{}.txt'.format(id)
        f = open(file, "r")
        read = f.readlines()
        x = float(read.pop(int(len(read) * 0.95)).strip("\n"))  # get last timestamp
        col7.append(x)
    y.append(col7)

    for id in it.chain(range(25, 29)):
        file = exp_dir + '/results/latency/PMJ_JBCR_NP_{}.txt'.format(id)
        f = open(file, "r")
        read = f.readlines()
        x = float(read.pop(int(len(read) * 0.95)).strip("\n"))  # get last timestamp
        col8.append(x)
    y.append(col8)
    return y


if __name__ == "__main__":
    x_values = [1, 10, 100, 200]

    y_values = ReadFile()

    legend_labels = ['Lazy:', 'NPJ', 'PRJ', 'MWAY', 'MPASS',
                     'Eager:', 'SHJ$^{JM}$', 'SHJ$^{JB}$', 'PMJ$^{JM}$', 'PMJ$^{JB}$']
    # print(y_values)
    DrawFigure(x_values, y_values, legend_labels,
               r'$dupe$', 'Latency (ms)', 0,
               1.6, 'latency_figure6', False)
