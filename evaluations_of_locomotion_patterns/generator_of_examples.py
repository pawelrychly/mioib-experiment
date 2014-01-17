__author__ = 'Pawel Rychly'
import sys
import os
import numpy
import random

step_num = 0

def get_step(clock = 0):
    global step_num
    step_num += 1
    return step_num

def get_signal_with_noise(vec, std_type = True):
    base_val = 0
    if std_type == True:
        std_val = numpy.std(vec, ddof=1)
        base_val = std_val
    else:
        base_val = numpy.mean(vec) * 0.5
    new_vec = [value + ((random.randrange(-10,10) * base_val) / 10) for value in vec]
    return new_vec


def get_sin_dispersion(a, length):
    return [ a +  (numpy.sin(i * 2 * numpy.pi/(length/10))* 0.5 * a) for i in range(length)]



def get_track(name, time, f_x, f_y, f_z, group="default",dispersion = {"Dxy":0, "Dz":0}, noise = False):
    data = {}
    data = {"info":{}, "name":name, "group": group}
    data['info']['c'] = [{'x':f_x(clock), 'y': f_y(clock), 'z': f_z(clock)} for clock in time]
    data['info']['Dxy'] = get_sin_dispersion(dispersion["Dxy"], len(time))
    data['info']['Dz'] = get_sin_dispersion(dispersion["Dz"], len(time))
    return data

def get_track_by_series(name, time, x_vec, y_vec, z_vec, group="default", noise = False):
    data = {}
    data = {"info":{}, "name":name, "group": group}
    data['info']['c'] = [{'x':x_vec[i], 'y': y_vec[i], 'z': z_vec[i]} for i, clock in enumerate(time)]
    return data

def get_arc_xy(length, r):
    time = [i for i in range(length)]
    y = [(r * numpy.sin(t*(numpy.pi)/length)) for t in time]
    x = time
    z = [0 for t in time]
    return get_track_by_series(
       name = "arc_{0}_{1}".format(length,r),
       time = time,
       x_vec = x,
       y_vec = y,
       z_vec = z,
       group = "std_error"
    )

def get_line_xy_with_const_v(length):
    time = [i for i in range(length)]
    x = [0]
    for t in time:
        x.append(x[-1] + 0.5)
    y = [5 for i in time]
    z = [0 for i in time]
    return get_track_by_series(
       name = "line_v_const",
       time = time,
       x_vec = x,
       y_vec = y,
       z_vec = z,
       group = "predkosc"
    )


def get_line_xy_with_sin_v(length, f):
    time = [i for i in range(length)]
    x = [0]
    for t in time:
        x.append(x[-1] + 0.5 * (numpy.sin(t*2*numpy.pi/(length/f)) + 1))
    y = [5 for i in time]
    z = [0 for i in time]
    return get_track_by_series(
       name = "line_v_sin_{0}_{1}".format(f, length),
       time = time,
       x_vec = x,
       y_vec = y,
       z_vec = z,
       group = "predkosc"
    )

def get_line_xy_with_random_v(length):
     time = [i for i in range(length)]
     x = [0]
     for t in time:
         x.append(x[-1] + random.randrange(1,10) * 0.1)
     y = [5 for i in time]
     z = [0 for i in time]
     return get_track_by_series(
        name = "line_v_rand",
        time = time,
        x_vec = x,
        y_vec = y,
        z_vec = z,
        group = "predkosc"
     )


def get_sinus_xy_1T():
    global step_num
    step_num = 0
    return get_track(
        name = "sinus_x_50_steps_1T",
        time = [i for i in range(50)],
        f_x = lambda t: t,
        f_y = lambda t: numpy.sin(t*(2*numpy.pi)/50),
        f_z = lambda t: 0,
        group="sin_x"
    )

