# This macro makes the trigger turn-on plot
# it takes one argument: the input filename
# Example: python makeTriggerTurnOnPlot.py myFlatTuple.root
# John Hakala 1/15/2016

from sys import argv
from os import path, makedirs
from ROOT import *

if not len(argv)>1 :
	print "Please supply one argument to this macro: the name of the input root file."
	exit(1)

if not path.exists("output"):
	makedirs("output")

histsfile = TFile(argv[1],"r")
inputHistNames  = [ ["leadingPhPtHist_trig", "leadingPhPtHist_noTrig"], ["leadingPhPt_noIDHist_trig","leadingPhPt_noIDHist"] ] 
outputPlotNames = [ "triggerTurnOn_IDapplied.pdf", "triggerTurnOn_noID.pdf" ]
ratios = []
canvases = []
for i in range (0, 2):
	trigHist = histsfile.Get("Trigger_turnon/%s"%inputHistNames[i][0])
	noTrigHist = histsfile.Get("Trigger_turnon/%s"%inputHistNames[i][1])
	ratios.append(TGraphAsymmErrors())
	ratios[i].Divide(trigHist, noTrigHist)
	canvases.append(TCanvas("canvas%i"%i, "Trigger Efficiency", 800, 800))
	canvases[i].cd()
	ratios[i].GetXaxis().SetTitle("Leading #gamma p_{T} (GeV)")
	ratios[i].GetYaxis().SetTitle("Efficiency")
	ratios[i].SetTitle("HLT_Photon_175_v1 Trigger Efficiency")
	ratios[i].Draw("ap")
	canvases[i].Print("output/%s"%outputPlotNames[i])


## Trick to keep plot open
#if __name__ == '__main__':
#   rep = ''
#   while not rep in [ 'q', 'Q' ]:
#      rep = raw_input( 'enter "q" to quit: ' )
#      if 1 < len(rep):
#         rep = rep[0]
