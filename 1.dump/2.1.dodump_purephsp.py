# -*- coding: UTF-8 -*-
# Public package
import os
import re
import numpy
import threading
# Private package
import ROOT
import headpy.hfile as hfile
import headpy.hbes.hnew as hnew
import headpy.hscreen.hprint as hprint
################################################################################
# dump purephsp文件
################################################################################

# 确定读取的branch
branchs_fit4c = ['chisq',
                 'fpi12_m',
                 'fpi13_m',
                 'fpi23_m',

                 'pip_m', 'pip_p', 'pip_a',  # 'pip_pe', 'pip_px', 'pip_py', 'pip_pz',
                 'pim_m', 'pim_p', 'pim_a',  # 'pim_pe', 'pim_px', 'pim_py', 'pim_pz',
                 'pi01_m', 'pi01_p', 'pi01_a',  # 'pi01_pe', 'pi01_px', 'pi01_py', 'pi01_pz',
                 'pi02_m', 'pi02_p', 'pi02_a',  # 'pi02_pe', 'pi02_px', 'pi02_py', 'pi02_pz',
                 'pi03_m', 'pi03_p', 'pi03_a',  # 'pi03_pe', 'pi03_px', 'pi03_py', 'pi03_pz',
                 'omega_m', 'omega_p', 'omega_a',  # 'omega_pe', 'omega_px', 'omega_py', 'omega_pz',
                 'omegapi02_m', 'omegapi02_p',  # 'omegapi02_a', 'omegapi02_pe', 'omegapi02_px', 'omegapi02_py', 'omegapi02_pz',
                 'omegapi03_m', 'omegapi03_p',  # 'omegapi03_a', 'omegapi03_pe', 'omegapi03_px', 'omegapi03_py', 'omegapi03_pz',
                 'pi02pi03_m', 'pi02pi03_p',  # 'pi02pi03_a', 'pi02pi03_pe', 'pi02pi03_px', 'pi02pi03_py', 'pi02pi03_pz',
                 ]
# 输入文件地址
massages = hnew.massage_read()
location1 = '%s' % (massages['purephsp'])
hnew.dump(hnew.root_dict,
          folder_root=location1,
          tree='fit4c',
          branchs=branchs_fit4c)
