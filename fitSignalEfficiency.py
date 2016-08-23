from ROOT import *
tfile = TFile("efficienciesGraphs_masswindow_110-140.root")
graphBtag = tfile.Get("SigEff_btag")
can1 = TCanvas()
can1.cd()
graphBtag.Draw("AP")

fitFunctionBtag = TF1("fitFunctionBtag", "([0]-1/((x-500)/[1]))*e^(-(x-500)/[2])", 650, 4000)
fitFunctionBtag.SetParameters(1, 100, 5000)
graphBtag.Fit(fitFunctionBtag)

graphAntiBtag = tfile.Get("SigEff_antibtag")
can2 = TCanvas()
can2.cd()
graphAntiBtag.Draw("AP")

fitFunctionAntiBtag = TF1("fitFunctionAntiBtag", "[0]*TMath::ATan((x-[1])/[2])", 650, 4000)
fitFunctionAntiBtag.SetParameters(0.2, 500, 500)
graphAntiBtag.Fit(fitFunctionAntiBtag)
