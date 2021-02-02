# -*- coding: UTF-8 -*-
# Public pack
import numpy
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
# Private pack
import headpy.hfile as hfile
import headpy.hbes.hopp as hopp
import headpy.hbes.hnew as hnew


def func(x, a, b, c, d):
    x0 = 1
    x1 = x
    x2 = x**2
    x3 = x**3
    output = a * x3 + b * x2 + c * x1 + d * x0
    return output


# 拟合fake参数部分
print('程序开始，正在输入参数')
fix = [1.08581592, 1.26796715, 1.12736264, 1.16136756, 1.15003349, 1.21386162,
       1.24155302, 1.31855993, 1.31857755, 1.61622019, 1.59340216, 1.77063659]
energy_list = hopp.energy_list()
energy_order = energy_list.keys()
energy_order.sort()
energy_list_pw = hopp.energy_list_pw()
energy_order_pw = energy_list_pw.keys()
energy_order_pw.sort()
x = numpy.array(energy_order_pw)
y = numpy.array(fix)
print('开始进行拟合')
ppara, pcov = curve_fit(func, x, y)
nx = numpy.arange(1.9, 3.1, 0.01)
ny = func(nx, ppara[0], ppara[1], ppara[2], ppara[3])
plt.plot(nx, ny)
plt.plot(x, y)
print('开始进行作图')
plt.show()

# 输出fake效果部分
print('开始输出数据')
massages = hnew.massage_read()
parameter = {}
for energy in energy_order:
    parameter[energy] = 1 * func(energy, ppara[0], ppara[1], ppara[2], ppara[3])
    print('%1.4f: %1.4f' % (energy, parameter[energy]))
hfile.pkl_dump('%s.pkl' % (massages['fake']), parameter)
