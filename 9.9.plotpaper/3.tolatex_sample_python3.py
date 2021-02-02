# -*- coding: UTF-8 -*-
import headpy.hbes.hconst as hconst

energy_list = hconst.energy_list()
order_list = [3.0800,
              3.0200,
              3.0000,
              2.9810,
              2.9500,
              2.9000,
              2.8000,
              2.7000,
              2.6464,
              2.6444,
              2.5000,
              2.3960,
              2.3864,
              2.3094,
              2.2324,
              2.2000,
              2.1750,
              2.1500,
              2.1250,
              2.1000,
              2.0500,
              2.0000]
for i in order_list:
    output = ''
    output += '%1.4f' % (i)
    output += ' & %s' % (energy_list[i][3])
    output += ' & %5d-%5d' % (energy_list[i][0], energy_list[i][1])
    output += ' \\\\\\hline'
    print(output)
