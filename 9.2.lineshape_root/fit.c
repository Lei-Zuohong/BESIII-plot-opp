#pragma region 1 include
#include <iostream>
#include <fstream>
#include "TComplex.h"
#include <complex>
#include <iostream>
#include <fstream>
#include "TGraphAsymmErrors.h"
#include "TGraphErrors.h"
#include "TLegend.h"
#include "TLegendEntry.h"
#include "bes3plotstyle.c"
#include "Math/QuantFuncMathCore.h"
#include <iomanip>
#include <TTree.h>
#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>
#include <TH2F.h>
#include <TMinuit.h>
#include <TComplex.h>
#include <TLorentzVector.h>
#include <TGraph.h>
#include <cassert>
#include "Riostream.h"
#include "TMatrixD.h"
#include "TVectorD.h"
#include "TGraphErrors.h"
#include "TDecompChol.h"
#include "TDecompSVD.h"
#include "TF1.h"
using namespace std;
#include "headc/bes_const.h"
#pragma endregion
#pragma region 2 相空间函数
double phasespace_3body_momentum(double ma, double m1, double m2)
{
    double part1 = ma * ma - (m1 + m2) * (m1 + m2);
    double part2 = ma * ma - (m1 - m2) * (m1 - m2);
    double output = 0;
    if (part1 > 0)
    {
        output = sqrt(part1 * part2) / (2 * ma);
    }
    else
    {
        output = 0;
    }
    return output;
}
double phasespace_3body_intergral(double *s, double *mass)
{
    double su = s[0];
    double m0 = mass[0];
    double m1 = mass[1];
    double m2 = mass[2];
    double m3 = mass[3];
    double E12 = (m3 * m3 + su - m0 * m0) / (2 * m3);
    double part1 = phasespace_3body_momentum(E12, m1, m2);
    double part2 = phasespace_3body_momentum(m3, sqrt(su), m0);
    double output = part1 * part2 / (m3 * E12);
    return output;
}
double phasespace_3body(double ma, double mparticle1, double mparticle2, double mparticle3)
{
    TF1 *pdf = new TF1("pdf", phasespace_3body_intergral, 0, 5, 4);
    pdf->SetParameter(0, mparticle1);
    pdf->SetParameter(1, mparticle2);
    pdf->SetParameter(2, mparticle3);
    pdf->SetParameter(3, ma);
    double x1 = mparticle1 + mparticle2;
    double x2 = ma - mparticle3;
    double pi = bes_const::pi;
    double output = pdf->Integral(x1, x2) / pi / pi / pi / 2.5;
    return output;
}
#pragma endregion
#pragma region 3 输入数据
const int Ndata = 19;
double xv[Ndata] = {2.0000,
                    2.0500,
                    2.1000,
                    2.1250,
                    2.1500,
                    2.1750,
                    2.2000,
                    2.2324,
                    2.3094,
                    2.3864,
                    2.3960,
                    2.6444,
                    2.6464,
                    2.9000,
                    2.9500,
                    2.9810,
                    3.0000,
                    3.0200,
                    3.0800};
