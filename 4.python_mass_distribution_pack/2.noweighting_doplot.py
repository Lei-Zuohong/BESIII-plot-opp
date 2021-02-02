# -*- coding: UTF-8 -*-
# Public package
import os
import sys
# Private package
import ROOT
import headpy.hbes.hopp as hopp
import headpy.hbes.hnew as hnew
import headpy.hbes.hstyle as hstyle


def plot(energy=0,
         tree='',
         branch='',
         pictures=[],
         stop=''):
    # 读取数据
    massages = hnew.massage_read()
    trees = hnew.trees_read(energy=energy,
                            tree=tree,
                            read=['real', 'omeganpw'])
    selecters = hopp.selecters()
    # 初始化数据
    alldata = hnew.ALLDATA(trees=trees,
                           selecters=selecters,
                           massages=massages)
    docuts = hopp.docuts()
    namef = {}
    nameh = {}
    alldata.selecters['omega_m'].set_width(0.05)
    namef['r'], nameh['r'] = alldata.hist(data='real',
                                          branchs=[branch],
                                          docuts=docuts,
                                          name='real')
    namef['m'], nameh['m'] = alldata.hist(data='omeganpw',
                                          branchs=[branch],
                                          docuts=docuts,
                                          name='omeganpw')
    alldata.selecters['omega_m'].shift(-0.15)
    namef['b1'], nameh['b1'] = alldata.hist(data='real',
                                            branchs=[branch],
                                            docuts=docuts,
                                            name='back1')
    alldata.selecters['omega_m'].shift(0.15 + 0.15)
    namef['b2'], nameh['b2'] = alldata.hist(data='real',
                                            branchs=[branch],
                                            docuts=docuts,
                                            name='back2')
    alldata.selecters['omega_m'].shift(-0.15)
    # 读取数据对象
    tfile = {}
    thist = {}
    entries = {}
    for i in namef:
        tfile[i] = ROOT.TFile(namef[i])
        thist[i] = tfile[i].Get(nameh[i])
        entries[i] = thist[i].GetEntries()
    # 1.calculation
    entries['weight'] = alldata.statis(data='omeganpw',
                                       docuts=docuts)
    thist['m'].Scale((entries['r'] - 0.5 * entries['b1'] - 0.5 * entries['b2']) / entries['weight'])
    thist['b1'].Scale(0.5)
    thist['b2'].Scale(0.5)
    # 2.set style
    hstyle.set_style()
    # 2.get canvas
    canvas = hstyle.get_canvas(1200, 900, 1, 1)
    # 2.set style
    xtitle, ytitle = alldata.selecters[branch].get_title()
    hstyle.set_axis(thist['r'], xtitle, ytitle)
    hstyle.set_height(thist['r'], 1.5)
    hstyle.set_marker(thist['r'])
    hstyle.set_background(thist['m'])
    hstyle.set_background(thist['b1'], Fillcolor=2, Linecolor=2)
    hstyle.set_background(thist['b2'], Fillcolor=3, Linecolor=3)
    if(branch in ['omegapi03_m', 'omegapi02_m', 'pi02pi03_m']):
        hstyle.set_xrange(thist['r'])
    thist['stack'] = ROOT.THStack('stack', '')
    thist['stack'].Add(thist['b1'])
    thist['stack'].Add(thist['b2'])
    thist['stack'].Add(thist['m'])
    ################################
    # 2. get legend & arrow
    ################################
    drawlist = []
    legendlist = hstyle.get_legend([[thist['r'], 'Real data', 'lp'],
                                    [thist['m'], 'Signal MC', 'f'],
                                    [thist['b1'], 'Background (Left)', 'f'],
                                    [thist['b2'], 'Background (Right)', 'f']],
                                   header='Energy: %1.4f GeV' % (energy),
                                   d=0.75, l=0.65)
    drawlist.append(legendlist)
    ################################
    # 3. draw
    ################################
    thist['r'].Draw('E1')
    thist['stack'].Draw('sameHIST')
    for i in drawlist:
        i.Draw('same')
    for i in pictures:
        canvas.Print(i)
        print('Done print to:')
        print('%s' % (i))
    if(stop != ''):
        input()


option1 = sys.argv[1]  # 判断单个能量点测试，或者批量输出文件
option2 = sys.argv[2]  # 文件夹名
option3 = sys.argv[3]  # branch名
energy_sort = hopp.energy_sort()

if(sys.argv[1] == '-1'):
    os.system('mkdir picture/2.Mass_Distribution_noweight/%s' % (option2))
    for i in energy_sort:
        plot(energy=i,
             tree='fit4c',
             branch=option3,
             pictures=['picture/2.Mass_Distribution_noweight/%s/%05d.pdf' % (option2, 10000 * i),
                       'picture/2.Mass_Distribution_noweight/%s/%05d.jpg' % (option2, 10000 * i)],
             stop='')
elif(float(option1) in energy_sort):
    plot(energy=float(option1),
         tree='fit4c',
         branch=option3,
         pictures=[],
         stop='yes')
else:
    print('Error energy point')
