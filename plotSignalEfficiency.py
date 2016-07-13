from ROOT import TFile, TGraph, TCanvas
from HgParameters import getNormalizations
from checkSignalEfficiency import getSignalEfficiencies

massWindowToCheck = [110, 140]
signalEfficiencies = getSignalEfficiencies(massWindowToCheck)
"plotting signal efficiencies for masswindow (%f, %f)" % (massWindowToCheck[0], massWindowToCheck[1])
outfile = TFile("efficienciesGraphs.root", "RECREATE")
outfile.cd()

canvases = []
graphs   = []


for category in ['btag', 'antibtag', 'nobtag']:
  canvases.append(TCanvas())
  graphs.append(TGraph())
  graphs[-1].SetNameTitle("SigEff_%s" % category, "Signal efficiency, %s category" % category)
  for mass in getNormalizations().keys():
    graphs[-1].SetPoint(graphs[-1].GetN(), float(mass), signalEfficiencies[mass][category])
  graphs[-1].GetXaxis().SetTitle("Signal mass (GeV)")
  graphs[-1].GetYaxis().SetTitle("#varepsilon")
  graphs[-1].SetMarkerStyle(2)
  graphs[-1].Write() 
outfile.Close()


