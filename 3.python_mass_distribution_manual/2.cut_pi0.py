# -*- coding: UTF-8 -*-
# Public pack
import os
import sys
# Private pack
import ROOT
import headpy.hbes.hopp as hopp
import headpy.hbes.hnew as hnew
import headpy.hbes.hstyle as hstyle
import headpy.hbes.hconst as hconst

################################################################################
# 设定
picture_folder1 = 'picture/1.Analysis/3.1_Criteria_of_mpi01'
picture_folder2 = 'picture/1.Analysis/3.2_Criteria_of_mpi02'
picture_folder3 = 'picture/1.Analysis/3.3_Criteria_of_mpi03'
tree = 'fit4c'
branch1 = 'pi01_m'
branch2 = 'pi02_m'
branch3 = 'pi03_m'
################################################################################


def plot(energy=0,
         tree='',
         branch='',
         pictures=[],
         stop=''):
    # 读取数据
    sigma = {}
    sigma['pi01_m'] = {}
    sigma['pi02_m'] = {}
    sigma['pi03_m'] = {}
    sigma['pi01_m']['l'] = 0.009609
    sigma['pi02_m']['l'] = 0.009231
    sigma['pi03_m']['l'] = 0.007509
    sigma['pi01_m']['r'] = 0.008620
    sigma['pi02_m']['r'] = 0.010711
    sigma['pi03_m']['r'] = 0.009896
    l = sigma[branch]['l']
    r = sigma[branch]['r']
    m0 = hconst.pdg()['m_pi0']
    massages = hnew.massage_read()
    trees = hnew.trees_read(energy=energy,
                            tree=tree,
                            read=['real', 'omeganpw'])
    selecters = hopp.selecters()
    selecters[branch].set_by_center(hconst.pdg()['m_pi0'],
                                    hconst.pdg()['m_pi0'])
    # 初始化数据
    docuts = hopp.docuts()
    namef = {}
    nameh = {}
    selecters['omega_m'].set_width(0.05)
    alldata = hnew.ALLDATA(trees=trees,
                           selecters=selecters,
                           massages=massages)
    alldata.get_weighter(data='omeganpw',
                         energy=energy,
                         name_weight='omegapi02_m_pi02pi03_m',
                         name_branch='wpi02_pi02pi03')
    namef['r'], nameh['r'] = alldata.hist(data='real',
                                          branchs=[branch],
                                          docuts=docuts,
                                          name='real')
    namef['m'], nameh['m'] = alldata.hist(data='omeganpw',
                                          branchs=[branch],
                                          docuts=docuts,
                                          doweight=['wpi02_pi02pi03'],
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
    hr = thist['r'].GetMaximum()
    entries['weight'] = alldata.statis(data='omeganpw',
                                       docuts=docuts,
                                       doweight=['wpi02_pi02pi03'])
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
    thist['stack'] = ROOT.THStack('stack', '')
    thist['stack'].Add(thist['b1'])
    thist['stack'].Add(thist['b2'])
    thist['stack'].Add(thist['m'])
    # 2.get legend & arrow
    drawlist = []
    drawlist = hstyle.add_arrow(drawlist,
                                hconst.pdg()['m_pi0'], 0,
                                hconst.pdg()['m_pi0'], 1.2 * hr,
                                2, 3)
    drawlist = hstyle.add_arrow(drawlist,
                                m0 - 3 * l, 0,
                                m0 - 3 * l, 1.2 * hr,
                                2, 3)
    drawlist = hstyle.add_arrow(drawlist,
                                m0 + 3 * r, 0,
                                m0 + 3 * r, 1.2 * hr,
                                2, 3)
    legendlist = hstyle.get_legend([[thist['r'], 'Real data', 'lp'],
                                    [thist['m'], 'Signal MC', 'f'],
                                    [thist['b1'], 'Background (Left)', 'f'],
                                    [thist['b2'], 'Background (Right)', 'f']],
                                   header='Energy: %1.4f GeV' % (energy))
    drawlist.append(legendlist)
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
    os.system('mkdir %s' % (picture_folder1))
    os.system('mkdir %s' % (picture_folder2))
    os.system('mkdir %s' % (picture_folder3))
    for i in energy_sort:
        plot(energy=i,
             tree=tree,
             branch=branch1,
             pictures=['%s/%5d.pdf' % (picture_folder1, 10000 * i),
                       '%s/%5d.jpg' % (picture_folder1, 10000 * i)],
             stop='')
        plot(energy=i,
             tree=tree,
             branch=branch2,
             pictures=['%s/%5d.pdf' % (picture_folder2, 10000 * i),
                       '%s/%5d.jpg' % (picture_folder2, 10000 * i)],
             stop='')
        plot(energy=i,
             tree=tree,
             branch=branch3,
             pictures=['%s/%5d.pdf' % (picture_folder3, 10000 * i),
                       '%s/%5d.jpg' % (picture_folder3, 10000 * i)],
             stop='')
elif(float(sys.argv[1]) in energy_sort):
    plot(float(sys.argv[1]),
         tree='fit4c',
         branch=branch1,
         pictures=[],
         stop='yes')
else:
    print('Error energy point')
