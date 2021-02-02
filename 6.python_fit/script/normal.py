# -*- coding: UTF-8 -*-
# Public package
import sys
# Private package
import headpy.hfile as hfile

option = sys.argv[1]
argv = hfile.pkl_read(option)

output = argv['func_fit'](**argv)