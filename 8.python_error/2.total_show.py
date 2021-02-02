# -*- coding: UTF-8 -*-
# Public package
import math
# Private package
import headpy.hfile as hfile
import headpy.hbes.hopp as hopp


# 读取数据
errors = []
errors.append(hfile.pkl_read('8.python_error/data/error_lumin.pkl'))
errors.append(hfile.pkl_read('8.python_error/data/error_charge.pkl'))
errors.append(hfile.pkl_read('8.python_error/data/error_pid.pkl'))
errors.append(hfile.pkl_read('8.python_error/data/error_photon.pkl'))
errors.append(hfile.pkl_read('8.python_error/data/error_branch.pkl'))
errors.append(hfile.pkl_read('8.python_error/data/error_kinematic.pkl'))
errors.append(hfile.pkl_read('8.python_error/data/error_background.pkl'))
errors.append(hfile.pkl_read('8.python_error/data/error_signal.pkl'))
errors.append(hfile.pkl_read('8.python_error/data/error_windowpi.pkl'))
errors.append(hfile.pkl_read('8.python_error/data/error_windowo.pkl'))
errors.append(hfile.pkl_read('8.python_error/data/error_isr.pkl'))
# 初始化最终结果
error_total = {}
# 循环能量点
energy_sort = hopp.energy_sort()
output = ''
output += '{:^12}&'.format('Energy')
for error in errors:
    output += '{:^12}&'.format(error.name)
output += '{:^12} \\\\\\hline'.format('Total')
print(output)
error_total = {}
for energy in energy_sort:
    total = 0
    output = ''
    output += '{:^12}&'.format('%1.4f' % (energy))
    for error in errors:
        if(error.name in ['L', 'Charged', 'PID', 'Photon', 'Br', '1+delta']):
            output += '{:^12}&'.format('%1.1f' % (error.get_error(energy)))
        else:
            output += '{:^12}&'.format('%1.2f' % (error.get_error(energy)))
        total += (error.get_error(energy))**2
    total = math.sqrt(total)
    output += '{:^12} \\\\'.format('%1.2f' % (total))
    error_total[energy] = total
    print(output)
hfile.pkl_dump('8.python_error/data/error_total.pkl', error_total)
