# -*- coding: UTF-8 -*-
# Public package
import threading
# Private package
import default as default
import headpy.hbes.hnew as hnew
################################################################################
# dump常规root文件
dump_real = 0
dump_omeganpw = 1
dump_omeganpw_truth = 0
################################################################################


class mythread(threading.Thread):
    def __init__(self, location, tree, branchs, tree_cut=0):
        threading.Thread.__init__(self)
        self.location = location
        self.tree = tree
        self.branchs = branchs
        self.tree_cut = tree_cut

    def run(self):
        print('开始线程: %s' % (self.location))
        hnew.dump(hnew.root_dict,
                  folder_root=self.location,
                  tree=self.tree,
                  branchs=self.branchs,
                  tree_cut=self.tree_cut)
        print('结束线程: %s' % (self.location))


# 输入文件地址
massages = hnew.massage_read()
location1 = '%s' % (massages['real'])
location2 = '%s' % (massages['omeganpw'])
# 创建进程
thread1 = mythread(location1, 'fit4c', default.branchs_fit4c)
thread2 = mythread(location2, 'fit4c', default.branchs_fit4c_truth)
thread3 = mythread(location2, 'truth', default.branchs_truth)
# 开始进程
if(dump_real == 1):
    thread1.start()
if(dump_omeganpw == 1):
    thread2.start()
if(dump_omeganpw_truth == 1):
    thread3.start()
# 停止进程
if(dump_real == 1):
    thread1.join()
if(dump_omeganpw == 1):
    thread2.join()
if(dump_omeganpw_truth == 1):
    thread3.join()
