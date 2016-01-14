# This macro makes the trigger turn-on plot
# it takes one argument: the input filename
# Example: python makeTriggerTurnOnPlot.py myFlatTuple.root
from sys import argv
from ROOT import *

histsfile = TFile(argv[1],"r")
trigHist = histsfile.Get("leadingPhPtHist_trig")
noTrigHist = histsfile.Get("leadingPhPtHist_noTrig")
ratio = TGraphAsymmErrors()
ratio.Divide(trigHist, noTrigHist)
canvas = TCanvas("canvas", "Trigger Efficiency", 800, 800)
canvas.cd()
ratio.Draw()
canvas.Print("triggerTurnOn_test.pdf")

