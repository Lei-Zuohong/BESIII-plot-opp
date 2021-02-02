# -*- coding: UTF-8 -*-
# Public pack
import os
import sys
# Private pack
import ROOT
import headpy.hbes.hopp as hopp
import headpy.hbes.hnew as hnew
import headpy.hbes.hstyle as hstyle

################################################################################
# 设定
picture_folder = 'picture/1.Analysis/2.0_Criteria_of_kinematic'
tree = 'fit4c'
branch = 'chisq'
################################################################################


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
    namef = {}
    nameh = {}
    # 初始化数据
    selecters['omega_m'].set_width(0.05)
    alldata = hnew.ALLDATA(trees=trees,
                           selecters=selecters,
                           massages=massages)
    alldata1 = hnew.ALLDATA(trees=trees,
                            selecters=selecters,
                            massages=massages)
    alldata2 = hnew.ALLDATA(trees=trees,
                            selecters=selecters,
                            massages=massages)
    namef['r'], nameh['r'] = alldata.hist(data='real',
                                          branchs=[branch],
                                          docuts=['pi01_m', 'pi02_m', 'pi03_m', 'omega_m'],
                                          name='chisq')
    namef['m'], nameh['m'] = alldata.hist(data='omeganpw',
                                          branchs=[branch],
                                          docuts=['pi01_m', 'pi02_m', 'pi03_m', 'omega_m'],
                                          name='chisq')
    alldata1.selecters['omega_m'].shift(-0.15)
    namef['b1'], nameh['b1'] = alldata1.hist(data='real',
                                             branchs=[branch],
                                             docuts=['pi01_m', 'pi02_m', 'pi03_m', 'omega_m'],
                                             name='back1')
    alldata2.selecters['omega_m'].shift(0.15)
    namef['b2'], nameh['b2'] = alldata2.hist(data='real',
                                             branchs=[branch],
                                             docuts=['pi01_m', 'pi02_m', 'pi03_m', 'omega_m'],
                                             name='back2')
    # 读取数据对象
    tfile = {}
    thist = {}
    entries = {}
    for i in namef:
        tfile[i] = ROOT.TFile(namef[i])
        thist[i] = tfile[i].Get(nameh[i])
        entries[i] = thist[i].GetEntries()
    # 1.calculation
    hr = thist['r'].GetMaximum()
    thist['m'].Scale((entries['r'] - 0.5 * entries['b1'] - 0.5 * entries['b2']) / entries['m'])
    thist['b1'].Scale(0.5)
    thist['b2'].Scale(0.5)
    # 2.set style
    hstyle.set_style()
    # 2.get canvas
    canvas = hstyle.get_canvas()
    # 2.set style
    xtitle, ytitle = selecters[branch].get_title()
    hstyle.set_axis(thist['r'], xtitle, ytitle)
    hstyle.set_height(thist['r'], 1.5)
    hstyle.set_marker(thist['r'])
    hstyle.set_background(thist['m'])
    hstyle.set_background(thist['b1'], Fillcolor=2, Linecolor=2)
    hstyle.set_background(thist['b2'], Fillcolor=3, Linecolor=3)
    thist['stack'] = ROOT.THStack('stack', '')
    thist['stack'].Add(thist['b1'])
    thist['stack'].Add(thist['b2'])
    thist['stack'].Add(thist['m'])
    # 2.get legend & arrow
    drawlist = []
    legendlist = hstyle.get_legend([[thist['r'], 'Real data', 'lp'],
                                    [thist['m'], 'Signal MC', 'f'],
                                    [thist['b1'], 'Background (Left)', 'f'],
                                    [thist['b2'], 'Background (Right)', 'f']],
                                   header='Energy: %1.4f GeV' % (energy))
    drawlist.append(legendlist)
    drawlist = hstyle.add_arrow(drawlist,
                                100, 0,
                                100, 0.75 * hr,
                                2, 3)
    # 3.draw
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
    return 0


energy_sort = hopp.energy_sort()
if(sys.argv[1] == '-1'):
    os.system('mkdir %s' % (picture_folder))
    for i in energy_sort:
        plot(energy=i,
             tree=tree,
             branch=branch,
             pictures=['%s/%5d.pdf' % (picture_folder, 10000 * i),
                       '%s/%5d.jpg' % (picture_folder, 10000 * i)],
             stop='')
elif(float(sys.argv[1]) in energy_sort):
    plot(float(sys.argv[1]),
         tree=tree,
         branch=branch,
         pictures=[],
         stop='yes')
else:
    print('Error energy point')
