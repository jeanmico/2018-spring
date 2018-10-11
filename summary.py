import os
import sys
from matplotlib import pyplot as plt
import numpy as np
from math import floor
from math import ceil
import click



def extract(col, body):
   return [body[i][col] for i in range(len(body))]


def make_hist(data, n):
    fig, ax = plt.subplots()
    datafloor = floor(min(data))
    dataceil = ceil(max(data))
    bins = np.linspace(datafloor, dataceil, (dataceil - datafloor)*n + 1)
    ax.hist(data, bins, edgecolor="black", linewidth=1.2)
    plt.show()



def make_bar():
    print('yes')


@click.command()
@click.option('--col', help='name of column you want to summarize')
@click.option('--chart_type', type=click.Choice(['histogram', 'barchart']))
@click.option('--bin_div', default=5, type=click.INT, help="number of bins into which one unit should be divided")
def summary(col, chart_type, bin_div):

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

    header_to_index = dict()
    index_to_header = dict()
    for j, item in enumerate(headers):
        header_to_index[item] = j
        index_to_header[j] = item

    summary_data = extract(header_to_index[col], body)

    if chart_type == 'histogram':
        make_hist([float(i) for i in summary_data], bin_div)

if __name__ == "__main__":
    summary()
