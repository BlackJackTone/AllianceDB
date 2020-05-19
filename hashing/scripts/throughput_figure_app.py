import itertools as it
import os

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pylab
from matplotlib.font_manager import FontProperties
from matplotlib.ticker import LogLocator

OPT_FONT_NAME = 'Helvetica'
TICK_FONT_SIZE = 20
LABEL_FONT_SIZE = 22
LEGEND_FONT_SIZE = 24
LABEL_FP = FontProperties(style='normal', size=LABEL_FONT_SIZE)
LEGEND_FP = FontProperties(style='normal', size=LEGEND_FONT_SIZE)
TICK_FP = FontProperties(style='normal', size=TICK_FONT_SIZE)

MARKERS = (['o', 's', 'v', "^", "h", "v", ">", "x", "d", "<", "|", "", "+", "_"])
# you may want to change the color map for different figures
COLOR_MAP = ('#ABB2B9', '#2E4053', '#8D6E63', '#000000', '#CD6155', '#52BE80', '#FFFF00', '#5499C7', '#BB8FCE')
# you may want to change the patterns for different figures
PATTERNS = (["", "", "", "", "/", "\\", "||", "-", "o", "O", "////", ".", "|||", "o", "---", "+", "\\\\", "*"])
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

FIGURE_FOLDER = '/data1/xtra/results/figure'


def DrawLegend(legend_labels, filename):
    fig = pylab.figure()
    ax1 = fig.add_subplot(111)
    FIGURE_LABEL = legend_labels
    LEGEND_FP = FontProperties(style='normal', size=26)
    figlegend = pylab.figure(figsize=(16, 0.5))
    bars = [None] * (len(FIGURE_LABEL))
    data = [1]
    x_values = [1]

    width = 0.3
    for i in range(len(FIGURE_LABEL)):
        bars[i] = ax1.bar(x_values, data, width,
                          hatch=PATTERNS[i],
                          color=LINE_COLORS[i],
                          label=FIGURE_LABEL[i],
                          edgecolor='black', linewidth=3)

    # LEGEND

    figlegend.legend(bars, FIGURE_LABEL, prop=LEGEND_FP, \
                     loc=1, ncol=len(FIGURE_LABEL), mode="expand", shadow=True, \
                     frameon=True, handlelength=2, handletextpad=0.3, columnspacing=0.5,
                     borderaxespad=-0.2, fancybox=True
                     )
    figlegend.savefig(FIGURE_FOLDER + '/' + filename + '.pdf')


# draw a bar chart
def DrawFigure(x_values, y_values, legend_labels, x_label, y_label, y_min, y_max, filename, allow_legend):
    # you may change the figure size on your own.
    fig = plt.figure(figsize=(8, 3))
    figure = fig.add_subplot(111)

    FIGURE_LABEL = legend_labels

    if not os.path.exists(FIGURE_FOLDER):
        os.makedirs(FIGURE_FOLDER)

    # values in the x_xis
    index = np.arange(len(x_values))
    # the bar width.
    # you may need to tune it to get the best figure.
    width = 0.1
    # draw the bars
    bars = [None] * (len(FIGURE_LABEL))
    for i in range(len(y_values)):
        bars[i] = plt.bar(index + i * width + width / 2,
                          y_values[i], width,
                          hatch=PATTERNS[i],
                          color=LINE_COLORS[i],
                          label=FIGURE_LABEL[i],
                          edgecolor="black", lw=3
                          )

    # sometimes you may not want to draw legends.
    if allow_legend == True:
        plt.legend(bars, FIGURE_LABEL,
                   prop=LEGEND_FP,
                   ncol=4,
                   loc='upper center',
                   # mode='expand',
                   shadow=False,
                   bbox_to_anchor=(0.45, 1.6),
                   columnspacing=0.1,
                   handletextpad=0.2,
                   #                     bbox_transform=ax.transAxes,
                   #                     frameon=True,
                   #                     columnspacing=5.5,
                   handlelength=2,
                   )

    # you may need to tune the xticks position to get the best figure.
    plt.xticks(index + 2.5 * width, x_values)
    plt.yscale('log')

    plt.grid(axis='y', color='gray')
    figure.yaxis.set_major_locator(LogLocator(base=10))
    # figure.xaxis.set_major_locator(LinearLocator(5))
    figure.get_xaxis().set_tick_params(direction='in', pad=10)
    figure.get_yaxis().set_tick_params(direction='in', pad=10)

    plt.xlabel(x_label, fontproperties=LABEL_FP)
    plt.ylabel(y_label, fontproperties=LABEL_FP)

    plt.savefig(FIGURE_FOLDER + "/" + filename + ".pdf", bbox_inches='tight')



