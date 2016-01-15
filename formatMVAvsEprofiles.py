# Script to format a the photon id MVA value vs. energy profiles
# This script requires one argument: the input filename Example:
# python formatMVAvsEprofiles.py myFlatTuple.root
# John Hakala 1/15/2016

from ROOT import *
from sys import argv

if not len(argv)>1:
	print "Please supply one argument to this macro: the name of the input root file."
	exit(1)

etaRanges = [0, 0.75, 1.479, 2.4, 3.0]  # This comes from treeChecker.C, which considers four regions: the inner and outer halves of both EE and EB

histFile = TFile(argv[1], "r")
profiles = []
canvases = []
for i in range(0,4):
	canvases.append(TCanvas("canvas%i"%i, "MVA values for photons in range %f#leq|#eta|<%f"%(etaRanges[i], etaRanges[i+1]), 800, 800))
	canvases[i].cd()
	profiles.append(histFile.Get("Photon_id/phMVAvsEProf%i"%i))
	profiles[i].Draw()
	canvases[i].Print("output/photonMVAvsE%i.pdf"%i)
