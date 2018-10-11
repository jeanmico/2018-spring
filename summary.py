import os
import sys
from matplotlib import pyplot as plt
import numpy as np
from math import floor
from math import ceil
import click
from statistics import mean,median,mode,stdev,StatisticsError


def extract(col, body):
   return [body[i][col] for i in range(len(body))]


def get_labels(col):
    labels_file = os.path.join(os.path.sep, 'Volumes', 'Padlock', 'TOLSURF', 'headers.txt')
    with open(labels_file, 'r') as f:
        for line in f:
            vals = line.strip().split(',')
            if vals[0] == col:
                return vals[1], vals[2]


def make_hist(col, data, n, outpath):

    # measures of centrality
    mn = mean(data)
    mdn = median(data)
    md = ''
    try:
        md = str(mode(data))
    except StatisticsError:
        md = 'not_unique'
    sigma = stdev(data)

    # plot
    title_lab, x_lab = get_labels(col)

    textstr = '\n'.join((
        r'$\mu=%.2f$' % (mn, ),
        r'$\mathrm{median}=%.2f$' % (mdn, ),
        r'$\sigma=%.2f$' % (sigma, )))


    fig, ax = plt.subplots()
    datafloor = floor(min(data))
    dataceil = ceil(max(data))
    bins = np.linspace(datafloor, dataceil, (dataceil - datafloor)*n + 1)
    ax.hist(data, bins, edgecolor="black", linewidth=1)
    ax.set_xlabel(x_lab)
    props = dict(boxstyle='round', facecolor='wheat', alpha=.5)
    ax.text(0.05, .95, textstr, transform=ax.transAxes, fontsize=10, verticalalignment='top', bbox=props)

    plt.title(title_lab) 
    # save plot
    plt.savefig(os.path.join(outpath, col + '.png'), dpi=300)

    # save measures of centrality:
    with open(os.path.join(outpath, col + '_stats.txt'), 'w+') as out:
        out.write('mean: ' +  str(mn))
        out.write('\n')
        out.write('median: ' + str(mdn))
        out.write('\n')
        out.write('mode: ' + str(md))
        out.write('\n')
        out.write('std_dev: ' + str(sigma))



def make_bar():
    print('yes')


@click.command()
@click.option('--col', help='name of column you want to summarize')
@click.option('--chart', type=click.Choice(['histogram', 'barchart']))
@click.option('--div', default=5, type=click.FLOAT, help="number of bins into which one unit should be divided")
def summary(col, chart, div):

    fpath = os.path.join(os.path.sep, 'Volumes', 'Padlock', 'TOLSURF', 'all')
                                                                                
    fname = 'all_subjects.txt'

    headers = []
    body = []
    i = 0
    with open(os.path.join(fpath, fname)) as f:
        for line in f:
            vals = line.strip().split('\t')
            if i == 0:
                headers = vals
            else:
                body.append(vals)
            i += 1
    with open(os.path.join(fpath, 'headers.txt'), 'w+') as out:
        out.write('\n'.join(str(item) for item in headers))

    header_to_index = dict()
    index_to_header = dict()
    for j, item in enumerate(headers):
        header_to_index[item] = j
        index_to_header[j] = item

    summary_data = extract(header_to_index[col], body)

    if chart == 'histogram':
        make_hist(col, [float(i) for i in summary_data], div, fpath)

if __name__ == "__main__":
    summary()