def GetThroughput(file, file2):
    f = open(file, "r")
    f2 = open(file2, "r")
    read = f.readlines()
    read2 = f2.readlines()
    x = float(read.pop(len(read) - 1).strip("\n"))  # get last timestamp
    i = float(read2.pop(0).strip("\n"))  # get number of inputs
    return i / x  # get throughput (#items/ms)


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

    for id in it.chain(range(38, 42)):
        file = '/data1/xtra/results/timestamps/NPJ_{}.txt'.format(id)
        file2 = '/data1/xtra/results/records/NPJ_{}.txt'.format(id)
        value = GetThroughput(file, file2)
        col1.append(value)
    y.append(col1)

    for id in it.chain(range(38, 42)):
        file = '/data1/xtra/results/timestamps/PRJ_{}.txt'.format(id)
        file2 = '/data1/xtra/results/records/PRJ_{}.txt'.format(id)
        value = GetThroughput(file, file2)
        col2.append(value)
    y.append(col2)

    for id in it.chain(range(38, 42)):
        file = '/data1/xtra/results/timestamps/MWAY_{}.txt'.format(id)
        file2 = '/data1/xtra/results/records/MWAY_{}.txt'.format(id)
        value = GetThroughput(file, file2)
        col3.append(value)
    y.append(col3)

    for id in it.chain(range(38, 42)):
        file = '/data1/xtra/results/timestamps/MPASS_{}.txt'.format(id)
        file2 = '/data1/xtra/results/records/MPASS_{}.txt'.format(id)
        value = GetThroughput(file, file2)
        col4.append(value)
    y.append(col4)

    for id in it.chain(range(38, 42)):
        file = '/data1/xtra/results/timestamps/SHJ_JM_NP_{}.txt'.format(id)
        file2 = '/data1/xtra/results/records/SHJ_JM_NP_{}.txt'.format(id)
        value = GetThroughput(file, file2)
        col5.append(value)
    y.append(col5)

    for id in it.chain(range(38, 42)):
        file = '/data1/xtra/results/timestamps/SHJ_JBCR_NP_{}.txt'.format(id)
        file2 = '/data1/xtra/results/records/SHJ_JBCR_NP_{}.txt'.format(id)
        value = GetThroughput(file, file2)
        col6.append(value)
    y.append(col6)

    for id in it.chain(range(38, 42)):
        file = '/data1/xtra/results/timestamps/PMJ_JM_NP_{}.txt'.format(id)
        file2 = '/data1/xtra/results/records/PMJ_JM_NP_{}.txt'.format(id)
        value = GetThroughput(file, file2)
        col7.append(value)
    y.append(col7)

    for id in it.chain(range(38, 42)):
        file = '/data1/xtra/results/timestamps/PMJ_JBCR_NP_{}.txt'.format(id)
        file2 = '/data1/xtra/results/records/PMJ_JBCR_NP_{}.txt'.format(id)
        value = GetThroughput(file, file2)
        col8.append(value)
    y.append(col8)
    return y


if __name__ == "__main__":
    x_values = ["Stock", "Rovio", "YSB", "DEBS"]

    y_values = ReadFile()

    legend_labels = ['NPJ', 'PRJ', 'MWAY', 'MPASS', 'SHJ$^{JM}$', 'SHJ$^{JB}$', 'PMJ$^{JM}$',
                     'PMJ$^{JB}$']

    DrawFigure(x_values, y_values, legend_labels,
               '', 'Tpt. (#inputs/ms)', 0,
               400, 'throughput_figure_app', False)

    DrawLegend(legend_labels, 'throughput_legend')
