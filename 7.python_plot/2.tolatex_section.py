# -*- coding: UTF-8 -*-
import math
import headpy.hfile as hfile
import headpy.hbes.hnew as hnew
import headpy.hbes.hopp as hopp
import headpy.hbes.hconst as hconst


massages = hnew.massage_read()
data = hfile.pkl_read('%s.pkl' % (massages['section']))
syse = hfile.pkl_read('8.python_error/data/error_total.pkl')
energy_sort = hopp.energy_sort()
output = ''
output += '{:^20}'.format('$\\sqrt{S}$ (GeV)')
output += '&{:^20}'.format('Events')
output += '&{:^20}'.format('$L(pb^{-1})$')
output += '&{:^25}'.format('$\\varepsilon$_noweight')
output += '&{:^20}'.format('$\\varepsilon$')
output += '&{:^15}'.format('ISR factor')
output += '&{:^15}'.format('VP factor')
output += '&{:^35}'.format('Cross section(pb)')
output += '\\\\\\hline'
print(output)
for i in energy_sort:
    output = ''
    output += '{:^20}'.format('%1.4f' % (i))
    output += '&{:^20}'.format('%.2f$\\pm$%.2f' % (data[i]['Nsignal'], data[i]['eNsignal']))
    output += '&{:^20}'.format('%s' % (hconst.energy_list()[i][3]))
    output += '&{:^25}'.format('%.2f' % (data[i]['Efficiency_noweight']))
    output += '&{:^20}'.format('%.2f' % (data[i]['Efficiency']))
    output += '&{:^15}'.format('%.2f' % (data[i]['isr']))
    output += '&{:^15}'.format('%.2f' % (data[i]['vpf']))
    output += '&{:^35}'.format('%.2f$\\pm$%.2f$\\pm$%.2f' % (data[i]['Section'],
                                                             data[i]['eSection'],
                                                             data[i]['Section'] * syse[i] / 100))
    output += '\\\\'
    print(output)
print('结束输出')
if(1 == 1):
    output_s = '{'
    output_e = '{'
    for i in energy_sort:
        output_s += '%.3f,' % (data[i]['Section'])
        error_sta = data[i]['eSection']
        error_sys = data[i]['Section'] * syse[i] / 100
        error_total = math.sqrt(error_sta * error_sta + error_sys * error_sys)
        output_e += '%.4f,' % (error_total)
    output_s += '}'
    output_e += '}'
    print(output_s)
    print(output_e)
