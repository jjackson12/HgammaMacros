from ROOT import *
from pyrootTools import * 
from getMCbgWeights import *
from HgParameters import *
from HgCuts import *
  
sampleDirs = getSamplesDirs()
weightsDict = getWeightsDict(sampleDirs["small3sDir"])

def testMethod(hist, sampleName):
  pre = getFilePrefix()
  fullFileName = sampleDirs["ddDir"]+pre+sampleName
  print "fullFileName is: %s" % fullFileName
  tfile = TFile(fullFileName)

  tree = tfile.Get("higgs") 
  tree.Draw("phJetInvMass_pruned_higgs", getAntiBtagComboCut())
  htemp = gPad.GetPrimitive("htemp")
  hist.GetXaxis().SetLimits(htemp.GetXaxis().GetBinUpEdge(0), htemp.GetXaxis().GetBinUpEdge(htemp.GetXaxis().GetNbins()))
  for histbin in range(0,htemp.GetXaxis().GetNbins()):
    hist.SetBinContent(histbin, weightsDict[sampleName]*htemp.GetBinContent(histbin))


#hists = []
#for key in weightsDict.keys():
#  hists.append(TH1F("", "", 100, 0, 0))
#  testMethod(hists[-1], key)
hist = TH1F("","",100,0,0)
testMethod(hist, weightsDict.keys()[1])
c = TCanvas()
c.cd()
drawInNewCanvas(hist)

#c = TCanvas()
#c.cd()
#for hist in hists:
#  drawInNewCanvas(hist)

