# Script to format a the photon id MVA value vs. energy profiles
# This script requires one argument: the input filename Example:
# python formatMVAvsEprofiles.py myFlatTuple.root
# John Hakala 1/15/2016

from ROOT import *
from sys import argv
from os import path, makedirs

if not len(argv)>1:
	print "Please supply one argument to this macro: the name of the input root file."
	exit(1)

if not path.exists("output"):
	makedirs("output")

etaRanges = [0, 0.75, 1.479, 2.4, 3.0]  # This comes from treeChecker.C, which considers four regions: the inner and outer halves of both EE and EB

histFile = TFile(argv[1], "r")
profiles = []
canvases = []
for i in range(0,4):
	canvases.append(TCanvas("canvas%i"%i, "MVA values for photons in range %f#leq|#eta|<%f"%(etaRanges[i], etaRanges[i+1]), 800, 800))
	canvases[i].cd()
	profiles.append(histFile.Get("Photon_id/phMVAvsEProf%i"%i))
	profiles[i].Draw()
	profiles[i].SetTitle("Leading #gamma MVA, %.3f#leq|#eta|<%.3f"%(etaRanges[i], etaRanges[i+1]))
	profiles[i].GetXaxis().SetTitle("Leading #gamma p_{T} (GeV)")
	profiles[i].GetYaxis().SetTitle("MVA value")
	canvases[i].Update()
	statsbox = profiles[i].FindObject("stats")
	statsbox.SetX1NDC(0.679648)
	statsbox.SetX2NDC(0.880653)
	statsbox.SetY1NDC(0.134367)
	statsbox.SetY2NDC(0.374677)
	canvases[i].Update()
	canvases[i].Print("output/photonMVAvsE%i.pdf"%i)

# Trick to keep graphical output open
#if __name__ == '__main__':          
#   rep = ''
#   while not rep in [ 'q', 'Q' ]:
#      rep = raw_input( 'enter "q" to quit: ' )
#      if 1 < len(rep):
#         rep = rep[0]
