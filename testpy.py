from ROOT import *
from pyrootTools import *
from getMCbgWeights import *
from HgParameters import *
from HgCuts import *

makeHists = False

def getHiggsRangesDict():
  rangesDict = {}
  rangesDict["cosThetaStar"] = [0., 1.]
  rangesDict["phPtOverMgammaj"]=[0., 2.]
  rangesDict["leadingPhPhi"]=[-3.5, 3.5]
  rangesDict["leadingPhPt"]=[0., 4000.]
  rangesDict["leadingPhAbsEta"]=[0.,4.]
  rangesDict["leadingPhEta"]=[-4.,4.]
  label = "higgs"
  rangesDict["%sJet_HbbTag"%label]=[-1. , 1.]
  rangesDict["%sJet_pruned_abseta"%label]=[0., 4.]
  rangesDict["%sJett2t1"%label]=[-1, 1]
  rangesDict["%sPrunedJetCorrMass"%label]=[0,4000]
  rangesDict["phJetDeltaR_%s"%label]=[0,15]
  rangesDict["phJetInvMass_pruned_%s"%label]=[0,8000]
  return rangesDict

def getSidebandRangesDict(sideband):
  rangesDict = {}
  if sideband == "100110":
    index="Four"
  elif sideband == "5070":
    index="Three"
  else:
    print "Invalid sideband! Either 100110 or 5070."
    quit()
  label="sideLow%s"%index
  rangesDict["cosThetaStar"] = [0., 1.]
  rangesDict["phPtOverMgammaj"]=[0., 2.]
  rangesDict["leadingPhPhi"]=[-3.5, 3.5]
  rangesDict["leadingPhPt"]=[0., 4000.]
  rangesDict["leadingPhAbsEta"]=[0.,4.]
  rangesDict["leadingPhEta"]=[-4.,4.]
  rangesDict["%sJet_HbbTag"%label]=[-1. , 1.]
  rangesDict["%sJet_pruned_abseta"%label]=[0., 4.]
  rangesDict["%sJett2t1"%label]=[-1, 1]
  rangesDict["%sPrunedJetCorrMass"%label]=[0,4000]
  rangesDict["phJetDeltaR_%s"%label]=[0,15]
  rangesDict["phJetInvMass_pruned_%s"%label]=[0,8000]
  return rangesDict

def getRangesDict():
  rangesDict = {}
  higgsRangesDict = getHiggsRangesDict()
  for key in higgsRangesDict.keys():
    rangesDict[key]=higgsRangesDict[key]
  lowFourRangesDict = getSidebandRangesDict("100110")
  for key in lowFourRangesDict.keys():
    rangesDict[key]=lowFourRangesDict[key]
  lowThreeRangesDict = getSidebandRangesDict("5070")
  for ranges in lowThreeRangesDict.keys():
    rangesDict[key]=lowThreeRangesDict[key]
  return rangesDict

  
def makeAllHists():
  sampleDirs = getSamplesDirs()
  weightsDict = getWeightsDict(sampleDirs["small3sDir"])
  regions = ["higgs", "side100110", "side5070"]
  rangesDict = getRangesDict()
  for key in getWeightsDict(getSamplesDirs()["small3sDir"]).keys():
    for region in regions:
      pre = getFilePrefix()
      tfile = TFile(sampleDirs["ddDir"]+pre+key)
      tree = tfile.Get(region)
      varNames = []
      for branch in tree.GetListOfBranches():
        if not "csvValues" in branch.GetName() and not "subjetCut" in branch.GetName():
          varNames.append(branch.GetName())
      for var in varNames:
        hist = TH1F("hist_%s_%s_%s"%(var, region, key),"hist_%s_%s_%s"%(var, region, key),100,rangesDict[var][0],rangesDict[var][1])
        nEntries = tree.Draw("%s>> hist_%s_%s_%s"%(var, var, region, key), getAntiBtagComboCut(region))
        if not nEntries == 0:
            outFile = TFile("weightedMCbgHists/%s_%s_%s"%(var, region, key), "RECREATE")
            outFile.cd()
            for histBin in range (0,hist.GetXaxis().GetNbins()):
              hist.SetBinContent(histBin, hist.GetBinContent(histBin)*weightsDict[key])  
            hist.Write()
            outFile.Close()

if makeHists:
  print "making all histograms!"
  makeAllHists()
