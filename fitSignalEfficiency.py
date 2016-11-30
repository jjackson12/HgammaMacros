from ROOT import *
tfile = TFile("efficienciesGraphs_masswindow_110-140.root")
graphBtag = tfile.Get("SigEff_btag")
can1 = TCanvas()
can1.cd()
graphBtag.Draw("AP")

fitFunctionBtag = TF1("fitFunctionBtag", "[0]+[1]*TMath::ATan((x-[2])^2/[3])*TMath::Exp(-x/[4])", 600, 4000)
fitFunctionBtag.SetParameters(0, .06, 500, 100000, 2500)
#fitFunctionBtag = TF1("fitFunctionBtag", "pol5", 600, 4000)

#fitFunctionBtag = TF1("fitFunctionBtag", "[0]*TMath::Landau([1]*x*x+[2]*x+[3], [4], [5])+[6]", 650, 4000)
#fitFunctionBtag.SetParameters(0.54, 0, 1.2, 566, 1930, 392, -.04)
#fitFunctionBtag = TF1("fitFunctionBtag", "pol6", 60, 4000)
#fitFunctionBtag.SetParameters(0, 0, 0, 0, 0, 0)
graphBtag.Fit(fitFunctionBtag)

graphAntiBtag = tfile.Get("SigEff_antibtag")
can2 = TCanvas()
can2.cd()
graphAntiBtag.Draw("AP")

#fitFunctionAntiBtag = TF1("fitFunctionAntiBtag", "[0]*TMath::TanH(TMath::Power(x-[1],[2])/[3])*TMath::Power((x/[4]),[5])", 649.992, 1000)
#fitFunctionAntiBtag = TF1("fitFunctionAntiBtag", "[0]*TMath::TanH((x-[1])/[2])*TMath::Power(x,[3])+[4]", 650, 1000)
#fitFunctionAntiBtag = TF1("fitFunctionAntiBtag", "[0]*TMath::ATan((x-[1])/[2])*TMath::Power(x,[3])+[4]", 650, 1000)
#fitFunctionAntiBtag.SetParameters(0.1, 700, 200, 0.2, .01)
fitFunctionAntiBtag = TF1("fitFunctionAntiBtag", "[0]*TMath::ATan((x-[1])/[2])+[3]", 650, 4000)
fitFunctionAntiBtag.SetParameters(0.1, 700, 200,  .01)
graphAntiBtag.Fit(fitFunctionAntiBtag)
print 
