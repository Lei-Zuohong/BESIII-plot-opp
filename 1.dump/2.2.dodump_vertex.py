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
# dump其它tree文件
dump_real = 0
dump_omeganpw = 1
################################################################################

# 确定读取的branch
branchs_vertex = ['chisq']
# 输入文件地址
massages = hnew.massage_read()
location1 = '%s' % (massages['real'])
location2 = '%s' % (massages['omeganpw'])


class mythread(threading.Thread):
    def __init__(self, location, tree, branchs):
        threading.Thread.__init__(self)
        self.location = location
        self.tree = tree
        self.branchs = branchs

    def run(self):
        print('开始线程: %s' % (self.location))
        hnew.dump(hnew.root_dict,
                  folder_root=self.location,
                  tree=self.tree,
                  branchs=self.branchs)
        print('结束线程: %s' % (self.location))


# 进行dump
thread1 = mythread(location1, 'vertex', branchs_vertex)
thread2 = mythread(location2, 'vertex', branchs_vertex)
# 开始进程
if(dump_real == 1):
    thread1.start()
if(dump_omeganpw == 1):
    thread2.start()
# 停止进程
if(dump_real == 1):
    thread1.join()
if(dump_omeganpw == 1):
    thread2.join()



