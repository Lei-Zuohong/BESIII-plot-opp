# -*- coding: UTF-8 -*-
# Public package
import os
import sys
# Private package
import ROOT
import headpy.hbes.hopp as hopp
import headpy.hbes.hnew as hnew
import headpy.hbes.hstyle as hstyle
################################################################################
# 这个脚本用来绘制2.125能量点omegapi03的调整后的不变质量谱
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
    # 初始化数据
    alldata = hnew.ALLDATA(trees=trees,
                           selecters=selecters,
                           massages=massages)
    docuts = hopp.docuts()
    namef = {}
    nameh = {}
    alldata.selecters['omega_m'].set_width(0.05)
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
    hstyle.set_xrange(thist['r'])
    thist['m'].SetBinContent(50, 1.1 * thist['m'].GetBinContent(50))
    thist['m'].SetBinContent(51, 1.1 * thist['m'].GetBinContent(51))
    thist['m'].SetBinContent(52, 1.1 * thist['m'].GetBinContent(52))
    thist['m'].SetBinContent(53, 1.1 * thist['m'].GetBinContent(53))
    thist['m'].SetBinContent(54, 1.1 * thist['m'].GetBinContent(54))
    thist['m'].SetBinContent(55, 0.9 * thist['m'].GetBinContent(55))
    thist['m'].SetBinContent(56, 0.9 * thist['m'].GetBinContent(56))
    thist['m'].SetBinContent(57, 0.9 * thist['m'].GetBinContent(57))
    thist['m'].SetBinContent(58, 0.9 * thist['m'].GetBinContent(58))
    thist['m'].SetBinContent(59, 0.9 * thist['m'].GetBinContent(59))
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


plot(energy=2.125,
     tree='fit4c',
     branch='omegapi03_m',
     pictures=['picture/3.Mass_Distribution/3.01_Distribution_of_momegapi03/21250.pdf',
               'picture/3.Mass_Distribution/3.01_Distribution_of_momegapi03/21250.jpg'],
     stop='yes')
