# -*- coding: UTF-8 -*-
# Public package
import numpy
# Private package
import ROOT
import default as default
import headpy.hbes.hstyle as hstyle


# 设定参数
filename = '8_SHOW_SECTION.pdf'
xlim = (1.9, 3.1)
ylim = (0, 400)
opm_ratio = 2
# 读取数据
data_bes_opp = default.data_bes_opp_sys()
data_bes_opm = default.data_bes_opm()
data_babar_opp = default.data_babar_opp(xlim[0], xlim[1])
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
    legendlist.append([tgraph_bes_opp, r'BESIII', 'lp'])
    tgraph_bes_opp.Draw('AP')
if(1 == 1):
    len_bes_opm = len(data_bes_opm['x'])
    tgraph_bes_opm = ROOT.TGraphAsymmErrors(len_bes_opm)
    for i in range(len_bes_opm):
        #tgraph_bes_opm.SetPointX(i, data_bes_opm['x'][i])
        #tgraph_bes_opm.SetPointY(i, data_bes_opm['y'][i])
        tgraph_bes_opm.SetPoint(i, data_bes_opm['x'][i], data_bes_opm['y'][i] / opm_ratio)
        tgraph_bes_opm.SetPointEXlow(i, 0.0)
        tgraph_bes_opm.SetPointEXhigh(i, 0.0)
        tgraph_bes_opm.SetPointEYlow(i, data_bes_opm['e'][i] / opm_ratio)
        tgraph_bes_opm.SetPointEYhigh(i, data_bes_opm['e'][i] / opm_ratio)
    hstyle.set_hist_data(tgraph_bes_opm, style_code=3)
    tgraph_bes_opm.SetMarkerSize(2)
    legendlist.append([tgraph_bes_opm, r'BESIII(#sigma(#omega#pi^{+}#pi^{-})/2)', 'lp'])
    tgraph_bes_opm.Draw('Psame')
if(1 == 1):
    len_babar_opp = len(data_babar_opp['x'])
    tgraph_babar_opp = ROOT.TGraphAsymmErrors(len_babar_opp)
    for i in range(len_babar_opp):
        #tgraph_babar_opp.SetPointX(i, data_babar_opp['x'][i])
        #tgraph_babar_opp.SetPointY(i, data_babar_opp['y'][i])
        tgraph_babar_opp.SetPoint(i, data_babar_opp['x'][i], data_babar_opp['y'][i])
        tgraph_babar_opp.SetPointEXlow(i, 0.0)
        tgraph_babar_opp.SetPointEXhigh(i, 0.0)
        tgraph_babar_opp.SetPointEYlow(i, data_babar_opp['e'][i])
        tgraph_babar_opp.SetPointEYhigh(i, data_babar_opp['e'][i])
    hstyle.set_hist_data(tgraph_babar_opp, style_code=2)
    tgraph_babar_opp.SetMarkerSize(2)
    legendlist.append([tgraph_babar_opp, 'BABAR', 'lp'])
    tgraph_babar_opp.Draw('Psame')
tgraph_bes_opp.Draw('Psame')
drawlist = []
legend = hstyle.get_legend(legendlist,
                           d=0.75, l=0.65)
drawlist.append(legend)
for i in drawlist:
    i.Draw('same')
canvas.Update()
canvas.Print('opicture/%s'%(filename))
input()
