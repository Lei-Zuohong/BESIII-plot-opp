# -*- coding: UTF-8 -*-
# Public package
import numpy as numpy
import math
# Private package
import headpy.hfile as hfile
import headpy.hbes.hnew as hnew
import headpy.hbes.hopp as hopp


def data_babar_opp(left=0, right=5):
    data = hfile.pkl_read('fdata/section-babar-opp.pkl')
    selecter = numpy.where((data[0] > left) & (data[0] < right))
    output = {}
    output['x'] = data[0][selecter]
    output['y'] = data[1][selecter]
    output['e'] = data[2][selecter]
    return output


def data_babar_opm(left=0, right=5):
    data = hfile.pkl_read('fdata/section-babar-opm.pkl')
    selecter = numpy.where((data[0] > left) & (data[0] < right))
    output = {}
    output['x'] = data[0][selecter]
    output['y'] = data[1][selecter]
    output['e'] = data[2][selecter]
    return output


def data_bes_opm():
    data = hfile.pkl_read('fdata/section-bes-opm.pkl')
    output = {}
    output['x'] = data[0]
    output['y'] = data[1]
    output['e'] = data[2]
    return output


def data_bes_opp_sta():
    massages = hnew.massage_read()
    data = hfile.pkl_read('%s.pkl' % (massages['section']))
    x = []
    y = []
    e = []
    energy_list = data.keys()
    energy_list.sort()
    for energy in energy_list:
        if(energy in data):
            x.append(data[energy]['Energy'])
            y.append(data[energy]['Section'])
            e.append(data[energy]['eSection'])
    output = {}
    output['x'] = numpy.array(x)
    output['y'] = numpy.array(y)
    output['e'] = numpy.array(e)
    return output


def data_bes_opp_sys():
    output = data_bes_opp_sta()

    error = hfile.pkl_read('8.python_error/data/error_total.pkl')
    error_sys = []
    for count, energy in enumerate(hopp.energy_sort()):
        error_sys.append(error[energy])
    error_sys = numpy.array(error_sys)
    error_sys = output['y'] * error_sys / 100

    for i in range(19):
        output['e'][i] = pow(output['e'][i]**2 + error_sys[i]**2, 0.5)
    return output
