from ROOT import *

for category in ["btag", "antibtag"]:

  inFiles = {}
  inFiles["weighted"] = TFile("vgHists_fixTurnOn_btag-nom/%s/histos_data2016SinglePhoton.root" % category)
  inFiles["unweighted"] = TFile("vgHists_fixTurnOn_btag-test/%s/histos_data2016SinglePhoton.root" % category)
  
  hists = {}
  for inFile in inFiles:
    hists[inFile] = inFiles[inFile].Get("distribs_X")
    hists[inFile].Rebin(50)
  
  diff = hists["weighted"].Clone()
  diff.Add(hists["unweighted"], -1)
  diff.Divide(hists["weighted"])
  
  can = TCanvas()
  can.cd()
  gStyle.SetOptStat(0)
  diff.SetTitle("Effects of weight factors, %s category" % category)
  diff.GetXaxis().SetTitle("m_{j#gamma} (GeV)")
  diff.GetXaxis().SetRangeUser(600, 3000)
  diff.GetYaxis().SetTitle("Fractional difference / 50 GeV")
  diff.GetYaxis().SetLabelSize(0.028)
  diff.GetYaxis().SetTitleOffset(1.3)
  diff.Draw("hist")
  can.Print("weightFactor_effect_new-%s.pdf" % category)
