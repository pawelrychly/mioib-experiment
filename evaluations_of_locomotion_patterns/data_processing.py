__author__ = 'Pawel Rychly'
import sys
from evaluations_of_locomotion_patterns import *
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
from plots import draw_path
import numpy

sys.argv.append("1_star_waterR.gen")
sys.argv.append("1_scorpion1_landR.gen")




data = []
depth = 0

with open("data/" + sys.argv[1]) as file:
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

results_err_xy = []
results_ff = []
results_vef = []
results_hw = []
results_xyz_speed = []
results_sfm = []
results_max_f = []
results_max_f_auto = []
i = 0
for genotype_data in data:
    i += 1
    print genotype_data["uid"]
    c = genotype_data["info"]["c"]
    d_xy = genotype_data["info"]["Dxy"]
    d_z = genotype_data["info"]["Dz"]
    if i < 4:
        draw_path(c)
    #results_ff.append(ff(d_xy))
    #results_xyz_speed.append(xyz_speed(c))
    #results_err_xy.append(err_xy(c))
    #results_vef.append(vef(d_z))
    results_max_f.append(max_f(c))
    #results_sfm.append(sfm(c))
    #results_hw.append(hw(d_xy, d_z))
    #results_max_f_auto.append(max_f_auto(c))

#print "ff: {0} ".format(numpy.mean(results_ff))
#print "xyz_speed: {0}".format(numpy.mean(results_xyz_speed))
#print "err_xy: {0}".format(numpy.mean(results_err_xy))
#print "vef: {0}".format(numpy.mean(results_vef))
print "max_f: {0}".format(numpy.mean(results_max_f))
#print "sfm: {0}".format(numpy.mean(results_sfm))
#print "hw: {0}".format(numpy.mean(results_hw))
#print "max_f_auto: {0}".format(numpy.mean(results_max_f_auto))

