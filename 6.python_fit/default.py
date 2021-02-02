# -*- coding: UTF-8 -*-
# Public package
import numpy
# Private package
import headpy.hfile as hfile
import headpy.hbes.hnew as hnew
import headpy.hbes.hopp as hopp


def dump(**argv):
    # 打开参数
    energy = argv['energy']
    # 读取数据
    massages = hnew.massage_read()
    trees = hnew.trees_read(energy=energy,
                            tree='fit4c',
                            read=['real', 'omeganpw'])
    selecters = hopp.selecters()
    selecters['omega_m'].set_width(0.15)
    selecters['omega_m'].set_width_show(0.15)
    # 初始化数据
    alldata = hnew.ALLDATA(trees=trees,
                           selecters=selecters,
                           massages=massages)
    alldata.get_weighter(data='omeganpw',
                         energy=energy,
                         name_weight='omegapi02_m_pi02pi03_m',
                         name_branch='wpi02_pi02pi03')
    namef = {}
    nameh = {}
    docuts = hopp.docuts()
    namef['r'], nameh['r'] = alldata.tree(data='real',
                                          branch='omega_m',
                                          docuts=docuts,
                                          name='fit_real')
    namef['m'], nameh['m'] = alldata.hist(data='omeganpw',
                                          branchs=['omega_m'],
                                          docuts=docuts,
                                          doweight=['wpi02_pi02pi03'],
                                          name='fit_pppmpz')
    return namef, nameh


def set_parameter(init, left_init, right_init, left, right):
    output = {}
    output['init'] = init
    output['left_init'] = left_init
    output['right_init'] = right_init
    output['left'] = left
    output['right'] = right
    return output
