__author__ = 'Pawel Rychly'

import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib.font_manager import FontProperties
import evaluations_of_locomotion_patterns
import numpy



def prepare_directory(data, directory):
    if not data.has_key('group'):
        data['group'] = "default"
    if not os.path.exists(directory):
        os.makedirs(directory)


def plot_v(data, directory):
    length = len(data['info']['c'])
    distances = [ evaluations_of_locomotion_patterns.euclidean_distance(data['info']['c'][i-1], data['info']['c'][i]) for i in range(1,length)]
    plt.figure()
    x = [i for i in range(len(distances))]

       #std = [value['avg_result_std'] for value in ]
    plt.errorbar(x, distances,
                 #yerr=std,
                 marker='.',
                 label="speed",
                 capsize=1,
                 linestyle= ':'
                 )

    plt.xticks(numpy.arange(x[0], x[-1], 10))
    #plt.xticks(x)
    fontP = FontProperties()
    fontP.set_size('small')
    leg = plt.legend(loc = 4, prop = fontP)
    plt.xlabel('time')
    plt.ylabel('speed')
    plt.legend(loc = 2, prop = fontP)
    plt.savefig(directory + '/speed-' + data['name'] + '.png')

def plot_path(data, directory, ranges={ "x":[],"y": [],"z": []}, is_large_data = False):
    prepare_directory(data, directory)
    mpl.rcParams['legend.fontsize'] = 10
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    x = [ value["x"] for value in data['info']['c']]
    y = [ value["y"] for value in data['info']['c']]
    z = [ value["z"] for value in data['info']['c']]
    if not is_large_data:
        ax.plot(x, y, z, '.', label="track")
        ax.plot(x, y, z, ':', markerfacecolor='blue')
    else:
        ax.plot(x, y, z, ':', markerfacecolor='blue', label="track")

    if len(ranges["x"]) == 2:
        ax.set_xlim(ranges["x"])
    if len(ranges["y"]) == 2:
        ax.set_ylim(ranges["y"])
    #plt.errorbar()
    ax.legend()
    plt.savefig(directory + "/track-" + data['name'] + ".png")
    #plt.show()

def plot_dispersion(data, directory):
    prepare_directory(data, directory)
    dxy = data['info']['Dxy']
    dz = data['info']['Dz']
    plt.figure()
    x = [i for i in range(len(dxy))]
    y1 = dxy
    y2 = dz
    #std = [value['avg_result_std'] for value in ]
    plt.errorbar(x, y1,
                 #yerr=std,
                 #marker=get_marker_style(),
                 label="dispersion XY",
                 capsize=1
                 #linestyle= get_line_style()
                 )
    plt.xticks(x)
    plt.errorbar(x, y2,
                 #yerr=std,
                 #marker=get_marker_style(),
                 label="dispersion Z",
                 capsize=1
                 #linestyle= get_line_style()
                 )
    plt.xticks(x)
    fontP = FontProperties()
    fontP.set_size('small')
    leg = plt.legend(loc = 4, prop = fontP)
    #fontP = FontProperties()
    #fontP.set_size('small')
    plt.xlabel('czas')
    plt.ylabel('dispersion xy')

    plt.legend(loc = 2, prop = fontP)
    plt.savefig(directory + '/dispersion-' + data['name'] + '.png')
    plt.yscale("log")
    plt.ylabel('dispersion xy - log')
    plt.savefig(directory + '/dispersion-log-' + data['name'] + '.png')

