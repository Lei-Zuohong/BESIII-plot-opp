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
picture_folder = 'picture/1.Analysis/1.0_Criteria_of_vertex'
tree = 'vertex'
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
    selecters['chisq'].set_by_edge_show(0, 100)
    selecters['chisq'].title = r'#chi_{vertex}^{2}'
    alldata = hnew.ALLDATA(trees=trees,
                           selecters=selecters,
                           massages=massages)
    namef['r'], nameh['r'] = alldata.hist(data='real',
                                          branchs=[branch],
                                          name='chisq')
    namef['m'], nameh['m'] = alldata.hist(data='omeganpw',
                                          branchs=[branch],
                                          name='chisq')
    # 读取数据对象
    tfile = {}
    thist = {}
    entries = {}
    for i in namef:
        tfile[i] = ROOT.TFile(namef[i])
        thist[i] = tfile[i].Get(nameh[i])
        entries[i] = thist[i].GetEntries()
    # 1.calculation
    mb = thist['r'].GetMaximumBin()
    hr = thist['r'].GetBinContent(mb)
    hm = thist['m'].GetBinContent(mb)
    thist['m'].Scale(hr / hm)
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
    # 2.get legend & arrow
    drawlist = []
    legendlist = hstyle.get_legend(legendlist=[[thist['r'], 'Data sample', 'lp'],
                                               [thist['m'], 'Exclusive MC', 'f']],
                                   header='Energy: %1.4f GeV' % (energy))
    drawlist.append(legendlist)
    # 3.draw
    thist['r'].Draw('E1')
    thist['m'].Draw('sameHIST')
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
