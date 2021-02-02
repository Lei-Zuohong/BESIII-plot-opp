# -*- coding: UTF-8 -*-
# Public package
import os
import sys
import numpy
# Private package
import ROOT
import headpy.hfile as hfile
import headpy.hbes.hopp as hopp
import headpy.hbes.hnew as hnew


def weight(energy):
    # region 初始化数据
    massages = hnew.massage_read()
    trees = hnew.trees_read(energy=energy,
                            tree='fit4c',
                            read=['real', 'omeganpw'])
    selecters = hopp.selecters()
    docuts = hopp.docuts()
    # endregion
    # region 筛选数据
    tree_real = trees['real']
    tree_omeganpw = trees['omeganpw']
    selecters['omega_m'].set_width(0.05)
    tree_r = hnew.tree_cut(tree_real,
                           selecters,
                           branchs=docuts)
    tree_m = hnew.tree_cut(tree_omeganpw,
                           selecters,
                           branchs=docuts)
    selecters['omega_m'].shift(-0.15)
    tree_b1 = hnew.tree_cut(tree_real,
                            selecters,
                            branchs=docuts)
    selecters['omega_m'].shift(0.15 + 0.15)
    tree_b2 = hnew.tree_cut(tree_real,
                            selecters,
                            branchs=docuts)
    # endregion
    weighter = hnew.WEIGHTER()
    weighter.set_branch(['omegapi02_m', 'pi02pi03_m'])
    weighter.set_data_m(data=[tree_m['omegapi02_m'], tree_m['pi02pi03_m']])
    weighter.set_data_r(data=[tree_r['omegapi02_m'], tree_r['pi02pi03_m']])
    weighter.set_data_b(data1=[tree_b1['omegapi02_m'], tree_b1['pi02pi03_m']],
                        data2=[tree_b2['omegapi02_m'], tree_b2['pi02pi03_m']])
    weighter.set_bins()
    weighter.set_matrix()
    weighter.set_weight()
    return weighter


name_weight = 'omegapi02_m_pi02pi03_m'
massage = hnew.massage_read()
weight_folder = 'fdata/weight-%s' % (massage['version'])
os.system('mkdir %s/%s' % (weight_folder, name_weight))
energy_sort = hopp.energy_sort()
for energy in energy_sort:
    # if(energy != 2.1250): continue
    output = weight(energy)
    hfile.pkl_dump('%s/%s/%1.4f.pkl' % (weight_folder, name_weight, energy), output)
