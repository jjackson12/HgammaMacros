# This script formats jet substructure plots and also some leading photon MVA id variables
# it takes one argument: the input filename
# Example: python formatSubjetVarsPlots.py myFlatTuple.root
# John Hakala 1/15/2016

from ROOT import *
from sys import argv
from os import path, makedirs

if not len(argv)>1:
	print "Please supply one argument to this macro: the name of the input root file."
	exit(1)

if not path.exists("output"):
	makedirs("output")

inFile = TFile(argv[1])

leadingJetTau1             = inFile.Get("Jet_substructure/leadingJetTau1Hist")
leadingJetTau2             = inFile.Get("Jet_substructure/leadingJetTau2Hist")
leadingJetTau3             = inFile.Get("Jet_substructure/leadingJetTau3Hist")
leadingJetT2T1             = inFile.Get("Jet_substructure/leadingJetT2T1")
leadingJetT3T2             = inFile.Get("Jet_substructure/leadingJetT3T2")
leadingJetPrunedCorrMass   = inFile.Get("Jet_substructure/leadingJetPrunedMassHist")
leadingJetSoftdropCorrMass = inFile.Get("Jet_substructure/leadingJetSoftdropMassHist")
leadingJetMass             = inFile.Get("Jet_kinematics/leadingJetMassHist")
leadingPhMVAhist_barrel    = inFile.Get("Photon_id/leadingPhMVAhist_barrel")
leadingPhMVAhist_endcap    = inFile.Get("Photon_id/leadingPhMVAhist_endcap")

canvas1 = TCanvas("canvas1", "canvas1", 800, 800)
canvas2 = TCanvas("canvas2", "canvas2", 800, 800)
canvas3 = TCanvas("canvas3", "canvas3", 800, 800)
canvas4 = TCanvas("canvas4", "canvas4", 800, 800)
canvas5 = TCanvas("canvas5", "canvas5", 800, 800)
canvas6 = TCanvas("canvas6", "canvas6", 800, 800)
canvas7 = TCanvas("canvas7", "canvas7", 800, 800)

leadingJetTau1             .GetXaxis().SetTitle("Leading AK8 jet #tau_{1}")
leadingJetTau2             .GetXaxis().SetTitle("Leading AK8 jet #tau_{2}")
leadingJetTau3             .GetXaxis().SetTitle("Leading AK8 jet #tau_{3}")
leadingJetT2T1             .GetXaxis().SetTitle("Leading AK8 jet #tau_{2}/#tau_{1}")
leadingJetT3T2             .GetXaxis().SetTitle("Leading AK8 jet #tau_{3}/#tau_{2}")
leadingJetMass             .GetXaxis().SetTitle("leading AK8 jet mass [GeV]")
leadingJetPrunedCorrMass   .GetXaxis().SetTitle("leading AK8 pruned jet mass (corrected) [GeV]")
leadingJetSoftdropCorrMass .GetXaxis().SetTitle("leading AK8 softdrop jet mass (corrected) [GeV]")
leadingPhMVAhist_barrel    .GetXaxis().SetTitle("Barrel photon ID MVA value")
leadingPhMVAhist_endcap    .GetXaxis().SetTitle("Endcap photon ID MVA value")

leadingJetTau1             .GetYaxis().SetTitle("Events")
leadingJetTau2             .GetYaxis().SetTitle("Events")
leadingJetTau3             .GetYaxis().SetTitle("Events")
leadingJetT2T1             .GetYaxis().SetTitle("Events")
leadingJetT3T2             .GetYaxis().SetTitle("Events")
leadingJetMass             .GetYaxis().SetTitle("Events")
leadingJetPrunedCorrMass   .GetYaxis().SetTitle("Events")
leadingJetSoftdropCorrMass .GetYaxis().SetTitle("Events")
leadingPhMVAhist_barrel    .GetYaxis().SetTitle("Events")
leadingPhMVAhist_endcap    .GetYaxis().SetTitle("Events")

leadingJetTau1             .GetYaxis().SetLabelSize(0.025)
leadingJetTau2             .GetYaxis().SetLabelSize(0.025)
leadingJetTau3             .GetYaxis().SetLabelSize(0.025)
leadingJetT2T1             .GetYaxis().SetLabelSize(0.025)
leadingJetT3T2             .GetYaxis().SetLabelSize(0.025)
leadingJetMass             .GetYaxis().SetLabelSize(0.03)
leadingJetPrunedCorrMass   .GetYaxis().SetLabelSize(0.03)
leadingJetSoftdropCorrMass .GetYaxis().SetLabelSize(0.03)
leadingPhMVAhist_barrel    .GetYaxis().SetLabelSize(0.02)
leadingPhMVAhist_endcap    .GetYaxis().SetLabelSize(0.02)

