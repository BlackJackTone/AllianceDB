import itertools as it
import os
from math import ceil

import matplotlib
import matplotlib.pyplot as plt
import pylab
from matplotlib.font_manager import FontProperties
from matplotlib.ticker import MaxNLocator, LinearLocator
from matplotlib import rc

OPT_FONT_NAME = 'Helvetica'
TICK_FONT_SIZE = 20
LABEL_FONT_SIZE = 24
LEGEND_FONT_SIZE = 26
LABEL_FP = FontProperties(style='normal', size=LABEL_FONT_SIZE)
LEGEND_FP = FontProperties(style='normal', size=LEGEND_FONT_SIZE)
TICK_FP = FontProperties(style='normal', size=TICK_FONT_SIZE)

MARKERS = (["", 'o', 's', 'v', "^", "", "h", "v", ">", "x", "d", "<", "|", "", "+", "_"])
# you may want to change the color map for different figures
COLOR_MAP = (
'#FFFFFF', '#B03A2E', '#2874A6', '#239B56', '#7D3C98', '#FFFFFF', '#F1C40F', '#F5CBA7', '#82E0AA', '#AEB6BF', '#AA4499')
# you may want to change the patterns for different figures
PATTERNS = (
["", "////", "\\\\", "//", "o", "", "||", "-", "//", "\\", "o", "O", "////", ".", "|||", "o", "---", "+", "\\\\", "*"])
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

# rc('text.latex', preamble=r'\usepackage[cm]{sfmath}')
# rc('font', **{'family': 'sans-serif',
#               'sans-serif': ['Helvetica'],
#               'weight': 'bold',
#               'size': 22
#               }
#    )
# rc('text', usetex=True)

FIGURE_FOLDER = '/data1/xtra/results/figure'


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


# draw a line chart
def DrawFigure(xvalues, yvalues, legend_labels, x_label, y_label, x_min, x_max, filename, allow_legend):
    # you may change the figure size on your own.
    fig = plt.figure(figsize=(10, 6))
    figure = fig.add_subplot(111)

    FIGURE_LABEL = legend_labels

    if not os.path.exists(FIGURE_FOLDER):
        os.makedirs(FIGURE_FOLDER)

    x_values = xvalues
    y_values = yvalues
    print("mark gap:", ceil(x_max / 6))
    lines = [None] * (len(FIGURE_LABEL))
    for i in range(len(y_values)):
        # if (i != 0 or i != 5):
        #     lines[i], = figure.plot(x_values[i], y_values[i], color=LINE_COLORS[i], \
        #                         linewidth=LINE_WIDTH, marker=MARKERS[i], \
        #                         markersize=MARKER_SIZE, label=FIGURE_LABEL[i],
        #                         markeredgewidth=2, markeredgecolor='k')
        # else:
        #     lines[i] = figure.plot(x_values[i], y_values[i], color='white', \
        #                            linewidth=0, marker='None', \
        #                            markersize=0, label=FIGURE_LABEL[i],
        #                            markevery=0, markeredgewidth=0, markeredgecolor='k'
        #                            )
        lines[i], = figure.plot(x_values[i], y_values[i], color=LINE_COLORS[i], \
                                linewidth=LINE_WIDTH, marker=MARKERS[i], \
                                markersize=MARKER_SIZE, label=FIGURE_LABEL[i],
                                markeredgewidth=2, markeredgecolor='k')

    # sometimes you may not want to draw legends.
    if allow_legend == True:
        plt.legend(lines,
                   FIGURE_LABEL,
                   prop=LEGEND_FP,
                   loc='upper center',
                   ncol=1,
                   #                     mode='expand',
                   bbox_to_anchor=(1.2, 1), shadow=False,
                   columnspacing=0.1,
                   frameon=True, borderaxespad=0.0, handlelength=1.5,
                   handletextpad=0.1,
                   labelspacing=0.1)
    # plt.xscale('log')
    # plt.yscale('log')
    # plt.xticks(x_values)
    # you may control the limits on your own.
    plt.xlim(x_min, x_max)
    plt.ylim(bottom=0)
    plt.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
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
def ReadFile(id, sample_point):
    # select 100 point from existing stats.
    w = 8
    x = []
    y = []
    empty_col = []
    empty_coly = []

    for key in it.chain(range(0, sample_point)):
        empty_col.append(0)
        empty_coly.append(0)

    bound = id + 1 * w
    for i in range(id, bound, 1):
        if i == 300 or i == 304:
            x.append(empty_col)
            y.append(empty_coly)
        col = []
        coly = []
        file = '/data1/xtra/mem/mem_stat_{}.txt'.format(i)
        f = open(file, "r")
        read = f.readlines()
        if i >= 300 and i<= 303: # lazy, progressive
            selector = 0
            loaded_data = int(read[0].split(": ")[1].split(" ")[0])
            for sample_idx in range(0, sample_point):
                # before 1000ms, progressive
                if sample_idx < 20:
                    col.append(sample_idx * 50)
                    coly.append(loaded_data * (float(sample_idx)/20))
                else:
                    # after 1000ms, keep origin number
                    if selector < len(read):
                        col.append(sample_idx * 50)
                        coly.append(int(read[selector].split(": ")[1].split(" ")[0]))
                        selector = sample_idx * 5
                    # else:
                    #     col.append(0)
        else: # eager, substract the offset
            selector = 0
            loaded_data = int(read[0].split(": ")[1].split(" ")[0])
            for sample_idx in range(0, sample_point):
                if selector < len(read):
                    if sample_idx < 20:
                        col.append(sample_idx * 50)
                        coly.append(int(read[selector].split(": ")[1].split(" ")[0]) - loaded_data + loaded_data * (float(sample_idx)/20))
                        selector = sample_idx * 5
                    else:
                        col.append(sample_idx * 50)
                        coly.append(int(read[selector].split(": ")[1].split(" ")[0]))
                        selector = sample_idx * 5
                # else:
                #     col.append(0)
        x.append(col)
        y.append(coly)
        f.close()
    print(y)

    # reorder the 1,2 and 3,4
    x[1], x[2], x[3], x[4] = x[3], x[4], x[1], x[2]
    y[1], y[2], y[3], y[4] = y[3], y[4], y[1], y[2]

    return x, y


if __name__ == "__main__":
    id = 300

    # 1500
    sample_point = 30

     # = [x * 50 for x in range(0, sample_point)]

    x_values, y_values = ReadFile(id, sample_point)

    legend_labels = ['Lazy:', 'NPJ', 'PRJ', 'MWAY', 'MPASS',
                     'Eager:', 'SHJ$^{JM}$', 'SHJ$^{JB}$', 'PMJ$^{JM}$', 'PMJ$^{JB}$']

    # print(y_values)
    DrawFigure(x_values, y_values, legend_labels,
               '$time(ms)$', 'memory usage (kb)', 0,
               1500, 'memory_usage', True)
