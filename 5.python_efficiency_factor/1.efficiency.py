# -*- coding: UTF-8 -*-
# Public package
import pickle
# Private package
import headpy.hfile as hfile
import headpy.hbes.hopp as hopp
import headpy.hbes.hnew as hnew
import headpy.hscreen.hprint as hprint


def effect(energy):
    # 读取信息并设定
    massages = hnew.massage_read()
    treesf = hnew.trees_read(energy, 'fit4c', ['omeganpw'])
    treest = hnew.trees_read(energy, 'truth', ['omeganpw'])
    selecters = hopp.selecters()
    docuts = hopp.docuts()
    # 初始化truth, MC数据
    selecters['omega_m'].set_width(0.15)
    alldata_fit4c = hnew.ALLDATA(trees=treesf,
                                 selecters=selecters,
                                 massages=massages)
    alldata_truth = hnew.ALLDATA(trees=treest,
                                 selecters=selecters,
                                 massages=massages)
    alldata_fit4c.get_weighter(data='omeganpw',
                               energy=energy,
                               name_weight='omegapi02_m_pi02pi03_m',
                               name_branch='1')
    alldata_truth.get_weighter(data='omeganpw',
                               energy=energy,
                               name_weight='omegapi02_m_pi02pi03_m',
                               name_branch='1')
    alldata_fit4c.selecters['t_is_isr'] = hnew.SELECTER_value(values=[1])
    entry_fit4c_isr = alldata_fit4c.statis(data='omeganpw',
                                           docuts=docuts + ['t_is_isr'],
                                           doweight=['1'])
    alldata_fit4c.selecters['t_is_isr'] = hnew.SELECTER_value(values=[0])
    entry_fit4c_nsr = alldata_fit4c.statis(data='omeganpw',
                                           docuts=docuts + ['t_is_isr'],
                                           doweight=['1'])
    alldata_truth.selecters['is_isr'] = hnew.SELECTER_value(values=[1])
    entry_truth_isr = alldata_truth.statis(data='omeganpw',
                                           docuts=['is_isr'],
                                           doweight=['1'])
    entry_conexc_isr = alldata_truth.statis(data='omeganpw',
                                            docuts=['is_isr'],
                                            doweight=[])
    alldata_truth.selecters['is_isr'] = hnew.SELECTER_value(values=[0])
    entry_truth_nsr = alldata_truth.statis(data='omeganpw',
                                           docuts=['is_isr'],
                                           doweight=['1'])
    entry_conexc_nsr = alldata_truth.statis(data='omeganpw',
                                            docuts=['is_isr'],
                                            doweight=[])
    # 输出数据
    hprint.ppoint('     ISR Generated', '%d' % (entry_conexc_isr))
    hprint.ppoint('None ISR Generated', '%d' % (entry_conexc_nsr))
    hprint.ppoint('     ISR Weighted truth', '%d' % (entry_truth_isr))
    hprint.ppoint('None ISR Weighted truth', '%d' % (entry_truth_nsr))
    hprint.ppoint('     ISR Weighted fit4c', '%d' % (entry_fit4c_isr))
    hprint.ppoint('None ISR Weighted fit4c', '%d' % (entry_fit4c_nsr))
    efficiency_isr = entry_fit4c_isr / entry_truth_isr
    efficiency_nsr = entry_fit4c_nsr / entry_truth_nsr
    hprint.ppoint('     ISR Efficiency', '%.5f' % (efficiency_isr))
    hprint.ppoint('None ISR Efficiency', '%.5f' % (efficiency_nsr))
    efficiency = (efficiency_isr * entry_conexc_isr + efficiency_nsr * entry_conexc_nsr) / (entry_conexc_isr + entry_conexc_nsr)
    efficiency_fake = (entry_fit4c_isr + entry_fit4c_nsr) / (entry_truth_isr + entry_truth_nsr)
    hprint.ppoint('     Total Efficiency', '%.5f' % (efficiency))
    hprint.ppoint('Fake Total Efficiency', '%.5f' % (efficiency_fake))
    hprint.pstar()
    return efficiency


# 读取信息
massages = hnew.massage_read()
energy_sort = hopp.energy_sort()
fileefficiency = '%s.pkl' % (massages['efficiency'])
# 进行统计
output = {}
for energy in energy_sort:
    output[energy] = effect(energy)
# 输出
hfile.pkl_dump(fileefficiency, output)
