from ROOT import *
from pyrootTools import *
from getMCbgWeights import *
from HgParameters import *
from HgCuts import *

sampleDirs = getSamplesDirs()
weightsDict = getWeightsDict(sampleDirs["small3sDir"])

def makeHist(tree, hist, var, key, region):
  nEntries = tree.Draw("%s>> hist"%var, getAntiBtagComboCut(region))
  if nEntries == 0:
    return False
  else:
    outFile = TFile("weightedMCbgHists/%s_%s_%s"%(key, region, var), "RECREATE")
    outFile.cd()
    for histBin in range (0,hist.GetXaxis().GetNbins()):
      hist.SetBinContent(histBin, hist.GetBinContent(histBin)*weightsDict[key])  
    hist.Write()
    outFile.Close()
    return True
  
pre = getFilePrefix()
regions = ["higgs", "side100110", "side5070"]
for key in getWeightsDict(getSamplesDirs()["small3sDir"]).keys():
  tfile = TFile(sampleDirs["ddDir"]+pre+key)
  for region in regions:
    inTree = tfile.Get(region)
    varNames = []
    for branch in inTree.GetListOfBranches():
      varNames.append(branch.GetName())
    print "Tree name %s has branches:"%inTree.GetName()
    print varNames
    for var in varNames:
      hist = TH1F("hist_%s_%s_%s"%(key, var, region),"hist_%s_%s_%s"%(key, var, region),3250,0,13000)
      if makeHist(inTree, hist, var, key, region):

        cblah=TCanvas()
        cblah.cd()
        hist.Draw()
    del varNames
