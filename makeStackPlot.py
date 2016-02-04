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

if not len(argv)>5:
   print "Please supply six arguments to this macro: the name of the input text file defining the inputs,  'requireTrigger' or 'noTrigger', the name of the histogram to be stacked, the rootfile name of that histogram, the rebin value, and either 'log' or 'lin'"
   exit(1)
elif argv[2]=="requireTrigger":
   histName=argv[4]
#elif argv[2]=="noTrigger":
#   histName="Resonance/phJetInvMassHist_pruned_sig_noTrig"
else:
   print "Please specify whether you want to require the trigger be fired by specifying the last argument as 'requireTrigger' or 'noTrigger'."
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
   [ "wJets"     ,  samplesDict["wJets"]     ,  kGreen+1   , "bg"   ],
   [ "zJets"     ,  samplesDict["zJets"]     ,  kMagenta+2 , "bg"   ],
   [ "QCD"       ,  samplesDict["QCD"]       ,  kRed-4     , "bg"   ],
   [ "gammaJets" ,  samplesDict["gammaJets"] ,  kBlue    , "bg"   ],
   [ "M-750"     ,  samplesDict["M-750"]     ,  kTeal+1    , "sig"  ],
   [ "M-2000"    ,  samplesDict["M-2000"]    ,  kViolet  , "sig"  ]
]

rebin=int(argv[5])

canvas=TCanvas("canvas", "Invariant mass", 800, 800)
if argv[6]=="log":
    canvas.SetLogy()
stackPlot    = THStack("stackPlot","")
tFiles       = []
invMassHists = []
names        = []
colors       = []
kinds        = []

legend = TLegend(0.5, 0.7, 0.9, 0.9)
legend.SetHeader("")

dataFile = TFile(samplesDict["data"],"r")
print "histName is: %s"%histName
dataHist = dataFile.Get(histName)
dataHist.Rebin(rebin)

for i in range(0, len(infiles)):
   print "working on sample: %s"%infiles[i][0]
   tFiles.append(TFile(infiles[i][1], "r"))
   print "using file %s"%tFiles[i]
   invMassHists.append(tFiles[i].Get(histName))
   invMassHists[i].Rebin(rebin)
   names.append(infiles[i][0])
   colors.append(infiles[i][2])
   kinds.append(infiles[i][3])
   invMassHists[i].SetTitle("")
   if kinds[i] is "bg":
      print "sample %s has kind %s"%(names[i], kinds[i])
      invMassHists[i].SetFillColor(colors[i])
      stackPlot.Add(invMassHists[i])
   elif kinds[i] is "sig":
      print "sample %s has kind %s"%(names[i], kinds[i])
      invMassHists[i].SetLineColor(colors[i])
      invMassHists[i].SetLineStyle(3)
      invMassHists[i].SetLineWidth(3)
   legend.AddEntry(invMassHists[i], names[i], "f")


dataHist.SetMarkerColor(kBlack)
dataHist.SetMarkerStyle(20)
dataHist.SetLineColor(kBlack)
legend.AddEntry(dataHist, "data, 2.2 fb^{-1}", "f")

canvas.cd()
stackPlot.Draw()
#stackPlot.GetXaxis().SetRangeUser(0, 5000)
#stackPlot.GetXaxis().SetTitle("m_{#gammaj} (GeV)")
#stackPlot.GetYaxis().SetTitleOffset(1.2)
#stackPlot.GetYaxis().SetTitle("Events / 100 GeV")
#stackPlot.SetMinimum(5e-1)
dataHist.SetTitle("")
dataHist.Draw("apE1 SAME")
for i in range(0, len(infiles)):
   if kinds[i] is "sig":
      invMassHists[i].SetTitle("")
      invMassHists[i].Draw("SAME")

legend.Draw()
canvas.Update()

canvas.SaveAs("output/%s.root"%argv[3])
