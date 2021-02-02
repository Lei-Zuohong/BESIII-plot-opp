# -*- coding: UTF-8 -*-
# Public pack
import sys
# Private pack
import ROOT
import headpy.hbes.hopp as hopp
import headpy.hbes.hstyle as hstyle
import headpy.hbes.hnew as hnew
import headpy.hbes.hconst as hconst


def plot(energy=0,
         pictures=[],
         stop=''):
    # 读取数据
    branch1 = 'dalitz_x1'
    branch2 = 'dalitz_y1'
    massages = hnew.massage_read()
    trees_f = hnew.trees_read(energy=energy,
                              tree='fit4c',
                              read=['selected_real', 'selected_omeganpw'])
    trees_t = hnew.trees_read(energy=energy,
                              tree='truth',
                              read=['selected_omeganpw'])
    selecters = hopp.selecters()
    selecters['omega_m'].set_width(0.15)
    # 初始化数据
    alldata_f = hnew.ALLDATA(trees=trees_f,
                             selecters=selecters,
                             massages=massages)
    alldata_t = hnew.ALLDATA(trees=trees_t,
                             selecters=selecters,
                             massages=massages)
    tfile = {}
    thist = {}
    tfile['r'], thist['r'] = alldata_f.hist(data='selected_real',
                                            branchs=[branch1, branch2],
                                            docuts=['chisq', 'pi01_m', 'pi02_m', 'pi03_m', 'omega_m'],
                                            name='dalitz_r')
    tfile['m'], thist['m'] = alldata_f.hist(data='selected_omeganpw',
                                            branchs=[branch1, branch2],
                                            docuts=['chisq', 'pi01_m', 'pi02_m', 'pi03_m', 'omega_m'],
                                            name='dalitz_m')
    tfile['t'], thist['t'] = alldata_t.hist(data='selected_omeganpw',
                                            branchs=[branch1, branch2],
                                            docuts=['pi01_m', 'pi02_m', 'pi03_m', 'omega_m'],
                                            name='dalitz_t')
    # 读取数据对象
    file = {}
    hist = {}
    for i in tfile:
        file[i] = ROOT.TFile(tfile[i])
        hist[i] = file[i].Get(thist[i])
    # 2.set style
    hstyle.set_style()
    # 2.get canvas
    canvas = hstyle.get_canvas(2700, 600, 3, 1)
    # 2.set style
    xtitle, xtitle1 = selecters[branch1].get_title()
    ytitle, ytitle1 = selecters[branch2].get_title()
    hstyle.set_axis(hist['r'], xtitle, ytitle)
    hstyle.set_axis(hist['m'], xtitle, ytitle)
    hstyle.set_axis(hist['t'], xtitle, ytitle)
    # 2.get legend & arrow
    canvas.cd(1)
    hist['r'].Draw('COLZ')
    canvas.cd(2)
    hist['m'].Draw('COLZ')
    canvas.cd(3)
    hist['t'].Draw('COLZ')

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
         pictures=[],
         stop='yes')
else:
    print('Error energy point')
