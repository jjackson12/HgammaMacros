# Script to format a the basic kinematic variables plots
# This script requires one argument: the input filename Example:
# python formatPreSelectionPlots.py myFlatTuple.root -b
# John Hakala 1/15/2016

from ROOT import *
from sys import argv

if not len(argv)>1:
	print "Please supply one argument to this macro: the name of the input root file."
	exit(1)

inFile = TFile(argv[1])

leadingPhHist  = inFile.Get("Photon_kinematics/leadingPhPtHist")
leadingJetHist = inFile.Get("Jet_kinematics/leadingJetPtHist")
HThist         = inFile.Get("Jet_kinematics/HThist")
HT_ak4hist     = inFile.Get("Jet_kinematics/HT_ak4hist")
jetEtaHist     = inFile.Get("Jet_kinematics/leadingJetEtaHist")
jetPhiHist     = inFile.Get("Jet_kinematics/leadingJetPhiHist")
phoEtaHist     = inFile.Get("Photon_kinematics/leadingPhEtaHist")
phoPhiHist     = inFile.Get("Photon_kinematics/leadingPhPhiHist")


canvas1 = TCanvas("canvas1", "canvas1", 800, 800)
canvas2 = TCanvas("canvas2", "canvas2", 800, 800)
canvas3 = TCanvas("canvas3", "canvas3", 800, 800)
canvas4 = TCanvas("canvas4", "canvas4", 800, 800)
canvas5 = TCanvas("canvas5", "canvas5", 800, 800)
canvas6 = TCanvas("canvas6", "canvas6", 800, 800)
canvas7 = TCanvas("canvas7", "canvas7", 800, 800)
canvas8 = TCanvas("canvas8", "canvas8", 800, 800)

canvas1.SetLogy()
canvas2.SetLogy()
canvas3.SetLogy()
canvas4.SetLogy()

leadingPhHist  .GetXaxis().SetTitle("Leading photon p_{T} [GeV]")
leadingPhHist  .GetYaxis().SetTitle("Events")

leadingJetHist .GetXaxis().SetTitle("Leading jet p_{T} [GeV]")
leadingJetHist .GetYaxis().SetTitle("Events")

HThist         .SetTitle("Scalar sum of jet p_{T}")
HThist         .GetXaxis().SetTitle("H_{T} [GeV]")
HThist         .GetYaxis().SetTitle("Events")


HT_ak4hist         .SetTitle("Scalar sum of AK4 jet p_{T}")
HT_ak4hist         .GetXaxis().SetTitle("H_{T} [GeV]")
HT_ak4hist         .GetYaxis().SetTitle("Events")

canvas1.cd()
leadingPhHist  .Draw()
canvas2.cd()
leadingJetHist .Draw()
canvas3.cd()
HThist         .Draw()
canvas4.cd()
HT_ak4hist         .Draw()
canvas5.cd()
jetEtaHist.Draw()
canvas6.cd()
jetPhiHist.Draw()
canvas7.cd()
phoEtaHist.Draw()
canvas8.cd()
phoPhiHist.Draw()


canvas1.Print("output/leadingPhPt.pdf")
canvas2.Print("output/leadingJetPt.pdf")
canvas3.Print("output/HT.pdf")
canvas4.Print("output/HT_ak4.pdf")
canvas5.Print("output/leadingJetEta.pdf")
canvas6.Print("output/leadingJetPhi.pdf")
canvas7.Print("output/leadingPhEta.pdf")
canvas8.Print("output/leadingPhPhi.pdf")