leadingJetTau1             .GetYaxis().SetTitleOffset(1.3)
leadingJetTau2             .GetYaxis().SetTitleOffset(1.3)
leadingJetTau3             .GetYaxis().SetTitleOffset(1.3)
leadingJetT2T1             .GetYaxis().SetTitleOffset(1.3)
leadingJetT3T2             .GetYaxis().SetTitleOffset(1.3)
leadingJetMass             .GetYaxis().SetTitleOffset(1.2)
leadingJetPrunedCorrMass   .GetYaxis().SetTitleOffset(1.2)
leadingJetSoftdropCorrMass .GetYaxis().SetTitleOffset(1.2)
leadingPhMVAhist_barrel    .GetYaxis().SetTitleOffset(1.5)
leadingPhMVAhist_endcap    .GetYaxis().SetTitleOffset(1.5)


canvas1.cd()
leadingJetTau1.Draw()

canvas2.cd()
leadingJetTau2.Draw()

canvas3.cd()
leadingJetTau3.Draw()

canvas4.cd()
leadingJetT2T1.Draw()

canvas5.cd()
leadingJetT3T2.Draw()

canvas6.SetLogy()
canvas6.cd()
leadingJetPrunedCorrMass.SetTitle("Leading (groomed) AK8 jet inv. mass")
leadingJetPrunedCorrMass.GetXaxis().SetTitle("Invariant mass (GeV)")
leadingJetPrunedCorrMass.GetXaxis().SetRangeUser(0,1000)
leadingJetPrunedCorrMass.Draw()
canvas6.Update()
prunedCorrMassStats = leadingJetPrunedCorrMass.FindObject("stats")
prunedCorrMassStats.SetTextColor(kBlue)
canvas6.Update()
leadingJetSoftdropCorrMass.SetLineColor(kRed)
leadingJetSoftdropCorrMass.Draw("SAMES")
canvas6.Update()
softDropCorrMassStats = leadingJetSoftdropCorrMass.FindObject("stats")
softDropCorrMassStats.SetX1NDC(0.778894)
softDropCorrMassStats.SetX2NDC(0.979899)
softDropCorrMassStats.SetY1NDC(0.600259)
softDropCorrMassStats.SetY2NDC(0.759379)
softDropCorrMassStats.SetTextColor(kRed)
canvas6.Update()
leadingJetMass.SetLineColor(kBlack)
leadingJetMass.Draw("SAMES")
canvas6.Update()
jetMassStats = leadingJetMass.FindObject("stats")
jetMassStats.SetX1NDC(0.561558)
jetMassStats.SetX2NDC(0.762563)
jetMassStats.SetY1NDC(0.776197)
jetMassStats.SetY2NDC(0.935317)
jetMassStats.SetTextColor(kBlack)
canvas6.Update()

canvas7.cd()
leadingPhMVAhist_barrel.SetTitle("Photon ID MVA values")
leadingPhMVAhist_barrel.GetXaxis().SetTitle("MVA value")
leadingPhMVAhist_barrel.GetYaxis().SetTitle("Events")
leadingPhMVAhist_barrel.Draw()
canvas7.Update()
barrelMVAstats = leadingPhMVAhist_barrel.FindObject("stats")
barrelMVAstats.SetX1NDC(0.775126-.655)
barrelMVAstats.SetX2NDC(0.976131-.655)
barrelMVAstats.SetY1NDC(0.600259+.18)
barrelMVAstats.SetY2NDC(0.759379+.18)
leadingPhMVAhist_endcap.Draw("SAMES")
canvas7.Update()
barrelMVAstats.SetTextColor(kBlue)
leadingPhMVAhist_endcap.SetLineColor(kRed)
endcapMVAstats = leadingPhMVAhist_endcap.FindObject("stats")
endcapMVAstats.SetX1NDC(0.775126-.655)
endcapMVAstats.SetX2NDC(0.976131-.655)
endcapMVAstats.SetY1NDC(0.600259)
endcapMVAstats.SetY2NDC(0.759379)
endcapMVAstats.SetTextColor(kRed)
canvas7.Update()

canvas1.Print(              "output/LeadingJetTau1.pdf" )
canvas2.Print(              "output/LeadingJetTau2.pdf" )
canvas3.Print(              "output/LeadingJetTau3.pdf" )
canvas4.Print(              "output/LeadingJetT2T1.pdf" )
canvas5.Print(              "output/LeadingJetT3T2.pdf" )
canvas6.Print( "output/JetMass_raw+softdrop+pruned.pdf" )
canvas7.Print(             "output/PhotonIDmvaVals.pdf" )

#if __name__ == '__main__':
#   rep = ''
#   while not rep in [ 'q', 'Q' ]:
#      rep = raw_input( 'enter "q" to quit: ' )
#      if 1 < len(rep):
#         rep = rep[0]
