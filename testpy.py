from ROOT import *
from pyrootTools import *
from getMCbgWeights import *
from HgParameters import *
from HgCuts import *

sampleDirs = getSamplesDirs()
weightsDict = getWeightsDict(sampleDirs["small3sDir"])

def makeHist(hist, var, key, region):
  nEntries = tree.Draw("%s>> hist"%var, getAntiBtagComboCut())
  if nEntries == 0:
    return False
  else:
    outFile = TFile("weightedMCbgHists/%s_%s_%s"%(region, var, key), "RECREATE")
    outFile.cd()
    for histBin in range (0,hist.GetXaxis().GetNbins()):
      hist.SetBinContent(histBin, hist.GetBinContent(histBin)*weightsDict[key])  
    hist.Write()
    outFile.Close()
    return True
  
pre = getFilePrefix()
varNames = []
tfile = TFile(sampleDirs["ddDir"]+pre+getWeightsDict(getSamplesDirs()["small3sDir"]).keys()[0])
sidebandTree = tfile.Get("side100110")
for branch in sidebandTree.GetListOfBranches():
  varNames.append(branch.GetName())
regions = ["higgs", "side100110", "side5070"]
for region in regions:
  tree = tfile.Get(region)
  for var in varNames:
    for key in getWeightsDict(getSamplesDirs()["small3sDir"]).keys():
      tfile = TFile(sampleDirs["ddDir"]+pre+key)
      sidebandTree = tfile.Get("side100110")
      #fullFileName = sampleDirs["ddDir"]+pre+weightsDict.keys()[1]
      hist = TH1F("hist","hist",3250,0,13000)
      if makeHist(hist, var, key, region):
    
        cblah=TCanvas()
        cblah.cd()
        hist.Draw()