double xe[Ndata] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
double yv[Ndata] = {255.103, 233.178, 195.393, 186.446, 181.036, 194.425, 203.001, 156.656, 84.446, 66.317, 60.351, 38.642, 35.689, 15.033, 11.569, 16.490, 9.334, 9.260, 7.065};
double ye[Ndata] = {24.5357, 31.9073, 19.6494, 13.4791, 30.2228, 19.3193, 18.8616, 15.6844, 8.9676, 7.1048, 5.1165, 3.9946, 3.7586, 1.4019, 2.5154, 2.8218, 2.2228, 1.9142, 0.8061};
double edge_left = 1.9;
double edge_right = 3.2;
double intergral = 0.00001;
const int Nphase = int((edge_right - edge_left) / intergral);
double *phasespace = new double[Nphase];
#pragma endregion
#pragma region 4 拟合函数
double Get_phasespace(double x)
{
    int dx = int((x - edge_left) / intergral);
    double output = phasespace[dx];
    return output;
}
double Func_etapipi(double *var, double *par)
{
    double x = var[0];
    double mr = par[0];
    double wr = par[1];
    double phi = par[2];
    double brc = par[3];
    double c = par[4];
    double b = par[5];
    complex<double> img(0.0, 1.0);
    complex<double> real(1.0, 0.0);
    complex<double> phase(cos(phi), sin(phi));

    double phspx = Get_phasespace(x);
    double phspm = Get_phasespace(mr);

    double part1 = sqrt(12 * 3.1415926 * wr * brc);
    complex<double> part2 = x * x - mr * mr + img * mr * wr;
    complex<double> partr = (mr / x) * (part1 / part2) * phase * sqrt(phspx / phspm);
    double partn = c * pow(x, b) * sqrt(phspx);
    double value = pow(abs(partr + partn), 2.0);
    return value;
}
double Func_etapipi_continue(double *var, double *par)
{
    double x = var[0];
    double mr = par[0];
    double wr = par[1];
    double phi = par[2];
    double brc = par[3];
    double c = par[4];
    double b = par[5];
    complex<double> img(0.0, 1.0);
    complex<double> real(1.0, 0.0);
    complex<double> phase(cos(phi), sin(phi));

    double phspx = Get_phasespace(x);
    double phspm = Get_phasespace(mr);

    double part1 = sqrt(12 * 3.1415926 * wr * brc);
    complex<double> part2 = x * x - mr * mr + img * mr * wr;
    complex<double> partr = (mr / x) * (part1 / part2) * phase * sqrt(phspx / phspm);
    double partn = c * pow(x, b) * sqrt(phspx);
    double value = pow(partn, 2.0);
    return value;
}
double Func_etapipi_resonance(double *var, double *par)
{
    double x = var[0];
    double mr = par[0];
    double wr = par[1];
    double phi = par[2];
    double brc = par[3];
    double c = par[4];
    double b = par[5];
    complex<double> img(0.0, 1.0);
    complex<double> real(1.0, 0.0);
    complex<double> phase(cos(phi), sin(phi));

    double phspx = Get_phasespace(x);
    double phspm = Get_phasespace(mr);

    double part1 = sqrt(12 * 3.1415926 * wr * brc);
    complex<double> part2 = x * x - mr * mr + img * mr * wr;
    complex<double> partr = (mr / x) * (part1 / part2) * phase * sqrt(phspx / phspm);
    double partn = c * pow(x, b) * sqrt(phspx);
    double value = pow(abs(partr), 2.0);
    return 4 * value;
}
double func_etapipi(double x, double *par)
{
    double mr = par[0];
    double wr = par[1];
    double phi = par[2];
    double brc = par[3];
    double c = par[4];
    double b = par[5];
    complex<double> img(0.0, 1.0);
    complex<double> real(1.0, 0.0);
    complex<double> phase(cos(phi), sin(phi));

    double phspx = Get_phasespace(x);
    double phspm = Get_phasespace(mr);

    double part1 = sqrt(12 * 3.1415926 * wr * brc);
    complex<double> part2 = x * x - mr * mr + img * mr * wr;
    complex<double> partr = (mr / x) * (part1 / part2) * phase * sqrt(phspx / phspm);
    double partn = c * pow(x, b) * sqrt(phspx);
    double value = pow(abs(partr + partn), 2.0);
    return value;
}
void fcn(Int_t &npar, Double_t *gin, Double_t &f, Double_t *par, Int_t iflag)
{
    Double_t chisq = 0;
    Double_t delta;
    for (Int_t i = 0; i < Ndata; i++)
    {
        delta = (yv[i] - func_etapipi(xv[i], par)) / ye[i];
        chisq += delta * delta;
    }
    f = chisq;
}
#pragma endregion

