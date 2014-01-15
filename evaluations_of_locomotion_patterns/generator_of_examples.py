__author__ = 'Pawel Rychly'
import sys
import os
import numpy

def get_sinus_track(name, num_of_steps, dimension, step_size, step_time):
    time = [0]
    data = {}

    for i in range(num_of_steps-1):
        time_of_step = time[-1] + step_time
        time.append(time_of_step)

    data = {"info":{}, "name":name}
    data['info']['c'] = [{'x':i*step_size, 'y': 10, 'z': 0} for i in range(num_of_steps)]
    for i, time in enumerate(time):
        data['info']['c'][i][dimension] = numpy.sin(time)
    return data