from ROOT import *
import copy
masses = [4000, 3500, 3000, 2500, 2000, 1750, 1500, 1250, 1000, 750, 650]
for mass in masses:

  histFile = TFile("~/WZgammaMacros/newerDDs/newerDD_Hgamma_m%i.root" % mass)
  #print "opening file %s" % histFile.GetName()
  newHist = TH1F("hist_m%i"%mass, "hist_m%i"%mass, 100, 0, 250)
  tree = histFile.Get("higgs")
  tree.Draw("higgsPrunedJetCorrMass>> hist_m%i"%mass, "higgsJet_HbbTag>0.9")
  outfile = TFile("hist_m%i.root" % mass, "RECREATE")
  newHist.Write()
  outfile.Close()

mycan = TCanvas("mycan","mycan")
mycan.cd()
i=0
offset=0
files = []
hists = []
color=kRed
for mass in masses:
  files.append( TFile("hist_m%i.root"%mass))
  hists.append(files[-1].Get("hist_m%i"%mass))
  print hists[-1]
  if i==4:
    color=kGreen
    offset=0
  elif i==8:
    color=kBlue
    offset=0
  hists[-1].SetLineColor(color+offset)
  if i==0:
    mycan.cd()
    hists[-1].Draw()
  else:
    mycan.cd()
    hists[-1].Draw("SAME")
  i+=1
  offset+=1