int fit()
{
#pragma region 5.1 设定选项
    int option_fit_migrad = 1;
    int option_fit_hesse = 1;
    int option_fit_minos = 1;
    int option_fit_mnprin = 1;
    int option_draw_origin = 1;
    int option_draw_test_function = 0;
    int option_draw_best_function = 1;
    int option_draw_continue_function = 1;
    int option_draw_resonance_function = 1;
#pragma endregion
#pragma region 5.2 计算相空间
    cout << "1. Start calculating phase space" << endl;
    for (int i = 0; i < Nphase; i++)
    {
        phasespace[i] = phasespace_3body(edge_left + intergral * i,
                                         bes_const::particle_piz.mass,
                                         bes_const::particle_omega782.mass,
                                         bes_const::particle_piz.mass);
    }
#pragma endregion
#pragma region 5.3 拟合
    const int npar = 6;
    TMinuit *my_fit = new TMinuit(npar + 1);
    my_fit->SetFCN(fcn);
    // 初始化需要的参数
    double fit_index[10];
    Int_t fit_error = 0;
    fit_index[0] = 1;
    // 1. SET ERR
    my_fit->mnexcm("SET ERR", fit_index, 1, fit_error);
    // 设定初始值、边界、步长
    my_fit->mnparm(0, "mr     ", 2.22130e+00, 0.001, 2.0, 2.4, fit_error);
    my_fit->mnparm(1, "wr     ", 5.04612e-02, 0.0001, 0.005, 0.5, fit_error);
    my_fit->mnparm(2, "phi    ", 2.32921e+00, 0.0001, 2, 2.5, fit_error);
    my_fit->mnparm(3, "brc    ", 8.61643e-02, 0.0001, 0.01, 1, fit_error);
    my_fit->mnparm(4, "c      ", 1.90508e+04, 0.01, 0.0, 100000.0, fit_error);
    my_fit->mnparm(5, "b      ", -5.36684e+00, 0.001, -100.0, 0.0, fit_error);
    fit_index[0] = 1000;
    fit_index[1] = 0.001;
    if (option_fit_migrad == 1):my_fit->mnexcm("MIGRAD", fit_index, 2, fit_error);
    if (option_fit_hesse == 1):my_fit->mnexcm("HESSE", fit_index, 2, fit_error);
    if (option_fit_minos == 1):my_fit->mnexcm("MINOS", fit_index, 2, fit_error);
    if (option_fit_mnprin == 1)
    {
        double amin, edm, errdef;
        Int_t nvpar, nparx, icstat;
        my_fit->mnstat(amin, edm, errdef, nvpar, nparx, icstat);
        my_fit->mnprin(0, amin);
    }
    double bestPar[npar];
    double bestErr[npar];
    for (int i = 0; i < npar; i++)
    {
        my_fit->GetParameter(i, bestPar[i], bestErr[i]);
    }
#pragma endregion
#pragma region 3.2.plot
    gStyle->SetPalette(1);
    gStyle->SetCanvasBorderMode(0);
    gStyle->SetCanvasBorderSize(0);
    gStyle->SetCanvasColor(10);
    gStyle->SetLabelFont(42, "xyz");
    gStyle->SetLabelSize(0.07, "xyz");
    gStyle->SetLabelOffset(0.01, "xyz");
    gStyle->SetNdivisions(510, "xyz");
    gStyle->SetTitleFont(42, "xyz");
    gStyle->SetTitleColor(1, "xyz");
    gStyle->SetTitleSize(0.08, "xyz");
    gStyle->SetTitleOffset(1.15, "xyz");
    gStyle->SetPadBorderMode(0);
    gStyle->SetPadBorderSize(0);
    gStyle->SetPadColor(10);
    gStyle->SetPadLeftMargin(0.2);
    gStyle->SetPadBottomMargin(0.2);
    gStyle->SetPadRightMargin(0.15);
    gStyle->SetPadTopMargin(0.05);
    gStyle->SetPadRightMargin(0.05);
    gStyle->SetPadTopMargin(0.05);
    gStyle->SetLegendBorderSize(0);
    gStyle->SetOptDate(0);
    gStyle->SetOptStat(0);
    gStyle->SetOptFit(0);
    gStyle->SetOptTitle(0);
    gStyle->SetOptTitle(kFALSE);
#pragma endregion
#pragma region 3.3.draw
    TCanvas *c1 = new TCanvas("c1", "c1", 800, 600);
    if (option_draw_origin == 1)
    {
        TGraph *Ddata = new TGraphAsymmErrors(Ndata, xv, yv, xe, xe, ye, ye);
        TLegend *legend = new TLegend(0.65, 0.7, 0.94, 0.94);
        FormatData(Ddata, 1, 20);
        NameAxes(Ddata, "#sqrt{s} (GeV)", "#sigma(e^{+}e^{-} #rightarrow #omega #pi^{0}#pi^{0}) (pb)");
        Ddata->SetMarkerStyle(21);
        Ddata->SetMarkerSize(1.3);
        Ddata->SetMarkerColor(2);
        Ddata->SetLineColor(2);
        Ddata->SetLineWidth(2);
        Ddata->Draw("AP");
        legend->AddEntry(Ddata, "R-scan data", "PEL")->SetTextColor(2);
    }
    double func_test_start[6] = {2.22089e+00,
                                 5.08490e-02,
                                 2.29351e+00,
                                 8.54312e-02,
                                 1.92712e+04,
                                 -5.38510e+00};
    if (option_draw_test_function == 1)
    {
        TF1 *func_test = new TF1("func_test", Func_etapipi, 1.9, 3.2, 6);
        func_test->SetParameters(func_test_start);
        func_test->SetLineColor(4);
        func_test->SetLineStyle(9);
        func_test->SetLineWidth(3);
        func_test->Draw("same");
    }
    if (option_draw_best_function == 1)
    {
        TF1 *func_best = new TF1("func_best", Func_etapipi, 1.9, 3.2, 6);
        double func_best_start[6] = {bestPar[0], bestPar[1], bestPar[2], bestPar[3], bestPar[4], bestPar[5]};
        //func_best->SetParameters(func_best_start);
        func_best->SetParameters(func_test_start);
        func_best->SetLineColor(4);
        func_best->SetLineStyle(9);
        func_best->SetLineWidth(3);
        func_best->Draw("same");
        legend->AddEntry(func_best, "Fitting", "L")->SetTextColor(4);
    }
    if (option_draw_continue_function == 1)
    {
        TF1 *func_conti = new TF1("func_conti", Func_etapipi_continue, 1.9, 3.2, 6);
        double func_conti_start[6] = {bestPar[0], bestPar[1], bestPar[2], bestPar[3], bestPar[4], bestPar[5]};
        //func_conti->SetParameters(func_conti_start);
        func_conti->SetParameters(func_test_start);
        func_conti->SetLineColor(8);
        func_conti->SetLineStyle(2);
        func_conti->SetLineWidth(3);
        func_conti->Draw("same");
        legend->AddEntry(func_conti, "Continous", "L")->SetTextColor(8);
    }
    if (option_draw_resonance_function == 1)
    {
        TF1 *func_reson = new TF1("func_reson", Func_etapipi_resonance, 1.9, 3.2, 6);
        double func_reson_start[6] = {bestPar[0], bestPar[1], bestPar[2], bestPar[3], bestPar[4], bestPar[5]};
        //func_reson->SetParameters(func_reson_start);
        func_reson->SetParameters(func_test_start);
        func_reson->SetLineColor(9);
        func_reson->SetLineStyle(2);
        func_reson->SetLineWidth(3);
        func_reson->Draw("same");
        legend->AddEntry(func_reson, "Resonance", "L")->SetTextColor(9);
    }
    legend->Draw();
    c1->Update();
    c1->Print("fit.pdf");
    c1->Print("fit.jpg");
#pragma endregion
#pragma region 3.4.print
    double best_chisq = 0;
    for (Int_t i = 0; i < Ndata; i++)
    {
        double delta = (yv[i] - func_etapipi(xv[i], bestPar)) / ye[i];
        best_chisq += delta * delta;
    }
    cout << "result_best_chisq: " << best_chisq << endl;
#pragma endregion
    return 0;
}
