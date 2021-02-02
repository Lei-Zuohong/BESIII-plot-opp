# -*- coding: UTF-8 -*-
# Public package
# Private package
import default as default
import headpy.hfile as hfile

error_lumin = default.SYSUNCERTAINTY('L')
error_lumin.set_constant(1.0)
hfile.pkl_dump('8.python_error/data/error_lumin.pkl', error_lumin)

error_charge = default.SYSUNCERTAINTY('Charged')
error_charge.set_constant(2.0)
hfile.pkl_dump('8.python_error/data/error_charge.pkl', error_charge)

error_pid = default.SYSUNCERTAINTY('PID')
error_pid.set_constant(2.0)
hfile.pkl_dump('8.python_error/data/error_pid.pkl', error_pid)

error_photon = default.SYSUNCERTAINTY('Photon')
error_photon.set_constant(6.0)
hfile.pkl_dump('8.python_error/data/error_photon.pkl', error_photon)

error_branch = default.SYSUNCERTAINTY('Br')
error_branch.set_constant(0.7)
hfile.pkl_dump('8.python_error/data/error_branch.pkl', error_branch)

dict_kinematic = {2.0000: 0.57,
                  2.0500: 0.55,
                  2.1000: 0.66,
                  2.1250: 0.36,
                  2.1500: 0.68,
                  2.1750: 0.46,
                  2.2000: 0.52,
                  2.2324: 0.47,
                  2.3094: 0.36,
                  2.3864: 0.34,
                  2.3960: 0.54,
                  2.6444: 0.39,
                  2.6464: 0.60,
                  2.9000: 0.23,
                  2.9500: 0.49,
                  2.9810: 0.50,
                  3.0000: 0.64,
                  3.0200: 0.26,
                  3.0800: 0.35}
error_kinematic = default.SYSUNCERTAINTY('4C')
error_kinematic.set_variable(dict_kinematic)
hfile.pkl_dump('8.python_error/data/error_kinematic.pkl', error_kinematic)

dict_background = {2.0000: 0.22,
                   2.0500: 0.10,
                   2.1000: 0.17,
                   2.1250: 0.19,
                   2.1500: 0.12,
                   2.1750: 0.11,
                   2.2000: 0.19,
                   2.2324: 0.14,
                   2.3094: 0.93,
                   2.3864: 0.14,
                   2.3960: 0.11,
                   2.6444: 0.17,
                   2.6464: 0.13,
                   2.9000: 0.17,
                   2.9500: 0.18,
                   2.9810: 0.14,
                   3.0000: 0.13,
                   3.0200: 0.14,
                   3.0800: 0.11}
error_background = default.SYSUNCERTAINTY('Bkg shape')
error_background.set_variable(dict_background)
hfile.pkl_dump('8.python_error/data/error_background.pkl', error_background)

dict_signal = {2.0000: 0.13,
               2.0500: 0.18,
               2.1000: 1.43,
               2.1250: 0.41,
               2.1500: 0.45,
               2.1750: 0.18,
               2.2000: 0.14,
               2.2324: 0.15,
               2.3094: 0.16,
               2.3864: 0.17,
               2.3960: 0.24,
               2.6444: 0.26,
               2.6464: 0.29,
               2.9000: 0.14,
               2.9500: 1.48,
               2.9810: 0.13,
               3.0000: 1.06,
               3.0200: 0.11,
               3.0800: 0.13}
error_signal = default.SYSUNCERTAINTY('Sig Shape')
error_signal.set_variable(dict_signal)
hfile.pkl_dump('8.python_error/data/error_signal.pkl', error_signal)

dict_windowpi = {2.0000: 0.18,
                 2.0500: 0.16,
                 2.1000: 0.11,
                 2.1250: 0.26,
                 2.1500: 0.14,
                 2.1750: 0.11,
                 2.2000: 0.15,
                 2.2324: 0.17,
                 2.3094: 0.18,
                 2.3864: 0.11,
                 2.3960: 0.47,
                 2.6444: 0.32,
                 2.6464: 0.10,
                 2.9000: 0.17,
                 2.9500: 0.61,
                 2.9810: 0.13,
                 3.0000: 0.13,
                 3.0200: 0.12,
                 3.0800: 0.15}
error_windowpi = default.SYSUNCERTAINTY('Pion window')
error_windowpi.set_variable(dict_windowpi)
hfile.pkl_dump('8.python_error/data/error_windowpi.pkl', error_windowpi)

dict_windowo = {2.0000: 0.18,
                2.0500: 0.18,
                2.1000: 0.11,
                2.1250: 0.17,
                2.1500: 0.14,
                2.1750: 0.18,
                2.2000: 0.16,
                2.2324: 0.52,
                2.3094: 0.16,
                2.3864: 0.13,
                2.3960: 0.10,
                2.6444: 0.36,
                2.6464: 0.16,
                2.9000: 0.15,
                2.9500: 0.77,
                2.9810: 0.11,
                3.0000: 0.66,
                3.0200: 0.17,
                3.0800: 0.10}
error_windowo = default.SYSUNCERTAINTY('Omega window')
error_windowo.set_variable(dict_windowo)
hfile.pkl_dump('8.python_error/data/error_windowo.pkl', error_windowo)

error_isr = default.SYSUNCERTAINTY('1+delta')
error_isr.set_constant(0.5)
hfile.pkl_dump('8.python_error/data/error_isr.pkl', error_isr)
