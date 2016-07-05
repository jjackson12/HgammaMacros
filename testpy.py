from ROOT import *
from pyrootTools import *
from getMCbgWeights import *
from HgParameters import *
from HgCuts import *

sampleDirs = getSamplesDirs()
weightsDict = getWeightsDict(sampleDirs["small3sDir"])

def doCrap(hist, var, key):
  nEntries = tree.Draw("%s>> hist"%var, getAntiBtagComboCut())
  if nEntries == 0:
    return False
  else:
    outFile = TFile("weightedMCbgHists/%s_%s"%(var, key), "RECREATE")
    outFile.cd()
    for histBin in range (0,hist.GetXaxis().GetNbins()):
      hist.SetBinContent(histBin, hist.GetBinContent(histBin)*weightsDict[key])  
    hist.Write()
    outFile.Close()
    return True
  
pre = getFilePrefix()
var="phJetInvMass_pruned_higgs"
for key in getWeightsDict(getSamplesDirs()["small3sDir"]).keys():
  tfile = TFile(sampleDirs["ddDir"]+pre+key)
  tree = tfile.Get("higgs")
  #fullFileName = sampleDirs["ddDir"]+pre+weightsDict.keys()[1]
  hist = TH1F("hist","hist",3250,0,13000)
  if doCrap(hist, var, key):

    cblah=TCanvas()
    cblah.cd()
    hist.Draw()
