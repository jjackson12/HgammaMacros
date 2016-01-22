# Script to make a WZgamma stack plot
# It takes one argument: the filename for a text file specifying the file for each sample
# The file for each sample is produced by the treeChecker
# An example text file is included on the github repository, stackPlotInputs.tx
# Example: python makeStackPlot.py myStackPlotInputs.tx
# John Hakala, 1/20/2016

from ROOT import *
from dictmaker import makeInputsDict
from sys import argv
from os import path, makedirs

if not len(argv)>2:
	print "Please supply two arguments to this macro: the name of the input text file defining the inputs, and 'requireTrigger' or 'noTrigger'."
	exit(1)

if not path.exists("output"):
	makedirs("output")

samplesDict = makeInputsDict(argv[1])

# Check the dict for all the keys:
keys = ["zJets", "wJets", "QCD", "gammaJets", "M-750", "M-2000", "data"]
for key in keys:
	if not key in samplesDict.keys():
		exit("\nError: a file for sample %s was not found in %s.\n"%(key, argv[1]))

infiles = [
	[ "zJets"     ,  samplesDict["zJets"]     ,  kMagenta, "bg"   ],
	[ "wJets"     ,  samplesDict["wJets"]     ,  kGreen  , "bg"   ],
	[ "QCD"       ,  samplesDict["QCD"]       ,  kRed    , "bg"   ],
	[ "gammaJets" ,  samplesDict["gammaJets"] ,  kBlue   , "bg"   ],
	[ "M-750"     ,  samplesDict["M-750"]     ,  kCyan   , "sig"  ],
	[ "M-2000"    ,  samplesDict["M-2000"]    ,  kViolet , "sig"  ]
]

canvas=TCanvas("canvas", "Invariant mass", 800, 800)
canvas.SetLogy()
stackPlot    = THStack("stackPlot","")
tFiles       = []
invMassHists = []
names        = []
colors       = []
kinds        = []

legend = TLegend(0.5, 0.7, 0.9, 0.9)
legend.SetHeader("Invariant mass of leading #gamma plus z-jet.")

dataFile = TFile(samplesDict["data"],"r")
dataHist = dataFile.Get("Resonance/phJetInvMassHist_pruned")
dataHist.Rebin(10)

for i in range(0, len(infiles)):
	tFiles.append(TFile(infiles[i][1], "r"))
	if argv[2] is "requireTrigger":
		invMassHists.append(tFiles[i].Get("Resonance/phJetInvMassHist_pruned"))
	elif argv[2] is "noTrigger":
		invMassHists.append(tFiles[i].Get("Resonance/phJetInvMassHist_pruned_noTrig"))
	invMassHists[i].Rebin(10)
	names.append(infiles[i][0])
	colors.append(infiles[i][2])
	kinds.append(infiles[i][3])
	if kinds[i] is "bg":
		print "sample %s has kind %s"%(names[i], kinds[i])
		invMassHists[i].SetFillColor(colors[i])
	elif kinds[i] is "sig":
		print "sample %s has kind %s"%(names[i], kinds[i])
		invMassHists[i].SetLineColor(colors[i])
		invMassHists[i].SetLineStyle(3)
	stackPlot.Add(invMassHists[i])
	legend.AddEntry(invMassHists[i], names[i], "f")

dataHist.SetMarkerColor(kBlack)
dataHist.SetMarkerStyle(20)
dataHist.SetLineColor(kBlack)
legend.AddEntry(dataHist, "data, 2.2 fb^{-1}", "f")

canvas.cd()
stackPlot.Draw()
stackPlot.GetXaxis().SetRangeUser(300, 5000)
stackPlot.GetXaxis().SetTitle("m_{#gammaj} (GeV)")
stackPlot.GetYaxis().SetTitleOffset(1.2)
stackPlot.GetYaxis().SetTitle("Events / 100 GeV")
stackPlot.SetMinimum(5e-3)
dataHist.Draw("apE1 SAME")
legend.Draw()
canvas.Update()

canvas.Print("output/stackPlot.pdf")
	
#if __name__ == '__main__':
#	rep = ''
#	while not rep in [ 'q', 'Q' ]:
#		rep = raw_input( 'enter "q" to quit: ' )
#		if 1 < len(rep):
#			rep = rep[0]
