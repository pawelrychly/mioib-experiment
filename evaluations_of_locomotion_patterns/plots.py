__author__ = 'Pawel Rychly'

import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt

def draw_path(c_vec):
    mpl.rcParams['legend.fontsize'] = 10
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    #theta = np.linspace(-4 * np.pi, 4 * np.pi, 100)
    #print theta
    #z = np.linspace(-2, 2, 100)
    #r = z**2 + 1
    #x = r * np.sin(theta)
    #y = r * np.cos(theta)
    x = [ value["x"] for value in c_vec]
    y = [ value["y"] for value in c_vec]
    z = [ value["z"] for value in c_vec]

    ax.plot(x, y, z, label='path')
    plt.errorbar()
    ax.legend()
    plt.show()

def generate_distance_from_optimum_diagram_avg(files, log = ""):

    plt.figure(get_figure_counter())
    if log == "log":
        plt.yscale(log)
    data = load_data(files)
    for series_name, series in data.iteritems():

        x = [i for i in range(len(series))]#[[value['file_name']] for value in series]#[value['dimnesions'] for value in series ]
        labels = [value['dimnesions'] for value in series ]
        y = [value['optimum_distance_avg_result'] for value in series]
        std = [value['avg_result_std'] for value in series]

        plt.errorbar(x, y,
                     yerr=std,
                     marker=get_marker_style(),
                     label=series_name,
                     capsize=5,
                     linestyle= get_line_style())
        plt.xticks(x, labels)
    fontP = FontProperties()
    fontP.set_size('small')
    if log == "log":
        plt.legend(loc = 4, prop = fontP)
    else:
        plt.legend(loc = 2, prop = fontP)
    plt.xlabel('rozmiar instancji problemu')
    plt.ylabel('usredniony wynik - optimum')
    plt.savefig(destination_dir+'avarage_results_distance_from_optimum' + log +'.pdf')

