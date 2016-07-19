from ROOT import *
tfile = TFile("efficienciesGraphs.root")
graph = tfile.Get("SigEff_btag")
graph.Draw("AP")

fitFunction = TF1("fitFunction", "([0]-1/((x-500)/[1]))*e^(-(x-500)/[2])", 650, 4000)
fitFunction.SetParameters(1, 100, 5000)
graph.Fit(fitFunction)
