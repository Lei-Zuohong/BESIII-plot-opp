# -*- coding: UTF-8 -*-
# Public pack
import os
# Private pack
import ROOT
import headpy.hbes.hopp as hopp
import headpy.hbes.hfit as hfit
import headpy.hbes.hnew as hnew
import headpy.hscreen.hprint as hprint
import headpy.hfile.hpickle as hpickle

# 初始化数据
massages = hnew.massage_read()
trees_f = hnew.trees_read(energy=2.1250,
                          tree='fit4c',
                          read=['real', 'omeganpw'])
trees_t = hnew.trees_read(energy=2.1250,
                          tree='topotree',
                          read=['selected_qqback'])
selecters = hopp.selecters()
selecters['omega_m'].set_width(0.15)
selecters['itopo'] = hnew.SELECTER_value(values=[2, 4, 11, 28, 52],
                                         reverse=1)
# 写入读取数据
alldata_f = hnew.ALLDATA(trees=trees_f,
                         selecters=selecters,
                         massages=massages)
alldata_t = hnew.ALLDATA(trees=trees_t,
                         selecters=selecters,
                         massages=massages)
tfile = {}
thist = {}
alldata_f.get_weight(data='omeganpw',
                     energy=2.1250,
                     name_weight='omegapi02_m_pi02pi03_m',
                     name_branch='new_weight',
                     dimension=2)
tfile['r'], thist['r'] = alldata_f.tree(data='real',
                                        branch='omega_m',
                                        docuts=['chisq', 'pi01_m', 'pi02_m', 'pi03_m', 'omega_m'],
                                        name='use_r')
tfile['m'], thist['m'] = alldata_f.hist(data='omeganpw',
                                        branchs=['omega_m'],
                                        docuts=['chisq', 'pi01_m', 'pi02_m', 'pi03_m', 'omega_m'],
                                        doweight=['new_weight'],
                                        name='use_m')
tfile['bh'], thist['bh'] = alldata_t.hist(data='selected_qqback',
                                          branchs=['omega_m'],
                                          docuts=['chisq', 'pi01_m', 'pi02_m', 'pi03_m', 'omega_m', 'itopo'],
                                          name='use_bh')
tfile['bt'], thist['bt'] = alldata_t.tree(data='selected_qqback',
                                          branch='omega_m',
                                          docuts=['chisq', 'pi01_m', 'pi02_m', 'pi03_m', 'omega_m', 'itopo'],
                                          name='use_bt')
file = {}
hist = {}
for i in tfile:
    file[i] = ROOT.TFile(tfile[i])
    hist[i] = file[i].Get(thist[i])
# 开始拟合
mass = ROOT.RooRealVar('omega_m', 'omega_m',
                       selecters['omega_m'].center - selecters['omega_m'].width,
                       selecters['omega_m'].center + selecters['omega_m'].width)
option_list = {}
option_list['gmean'] = [2.42373e-03, -0.01, 0.01]
option_list['gsigm'] = [1.02158e-03, 0, 0.005]
option_list['npdf1'] = [2.16245e+03, 0, 3000]
option_list['npdf2'] = [1.84855e+03, 0, 3000]
option_list['npdf3'] = [1.84855e+03, 0, 3000]
option_list['p0'] = [-2.43231e+01, -1000, 1000]
option_list['p1'] = [3.77516e+01, -1000, 1000]
parameter = {}
for i in option_list:
    parameter[i] = ROOT.RooRealVar(i, i,
                                   option_list[i][0],
                                   option_list[i][1],
                                   option_list[i][2])
# PDF_signal
histm = ROOT.RooDataHist('histm', 'histm',
                         ROOT.RooArgList(mass),
                         hist['m'])
mcpdf = ROOT.RooHistPdf('signpdf', 'signpdf',
                        ROOT.RooArgSet(mass),
                        histm,
                        1)
gauss = ROOT.RooGaussian('gauss', 'gauss',
                         mass,
                         parameter['gmean'],
                         parameter['gsigm'])
signpdf = ROOT.RooFFTConvPdf('signpdf', 'signpdf',
                             mass,
                             mcpdf,
                             gauss)
# PDF_back_function
backpdf_f = ROOT.RooPolynomial('backpdf_f', 'backpdf_f',
                               mass,
                               ROOT.RooArgList(parameter['p0'],
                                               parameter['p1']))
