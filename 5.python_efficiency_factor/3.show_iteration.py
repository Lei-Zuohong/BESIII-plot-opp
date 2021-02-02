# -*- coding: UTF-8 -*-
# Public package
import numpy as numpy
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
# Private package
import headpy.hfile as hfile
import headpy.hbes.hopp as hopp


def trans(factor, all_energy):
    ny = []
    for i in all_energy:
        ny.append(factor[i]['isr'] * factor[i]['vpf'])
    y = numpy.array(ny)
    return y


def trans2(factor1, factor2, all_energy):
    ny = []
    for i in all_energy:
        f1 = factor1[i]['isr'] * factor1[i]['vpf']
        f2 = factor2[i]['isr'] * factor2[i]['vpf']
        ny.append(abs(f2 - f1) / f1)
    y = numpy.array(ny)
    return y


# 读取能量
energy_list = hopp.energy_list()
all_energy = list(energy_list.keys())
all_energy.sort()
# 转换数据
factor1 = hfile.pkl_read('fdata/4.section-00-01_fake.pkl')
factor2 = hfile.pkl_read('fdata/4.section-00-02_fake.pkl')
factor3 = hfile.pkl_read('fdata/4.section-00-03_fake.pkl')
delta1 = trans(factor1, all_energy)
delta2 = trans(factor2, all_energy)
delta3 = trans(factor3, all_energy)
change23 = trans2(factor2, factor3, all_energy)

# 1.作图
if(1 == 1):
    x = numpy.array(all_energy)
    pdf = PdfPages('opicture/5_ISR_ITERATION.pdf')
    fig, axes = plt.subplots(1, 1)
    axe = axes
    axe.plot(x, delta1, label=r'Iteration 1')
    axe.plot(x, delta2, label=r'Iteration 2')
    axe.plot(x, delta3, label=r'Iteration 3')
    axe.legend(loc=1)
    axe.set_xlabel(r'Energy (GeV)')
    axe.set_ylabel(r'1+$delta$')
    pdf.savefig()
    plt.show()
    pdf.close()
    plt.close()

# 2.输出系统误差
if(1 == 0):
    output = {}
    for count, i in enumerate(all_energy):
        output[i] = change23[count]
    hfile.pkl_dump('5.python_efficiency_factor/4.isr_data.pkl', output)

# 3.输出latex
if(1 == 1):
    for count, i in enumerate(all_energy):
        v1 = delta1[count]
        v2 = delta2[count]
        v3 = delta3[count]
        d12 = abs(v2 - v1) / v1
        d23 = abs(v3 - v2) / v2
        output = '{:^15}&{:^15}&{:^15}&{:^15}&{:^15}&{:^15} \\\\\\hline'.format('%1.4f' % (i),
                                                                                '%1.4f' % (v1),
                                                                                '%1.4f' % (v2),
                                                                                '%1.4f' % (v3),
                                                                                '%1.4f' % (d12),
                                                                                '%1.4f' % (d23))
        print(output)
