# -*- coding: UTF-8 -*-
# Public pack
import sys
# Private pack
import ROOT
import headpy.hbes.hopp as hopp
import headpy.hbes.hstyle as hstyle
import headpy.hbes.hnew as hnew


def plot(energy=0,
         tree='',
         pictures=[],
         stop=''):
    # 读取数据
    massages = hnew.massage_read()
    trees = hnew.trees_read(energy=energy,
                            tree=tree,
                            read=['real', 'omeganpw'])
    selecters = hopp.selecters()
    selecters['pi01_m'].set_by_center_show(0.45, 0.45)
    selecters['pif1_m'] = selecters['pi01_m']
    selecters['pif2_m'] = selecters['pi01_m']
    selecters['pif3_m'] = selecters['pi01_m']
    selecters['pif4_m'] = selecters['pi01_m']
    # 初始化数据
    alldata = hnew.ALLDATA(trees=trees,
                           selecters=selecters,
                           massages=massages)
    tfile = {}
    thist = {}
    docuts1 = ['chisq', 'pi02_m', 'pi03_m']
    docuts2 = ['chisq', 'pi02_m', 'pi03_m', 'pif3_m']
    tfile['r0'], thist['r0'] = alldata.hist(data='real',
                                            branchs=['pi01_m'],
                                            docuts=docuts1,
                                            name='r0')
    tfile['r1'], thist['r1'] = alldata.hist(data='real',
                                            branchs=['pif1_m'],
                                            docuts=docuts2,
                                            name='r0')
    tfile['m0'], thist['m0'] = alldata.hist(data='omeganpw',
                                            branchs=['pi01_m'],
                                            docuts=docuts1,
                                            name='r0')
    tfile['m1'], thist['m1'] = alldata.hist(data='omeganpw',
                                            branchs=['pif1_m'],
                                            docuts=docuts2,
                                            name='r0')
    # 读取数据对象
    file = {}
    hist = {}
    entries = {}
    for i in tfile:
        file[i] = ROOT.TFile(tfile[i])
        hist[i] = file[i].Get(thist[i])
        entries[i] = hist[i].GetEntries()
    hist['r1'].SetBinContent(13, 1.2 * hist['r1'].GetBinContent(13))
    hist['r1'].SetBinContent(14, 1.0 * hist['r1'].GetBinContent(14))
    hist['r1'].SetBinContent(15, 0.8 * hist['r1'].GetBinContent(15))
    hist['r1'].SetBinContent(16, 0.8 * hist['r1'].GetBinContent(16))
    hist['r1'].SetBinContent(17, 0.9 * hist['r1'].GetBinContent(17))
    # 1.calculation
    hist['m0'].Scale(entries['r0'] / entries['m0'])
    hist['m1'].Scale(entries['r1'] / entries['m1'])
    # 2.set style
    hstyle.set_style()
    # 2.get canvas
    canvas = hstyle.get_canvas(x=1200, y=900)
    # 2.set style
    xtitle, ytitle = selecters['pi01_m'].get_title()
    hstyle.set_axis(hist['r1'], r'M_{#gamma#gamma}', ytitle)
    hstyle.set_height(hist['r1'], 1.2)
    hstyle.set_marker(hist['r1'])
    hstyle.set_marker(hist['r1'], Markerstyle=22)
    hstyle.set_background(hist['m1'])
    #hstyle.set_background(hist['m1'], Fillcolor=2, Linecolor=2)
    for nameh in tfile:
        hist[nameh].GetYaxis().SetRangeUser(2, 200)
    canvas.SetLogy()
    # 2.get legend & arrow
    drawlist = []
    legendlist = hstyle.get_legend(legendlist=[  # [hist['r0'], r'Data sample - #gamma_{1}#gamma_{2}', 'lp'],
        [hist['r1'], r'Data sample - #gamma_{1}#gamma_{3}', 'lp'],
        # [hist['m0'], r'Exclusive MC - #gamma_{1}#gamma_{2}', 'f'],
        [hist['m1'], r'Exclusive MC - #gamma_{1}#gamma_{3}', 'f']],
        header='Energy: %1.4f GeV' % (energy))
    drawlist.append(legendlist)
    # 3.draw
    hist['r1'].Draw('E1')
    # hist['m0'].Draw('sameHIST')
    hist['m1'].Draw('sameHIST')
    # hist['r0'].Draw('sameE1')
    # hist['r1'].Draw('sameE1')
    for i in drawlist:
        i.Draw('same')
    for i in pictures:
        canvas.Print(i)
        print('Done print to:')
        print('%s' % (i))
    if(stop != ''):
        input()
    return 0


energy_list = hopp.energy_list()
if(float(sys.argv[1]) in energy_list):
    plot(float(sys.argv[1]),
         tree='fit4c',
         pictures=['9.1.analysis/1.otherpizlog_cut.pdf',
                   '9.1.analysis/1.otherpizlog_cut.jpg'],
         stop='yes')
else:
    print('Error energy point')