# PDF_back_hist
histb = ROOT.RooDataHist('histb', 'histb',
                         ROOT.RooArgList(mass),
                         hist['bh'])
backpdf_h = ROOT.RooHistPdf('backpdf_h', 'backpdf_h',
                            ROOT.RooArgSet(mass),
                            histb,
                            1)
# PDF_back_tree
backpdf_t = ROOT.RooDataSet('backpdf_t', 'backpdf_t',
                            hist['bt'],
                            ROOT.RooArgSet(ROOT.RooArgList(mass)))
# PDF_real
realpdf = ROOT.RooDataSet('datar', 'datar',
                          hist['r'],
                          ROOT.RooArgSet(ROOT.RooArgList(mass)))
# PDF_backf+signal
allpdf = ROOT.RooAddPdf('allpdf', 'allpdf',
                        ROOT.RooArgList(signpdf, backpdf_f),
                        ROOT.RooArgList(parameter['npdf1'],
                                        parameter['npdf2']))
backpdf_u = ROOT.RooAddPdf('backpdf_u', 'backpdf_u',
                           ROOT.RooArgList(backpdf_f),
                           ROOT.RooArgList(parameter['npdf3']))
# 开始 simutaneous 拟合
sample = ROOT.RooCategory("sample", "sample")
sample.defineType("signal")
sample.defineType("background")
simdata = ROOT.RooDataSet("simdata", "simdata", ROOT.RooArgSet(ROOT.RooArgList(mass)),
                          ROOT.RooFit.Index(sample),
                          ROOT.RooFit.Import("signal", realpdf),
                          ROOT.RooFit.Import("background", backpdf_t))
simpdf = ROOT.RooSimultaneous("simpdf", "simpdf", sample)
simpdf.addPdf(allpdf, 'signal')
simpdf.addPdf(backpdf_u, 'background')
simpdf.fitTo(simdata)

output = {}
output['nevent'] = parameter['npdf1'].getVal()
output['enevent'] = parameter['npdf1'].getError()
massframe = mass.frame()
realpdf.plotOn(massframe)
allpdf.plotOn(massframe)
allpdf.plotOn(massframe, ROOT.RooFit.Components('backpdf_f'),
              ROOT.RooFit.LineStyle(ROOT.kDashed),
              ROOT.RooFit.LineColor(ROOT.kRed))
backpdf_t.plotOn(massframe,
                 ROOT.RooFit.MarkerStyle(ROOT.kOpenSquare))
backpdf_u.plotOn(massframe, ROOT.RooFit.Components('backpdf_f'),
                 ROOT.RooFit.LineStyle(ROOT.kDashed),
                 ROOT.RooFit.LineColor(ROOT.kGreen))
cvs = ROOT.TCanvas('canvas', '', 1200, 900)
cvs.SetFillColor(10)
cvs.SetFrameLineWidth(2)
cvs.SetTickx()
cvs.SetTicky()
massframe.SetTitle('')
picture_xtitle, picture_ytitle = selecters['omega_m'].get_title()
massframe.GetXaxis().SetTitle(picture_xtitle)
massframe.GetXaxis().SetTitleSize(0.05)
massframe.GetXaxis().SetTitleOffset(0.9)
massframe.GetXaxis().CenterTitle()
massframe.GetXaxis().SetNdivisions(505)
massframe.GetYaxis().SetTitle(picture_ytitle)
massframe.GetYaxis().SetTitleSize(0.05)
massframe.GetYaxis().SetTitleOffset(0.9)
massframe.GetYaxis().CenterTitle()
massframe.Draw()
pt = ROOT.TPaveText(0.60, 0.60, 0.85, 0.85, 'BRNDC')
pt.SetBorderSize(0)
pt.SetTextAlign(12)
pt.SetTextColor(1)
pt.SetTextSize(0.05)
pt.AddText('Energy: %1.4f GeV' % (2.125))
pt.AddText('Sig: ' + str(round(parameter['npdf1'].getVal(), 1)) +
           '#pm' + str(round(parameter['npdf1'].getError(), 1)))
pt.AddText('Bkg:  ' + str(round(parameter['npdf2'].getVal(), 1)) +
           '#pm' + str(round(parameter['npdf2'].getError(), 1)))
pt.Draw()
pictures = ['6.python_fit/9.2.simutaneous.pdf',
            '6.python_fit/9.2.simutaneous.jpg']
for i in pictures:
    cvs.Print(i)
input()
