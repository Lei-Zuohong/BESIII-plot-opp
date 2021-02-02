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
picture_folder1 = 'picture/1.Analysis/4.1_Sideband_of_mpi01'
picture_folder2 = 'picture/1.Analysis/4.2_Sideband_of_mpi02'
picture_folder3 = 'picture/1.Analysis/4.3_Sideband_of_mpi03'
tree = 'fit4c'
branch = 'omega_m'
branch1 = 'pi01_m'
branch2 = 'pi02_m'
branch3 = 'pi03_m'
################################################################################


def plot(energy=0,
         tree='',
         branch1='omega_m',
         branch2='',
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
    # 定义常数
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
    l0 = sigma[branch2]['l']
    r0 = sigma[branch2]['r']
    m0 = hconst.pdg()['m_pi0']
    allcuts = ['chisq', 'pi02_m', 'pi03_m', 'pi01_m']
    threecuts = []
    for i in allcuts:
        if(i != branch2):
            threecuts.append(i)
    # 初始化数据
    alldata = hnew.ALLDATA(trees=trees,
                           selecters=selecters,
                           massages=massages)
    alldata.selecters[branch2].set_scale_show(3)
    namef['2'], nameh['2'] = alldata.hist(data='real',
                                          branchs=[branch1, branch2],
                                          docuts=threecuts,
                                          name='data2')
    namef['r'], nameh['r'] = alldata.hist(data='real',
                                          branchs=[branch1],
                                          docuts=allcuts,
                                          name='datar')
    # 读取右侧sideband
    alldata.selecters[branch2].shift(- 9 * r0)
    namef['s'], nameh['s'] = alldata.hist(data='real',
                                          branchs=[branch1],
                                          docuts=allcuts,
                                          name='datas')
    # 读取左侧sideband
    # 读取数据对象
    tfile = {}
    thist = {}
    for i in namef:
        tfile[i] = ROOT.TFile(namef[i])
        thist[i] = tfile[i].Get(nameh[i])
    # 1.calculation
    # 2.set style
    hstyle.set_style()
    # 2.get canvas
    canvas = hstyle.get_canvas(600, 900, 1, 2)
    # 2.set style
    xtitle, xtitle1 = alldata.selecters[branch1].get_title()
    ytitle, ytitle1 = alldata.selecters[branch2].get_title()
    hstyle.set_axis(thist['2'], xtitle, ytitle)
    hstyle.set_axis(thist['r'], xtitle, xtitle1)
    hstyle.set_height(thist['r'], 1.5)
    hstyle.set_marker(thist['r'])
    hstyle.set_background(thist['s'])
    # 2.get legend & arrow
    drawlist1 = []
    momegaleft, momegaright = alldata.selecters['omega_m'].get_range_show()
    drawlist1 = hstyle.add_box(drawlist1,
                               momegaleft, momegaright,
                               m0 - 3 * l0, m0 + 3 * r0,
                               2, 3)
    drawlist1 = hstyle.add_box(drawlist1,
                               momegaleft, momegaright,
                               m0 - 12 * l0, m0 - 6 * l0,
                               3, 3)
    drawlist1 = hstyle.add_box(drawlist1,
                               momegaleft, momegaright,
                               m0 + 6 * r0, m0 + 12 * r0,
                               3, 3)
    drawlist2 = []
    legendlist = hstyle.get_legend(legendlist=[[thist['r'], 'Signal region', 'lp'],
                                               [thist['s'], 'Sideband region', 'f']],
                                   header='Energy: %1.4f GeV' % (energy))
    drawlist2.append(legendlist)

    # 3.draw
    canvas.cd(1)
    thist['2'].Draw('COLZ')
    for i in drawlist1:
        i.Draw('same')

    canvas.cd(2)
    thist['r'].Draw('sameE1')
    thist['s'].Draw('sameHIST')
    for i in drawlist2:
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
             branch1=branch,
             branch2=branch1,
             pictures=['%s/%5d.pdf' % (picture_folder1, 10000 * i),
                       '%s/%5d.jpg' % (picture_folder1, 10000 * i)],
             stop='')
        plot(energy=i,
             tree=tree,
             branch1=branch,
             branch2=branch2,
             pictures=['%s/%5d.pdf' % (picture_folder2, 10000 * i),
                       '%s/%5d.jpg' % (picture_folder2, 10000 * i)],
             stop='')
        plot(energy=i,
             tree=tree,
             branch1=branch,
             branch2=branch3,
             pictures=['%s/%5d.pdf' % (picture_folder3, 10000 * i),
                       '%s/%5d.jpg' % (picture_folder3, 10000 * i)],
             stop='')
elif(float(sys.argv[1]) in energy_sort):
    plot(float(sys.argv[1]),
         tree='fit4c',
         branch1=branch,
         branch2=branch1,
         pictures=[],
         stop='yes')
else:
    print('Error energy point')
