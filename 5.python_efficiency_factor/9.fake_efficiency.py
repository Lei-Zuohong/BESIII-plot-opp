# -*- coding: UTF-8 -*-
# Public package
import pickle
# Private package
import headpy.hfile as hfile
import headpy.hbes.hopp as hopp
import headpy.hbes.hnew as hnew


# 读取信息
massages = hnew.massage_read()
energy_sort = hopp.energy_sort()
efficiency = '%s.pkl' % (massages['efficiency'])
efficiency_noweight = '%s.pkl' % (massages['efficiency_noweight'])
efficiency_adjust = '%s.pkl' % (massages['efficiency_adjust'])
efficiency_adjust_noweight = '%s.pkl' % (massages['efficiency_adjust_noweight'])
# 读取
data_efficiency = hfile.pkl_read(efficiency)
data_efficiency_noweight = hfile.pkl_read(efficiency_noweight)
data_efficiency_adjust = {}
data_efficiency_adjust_noweight = {}
# 输出
fake = hfile.pkl_read('%s.pkl' % (massages['fake']))
for energy in energy_sort:
    data_efficiency_adjust[energy] = data_efficiency[energy] * fake[energy]
    data_efficiency_adjust_noweight[energy] = data_efficiency_noweight[energy] * fake[energy]
    print('Energy: %1.4f' % (energy))
    print(data_efficiency[energy])
    print(data_efficiency_noweight[energy])
    print(data_efficiency_adjust[energy])
    print(data_efficiency_adjust_noweight[energy])
data_efficiency_adjust[2.0500] *= 1.118525
data_efficiency_adjust_noweight[2.0500] *= 1.118525
hfile.pkl_dump(efficiency_adjust, data_efficiency_adjust)
hfile.pkl_dump(efficiency_adjust_noweight, data_efficiency_adjust_noweight)
