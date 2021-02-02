# -*- coding: UTF-8 -*-
# Public package
# Private package

class SYSUNCERTAINTY:
    def __init__(self, name=''):
        self.constant = 0
        self.variable = 0
        self.name = name

    def set_constant(self, error):
        self.constant = 1
        self.error = error

    def set_variable(self, error_dict):
        self.variable = 1
        self.error_dict = error_dict

    def get_error(self, energy):
        if(self.constant == 1):
            output = self.error
        elif(self.variable == 1):
            output = self.error_dict[energy]
        return output

