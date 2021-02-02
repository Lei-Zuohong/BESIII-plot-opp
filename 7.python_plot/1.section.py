# -*- coding: UTF-8 -*-
# Public package
import pickle
# Private package
import headpy.hfile as hfile
import headpy.hbes.hopp as hopp
import headpy.hbes.hnew as hnew
import headpy.hbes.hconst as hconst

# 读取文件
massages = hnew.massage_read()
filename = {}
filename['efficiency_noweight'] = '%s.pkl' % (massages['efficiency_adjust_noweight'])
filename['efficiency'] = '%s.pkl' % (massages['efficiency_adjust'])
filename['factor'] = '%s.pkl' % (massages['factor'])
filename['event'] = '%s.pkl' % (massages['nevent'])
data = {}
for i in filename:
    data[i] = hfile.pkl_read(filename[i])
# 计算文件
energy_list = hopp.energy_list()
energy_sort = hopp.energy_sort()
nsignal = {}
for i in energy_sort:
    nsignal[i] = {}
    nsignal[i]['Energy'] = i
    nsignal[i]['Nsignal'] = data['event'][i]['nevent']
    nsignal[i]['eNsignal'] = data['event'][i]['enevent']
    nsignal[i]['Efficiency_noweight'] = data['efficiency_noweight'][i]
    nsignal[i]['Efficiency'] = data['efficiency'][i]
    nsignal[i]['Lumin'] = energy_list[i][2]
    nsignal[i]['isr'] = data['factor'][i]['isr']
    nsignal[i]['vpf'] = data['factor'][i]['vpf']

    a = nsignal[i]['Nsignal']
    ea = nsignal[i]['eNsignal']
    b = nsignal[i]['Efficiency']
    c = nsignal[i]['Lumin']
    isr = nsignal[i]['isr']
    v = nsignal[i]['vpf']
    br1 = hconst.pdg()['br_omega']
    br2 = hconst.pdg()['br_pi0']
    da = ea / b / c

    nsignal[i]['Section'] = a / b / c / isr / v / br1 / br2 / br2 / br2
    nsignal[i]['eSection'] = ea / b / c / isr / v / br1 / br2 / br2 / br2
for i in energy_sort:
    print('|{:^20}|{:^20}|{:^20}|'.format('%1.4f' % (i),
                                          '%.4f' % (nsignal[i]['Section']),
                                          '%.4f' % (nsignal[i]['eSection'])))
fileoutput = '%s.pkl' % (massages['section'])
hfile.pkl_dump(fileoutput, nsignal)
