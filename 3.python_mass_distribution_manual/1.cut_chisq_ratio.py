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
picture_folder = 'picture/1.Analysis/2.1_Criteria_of_fom'
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
                            read=['real'])
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
    alldata1.selecters['omega_m'].shift(-0.15)
    namef['b1'], nameh['b1'] = alldata1.hist(data='real',
                                             branchs=[branch],
                                             docuts=['pi01_m', 'pi02_m', 'pi03_m', 'omega_m'],
                                             name='back1')
    alldata2.selecters['omega_m'].shift(0.15 + 0.15)
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
    indexs = selecters[branch].inter
    # 统计序列
    content_r = []
    content_b = []
    for index in range(indexs):
        content_r.append(thist['r'].GetBinContent(index))
        content_b.append(0.5 * (thist['b1'].GetBinContent(index) + thist['b2'].GetBinContent(index)))
    all_r = 0
    all_b = 0
    fom = []
    efom = []
    for index in range(indexs):
        all_r += content_r[index]
        all_b += content_b[index]
        if(all_r == 0):
            fom.append(0)
            efom.append(0)
        else:
            fom.append((all_r - all_b) / pow(all_r, 0.5))
            efom.append(((0.5 * (1 + all_b / all_r))**2 + (all_b / all_r))**0.5)
    hr = (all_r - all_b) / pow(all_r, 0.5)
    # 2.set style
    hstyle.set_style()
    # 2.get canvas
    canvas = hstyle.get_canvas()
    # 2.get tgraph
    error_ratio = ROOT.TGraphErrors(indexs)
    for i in range(indexs):
        error_ratio.SetPoint(i, 4 * i, fom[i])
        error_ratio.SetPointError(i, 0, efom[i])
    # 2.set style
    hstyle.set_style()
    hstyle.set_axis(error_ratio,
                    '#chi_{#pi^{+}#pi^{-}6#gamma}^{2}',
                    'S/#sqrt{S+B}')
    error_ratio.SetMarkerStyle(7)
    error_ratio.GetXaxis().SetRangeUser(0, 200)
    error_ratio.GetYaxis().SetRangeUser(0, 2 * hr)
    # 2.get legend & arrow
    drawlist = []
    drawlist = hstyle.add_arrow(drawlist,
                                100, 0,
                                100, 2 * hr,
                                2, 3)
    # 3.draw
    error_ratio.Draw('AP')
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