def get_sinus_xy_10T():
    global step_num
    step_num = 0
    return get_track(
        name = "sinus_x_50_steps_10T",
        time = [i for i in range(50)],
        f_x = lambda t: t,
        f_y = lambda t: numpy.sin(t*(2*numpy.pi)/5),
        f_z = lambda t: 0,
        group = "sin_x"
    )

def get_rectangular_xy_10T():
    global step_num
    step_num = 0
    time = [i for i in range(50)]
    x_vec = [i for i in time]
    z_vec = [0 for i in time]
    y_vec = []
    for t in time:
        y = numpy.sin(t*(2*numpy.pi)/5)
        if y > 0.5:
            y = 0.5
        if y < 0.5:
            y = -0.5
        y_vec.append(y)

    return get_track_by_series(
        name = "rectangular_sin_x_50_steps_10T",
        time = time,
        x_vec = x_vec,
        y_vec = y_vec,
        z_vec = z_vec,
        group = "rectangular_sin_x"
    )

def get_random_xy(step_size, num_of_steps, max_alfa=6):
    data = {}
    data = {"info":{}, "name":"random_{0}_{1}".format(step_size, max_alfa), "group": "random"}
    data['info']['c'] = []
    x1 = random.randrange(0, 20, 1)
    y1 = random.randrange(0, 20, 1)
    data['info']['c'].append({"x": x1, "y": y1, "z":0})
    for i in range(num_of_steps):
        alfa = random.randrange(0, max_alfa)
        y2 = step_size * numpy.sin(alfa) + y1
        if (numpy.tan(alfa) != 0):
            x2 = (y2 - y1 + (x1 * numpy.tan(alfa)))/numpy.tan(alfa)
        else:
            x2 = x1
        data['info']['c'].append({"x": x2, "y": y2, "z":0})
        x1 = x2
        y1 = y2
    return data


def get_line_xy_x():
    global step_num
    step_num = 0
    return get_track(
        name = "line_xy_x",
        time = [i for i in range(50)],
        f_x = lambda t: 5,
        f_y = lambda t: t,
        f_z = lambda t: 0,
        group = "default"
    )

def get_line_xy_y():
    global step_num
    step_num = 0
    return get_track(
        name = "line_xy_y",
        time = [i for i in range(50)],
        f_x = lambda t: t,
        f_y = lambda t: 5,
        f_z = lambda t: 0,
        group = "default"
    )

def get_line_xy_xy():
    global step_num
    step_num = 0
    return get_track(
        name = "line_xy_xy",
        time = [i for i in range(50)],
        f_x = lambda t: t,
        f_y = lambda t: t,
        f_z = lambda t: 0,
        group = "default"
    )

def get_line_with_noise_y():
    global step_num
    step_num = 0
    time = [i for i in range(50)]
    y_vec = [5 for i in time]
    z_vec = [0 for i in time]
    return  get_track_by_series(
        name = "line_xy_y_with_noise",
        time = time,
        x_vec = time,
        y_vec = get_signal_with_noise(y_vec, False),
        z_vec = z_vec,
        group = "noise"
    )


def get_sinus_xy_1T_with_noise():
    global step_num
    step_num = 0
    time = [i for i in range(50)]
    y_vec = get_signal_with_noise([numpy.sin(t*(2*numpy.pi)/50) for t in time], std_type=True)
    z_vec = [0 for i in range(50)]

    return get_track_by_series(
        name = "sinus_x_50_steps_1T",
        time = time,
        x_vec = time,
        y_vec = y_vec,
        z_vec = z_vec,
        group="sin_x_with_noise"
    )

def get_sinus_xy_10T_with_noise():
    global step_num
    step_num = 0
    time = [i for i in range(50)]
    y_vec = get_signal_with_noise([numpy.sin(t*(2*numpy.pi)/5) for t in time], std_type=True)
    z_vec = [0 for i in range(50)]

    return get_track_by_series(
        name = "sinus_x_50_steps_10T",
        time = time,
        x_vec = time,
        y_vec = y_vec,
        z_vec = z_vec,
        group="sin_x_with_noise"
    )