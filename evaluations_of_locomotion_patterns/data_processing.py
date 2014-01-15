__author__ = 'Pawel Rychly'
import sys
import os
from evaluations_of_locomotion_patterns import *
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
from plots import plot_path, plot_dispersion
import numpy
import generator_of_examples

sys.argv.append("1_scorpion1_landR.gen")
sys.argv.append("1_star_waterR.gen")







def read_file(file_name):
    depth = 0
    data = []
    print file_name
    with open("data/" + file_name) as file:
        temp_genotype = {}
        field_name = ""
        temp_value = ""
        is_long_value_reading = False
        for line in file:
            if line.startswith("#"): continue
            if is_long_value_reading:
                end_position = line.find("~")
                if end_position >= 0:
                    temp_value += line[:end_position]
                    is_long_value_reading = False
                    temp_genotype[field_name] = temp_value
                    temp_value = ""
                temp_value += line
            else:
                line = line.strip()
                line = line.replace(" ", "")
                if ":" in line:
                    values = line.split(":")
                    field_name = values[0]

                if temp_genotype.has_key(field_name):
                    data.append(temp_genotype)
                    temp_genotype = {}
                    continue

                start_position = line.find("~")
                if start_position >= 0:
                    temp_value = line[start_position+1:]
                    is_long_value_reading = True
                else:
                    if len(values) > 1:
                        temp_genotype[field_name] = values[1]
                    else:
                        filed_name = ""

        for genotype_data in data:
            if not genotype_data.has_key("info"):
                continue
            temp_data = genotype_data["info"].split("\n")
            info = {"c":[], "Dxy":[], "Dz": []}
            for row in temp_data:
                row = row.strip()
                values = row.split("\t")
                if len(values) == 5:
                    c = {"x": float(values[0]), "y": float(values[1]), "z": float(values[2])}
                    info["c"].append(c)
                    info["Dxy"].append(float(values[3]))
                    info["Dz"].append(float(values[4]))
            genotype_data["info"] = info
    return data

def describe_data(data):
    print data
    if not data.has_key("name"):
        print "Obiekt nie posiada nazwy"
        return
    if not data.has_key("group"):
        print "Obiekt nalezy do grupy domyslnej"
        data['group'] = "default"

    directory = "./results-and-plots/" + data['group'] + '/' + data['name']
    if not os.path.exists(directory):
        os.makedirs(directory)

    c = data["info"]["c"]

    plot_path(data, directory)
    d_xy = []
    d_z = []
    results = {}
    results['xyz_speed'] = xyz_speed(c)
    results['err_xy'] = err_xy(c)
    results['max_f'] = max_f(c)
    results['sfm'] = sfm(c)
    max_f_auto(c)
    if data['info'].has_key('Dxy') and data['info'].has_key('Dz'):
        d_xy = data["info"]["Dxy"]
        d_z = data["info"]["Dz"]
        results['ff'] = ff(d_xy)
        results['vef'] = vef(d_z)
        results['hw'] = hw(d_xy, d_z)
        plot_dispersion(data, directory)
    directory += "/" + data["name"] + "txt"
    with open(directory, 'w+') as file:
        file.write(str(results).replace(",",",\n\r"))
    print results

def describe_organism(file_name, uid):
    data = read_file(file_name)
    group = file_name.split(".")[0]
    for organism in data:
        if organism["uid"] == uid:
            organism['group'] = group
            describe_data(organism)


#describe_organism(sys.argv[1], "g1")
data = generator_of_examples.get_sinus_track(name="sin-1000-z-0_1-0_1", num_of_steps=1000, dimension="z", step_size=0.1, step_time=0.1)
describe_data(data)
#results_err_xy = []
#results_ff = []
#results_vef = []
#results_hw = []
#results_xyz_speed = []
#results_sfm = []
#results_max_f = []
#results_max_f_auto = []
#i = 0
#for genotype_data in data:
#    i += 1
#    print genotype_data["uid"]
#    c = genotype_data["info"]["c"]
#    d_xy = genotype_data["info"]["Dxy"]
#    d_z = genotype_data["info"]["Dz"]
#    #if i < 3:
        #plot_path(c, uid = genotype_data["uid"], type_of=sys.argv[1].replace(".", "-"))
        #plot_dispersion(d_xy, uid=genotype_data["uid"],type_of=sys.argv[1].replace(".", "-"))

    #results_ff.append(ff(d_xy))
    #results_xyz_speed.append(xyz_speed(c))
    #results_err_xy.append(err_xy(c))
    #results_vef.append(vef(d_z))
    #results_max_f.append(max_f(c))
    #results_sfm.append(sfm(c))
    #results_hw.append(hw(d_xy, d_z))
    #results_max_f_auto.append(max_f_auto(c))

#print "ff: {0} ".format(numpy.mean(results_ff))
#print "xyz_speed: {0}".format(numpy.mean(results_xyz_speed))
#print "err_xy: {0}".format(numpy.mean(results_err_xy))
#print "vef: {0}".format(numpy.mean(results_vef))
#print "max_f: {0}".format(numpy.mean(results_max_f))
#print "sfm: {0}".format(numpy.mean(results_sfm))
#print "hw: {0}".format(numpy.mean(results_hw))
#print "max_f_auto: {0}".format(numpy.mean(results_max_f_auto))

