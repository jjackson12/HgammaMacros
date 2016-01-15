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

canvas1 = TCanvas("canvas1", "canvas1", 800, 800)
canvas2 = TCanvas("canvas2", "canvas2", 800, 800)
canvas3 = TCanvas("canvas3", "canvas3", 800, 800)

canvas1.SetLogy()
canvas2.SetLogy()
canvas3.SetLogy()

leadingPhHist  .GetXaxis().SetTitle("Leading photon P_{T} [GeV]")
leadingJetHist .GetXaxis().SetTitle("Leading jet P_{T} [GeV]")
HThist         .GetXaxis().SetTitle("HT [GeV]")
leadingPhHist  .GetYaxis().SetTitle("Events")
leadingJetHist .GetYaxis().SetTitle("Events")
HThist         .GetYaxis().SetTitle("Events")

canvas1.cd()
leadingPhHist  .Draw()
canvas2.cd()
leadingJetHist .Draw()
canvas3.cd()
HThist         .Draw()

canvas1.Print("output/leadingPhPt.pdf")
canvas2.Print("output/leadingJetPt.pdf")
canvas3.Print("output/HT.pdf")
