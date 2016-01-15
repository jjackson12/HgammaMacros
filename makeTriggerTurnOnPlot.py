# This macro makes the trigger turn-on plot
# it takes one argument: the input filename
# Example: python makeTriggerTurnOnPlot.py myFlatTuple.root
# John Hakala 1/15/2016

from sys import argv
from ROOT import *

if not len(argv)>1 :
	print "Please supply one argument to this macro: the name of the input root file."
	exit(1)

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
  ratios[i].Draw()
  canvases[i].Print("output/%s"%outputPlotNames[i])

