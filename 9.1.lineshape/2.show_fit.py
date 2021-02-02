# -*- coding: UTF-8 -*-
# Public package
import numpy
# Private package
import ROOT
import default as default
import headpy.hbes.hstyle as hstyle
import headpy.hbes.hfunc as hfunc


# 设定参数
filename = '8_SHOW_FITTING.pdf'
xlim = (1.9, 3.1)
ylim = (0, 400)
steps = 0.001
# 读取数据
data_bes_opp = default.data_bes_opp_sys()
# 绘图
hstyle.set_style()
canvas = hstyle.get_canvas()
legendlist = []
if(1 == 1):
    len_bes_opp = len(data_bes_opp['x'])
    tgraph_bes_opp = ROOT.TGraphAsymmErrors(len_bes_opp)
    for i in range(len_bes_opp):
        #tgraph_bes_opp.SetPointX(i, data_bes_opp['x'][i])
        #tgraph_bes_opp.SetPointY(i, data_bes_opp['y'][i])
        tgraph_bes_opp.SetPoint(i, data_bes_opp['x'][i], data_bes_opp['y'][i])
        tgraph_bes_opp.SetPointEXlow(i, 0.0)
        tgraph_bes_opp.SetPointEXhigh(i, 0.0)
        tgraph_bes_opp.SetPointEYlow(i, data_bes_opp['e'][i])
        tgraph_bes_opp.SetPointEYhigh(i, data_bes_opp['e'][i])
    hstyle.set_axis(tgraph_bes_opp, r'#sqrt{s} (GeV)', r'Cross Section (pb)')
    tgraph_bes_opp.GetXaxis().SetRangeUser(1.95, 3.10)
    tgraph_bes_opp.GetYaxis().SetRangeUser(0.0, 400.0)
    hstyle.set_hist_data(tgraph_bes_opp, style_code=1)
    tgraph_bes_opp.SetMarkerSize(1.2)
    legendlist.append([tgraph_bes_opp, r'Measurement', 'lp'])
    tgraph_bes_opp.Draw('AP')
if(1 == 1):
    data_fit_opp = {}
    nx = numpy.arange(xlim[0], xlim[1], steps)
    ny = numpy.arange(xlim[0], xlim[1], steps)
    len_fit_opp = int((xlim[1] - xlim[0]) / steps)
    for i in range(len_fit_opp):
        ny[i] = hfunc.bes_line_shape_omegapipi(nx[i],
                                               2.21678e+00,
                                               5.69036e-02,
                                               2.15072e+00,
                                               8.79830e-02,
                                               1.79790e+04,
                                               -5.30545e+00)
    data_fit_opp['x'] = nx
    data_fit_opp['y'] = ny
    tgraph_fit_opp = ROOT.TGraph(len_fit_opp)
    for i in range(len_fit_opp):
        tgraph_fit_opp.SetPoint(i, data_fit_opp['x'][i], data_fit_opp['y'][i])
    tgraph_fit_opp.SetLineColor(hstyle.style_color[2])
    tgraph_fit_opp.SetLineWidth(3)
    tgraph_fit_opp.SetLineStyle(1)
    legendlist.append([tgraph_fit_opp, r'Fitting', 'l'])
    tgraph_fit_opp.Draw('Lsame')
if(1 == 1):
    data_fit_opp_r = {}
    nx = numpy.arange(xlim[0], xlim[1], steps)
    ny = numpy.arange(xlim[0], xlim[1], steps)
    len_fit_opp_r = int((xlim[1] - xlim[0]) / steps)
    for i in range(len_fit_opp_r):
        ny[i] = hfunc.bes_line_shape_omegapipi_r(nx[i],
                                                 2.21678e+00,
                                                 5.69036e-02,
                                                 2.15072e+00,
                                                 8.79830e-02,
                                                 1.79790e+04,
                                                 -5.30545e+00)
    data_fit_opp_r['x'] = nx
    data_fit_opp_r['y'] = ny
    tgraph_fit_opp_r = ROOT.TGraph(len_fit_opp_r)
    for i in range(len_fit_opp_r):
        tgraph_fit_opp_r.SetPoint(i, data_fit_opp_r['x'][i], data_fit_opp_r['y'][i])
    tgraph_fit_opp_r.SetLineColor(hstyle.style_color[3])
    tgraph_fit_opp_r.SetLineWidth(3)
    tgraph_fit_opp_r.SetLineStyle(2)
    legendlist.append([tgraph_fit_opp_r, r'Resonance', 'l'])
    tgraph_fit_opp_r.Draw('Lsame')
if(1 == 1):
    data_fit_opp_n = {}
    nx = numpy.arange(xlim[0], xlim[1], steps)
    ny = numpy.arange(xlim[0], xlim[1], steps)
    len_fit_opp_n = int((xlim[1] - xlim[0]) / steps)
    for i in range(len_fit_opp_n):
        ny[i] = hfunc.bes_line_shape_omegapipi_n(nx[i],
                                                 2.21678e+00,
                                                 5.69036e-02,
                                                 2.15072e+00,
                                                 8.79830e-02,
                                                 1.79790e+04,
                                                 -5.30545e+00)
    data_fit_opp_n['x'] = nx
    data_fit_opp_n['y'] = ny
    tgraph_fit_opp_n = ROOT.TGraph(len_fit_opp_n)
    for i in range(len_fit_opp_n):
        tgraph_fit_opp_n.SetPoint(i, data_fit_opp_n['x'][i], data_fit_opp_n['y'][i])
    tgraph_fit_opp_n.SetLineColor(hstyle.style_color[4])
    tgraph_fit_opp_n.SetLineWidth(3)
    tgraph_fit_opp_n.SetLineStyle(3)
    legendlist.append([tgraph_fit_opp_n, r'Continum', 'l'])
    tgraph_fit_opp_n.Draw('Lsame')
tgraph_bes_opp.Draw('Psame')
drawlist = []
legend = hstyle.get_legend(legendlist,
                           d=0.75, l=0.65)
drawlist.append(legend)
for i in drawlist:
    i.Draw('same')
canvas.Update()
canvas.Print('opicture/%s' % (filename))
input()
