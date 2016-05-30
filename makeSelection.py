import copy
from ROOT import *
from pyrootTools import instance
from HgParameters import *


def combineCuts(cutDict):
  combinedCut = TCut()
  for cut in cutDict.keys():
    combinedCut += cutDict[cut]
  return combinedCut

def drawInNewCanvas(tree, var, comboCut, label):
  newCan = TCanvas()
  newCan.cd()
  tree.Draw(var, comboCut)
  newCan.Print("%s_%s.pdf"%(var, label))


samplesDirs = getSamplesDirs()
dataFileName = samplesDirs["dataDir"]

cuts = {}
#cuts["turnon"]   = TCut("phJetInvMass_pruned_higgs>600")
cuts["phEta"]    = TCut("leadingPhAbsEta<1.4442")
cuts["jetEta"]   = TCut("higgsJet_pruned_abseta<2.2")
cuts["deltaR"]   = TCut("phJetDeltaR_higgs>1.1")
cuts["ptOverM"]  = TCut("phPtOverMgammaj>0.35")
cuts["btag"]     = TCut("higgsJet_HbbTag>0.9")
cuts["antibtag"] = TCut("higgsJet_HbbTag<0.9")

btagCuts = copy.deepcopy(cuts)
btagCuts.pop("antibtag")
btagComboCut = combineCuts(btagCuts)
print btagComboCut

antibtagCuts = copy.deepcopy(cuts)
antibtagCuts.pop("btag")
antibtagComboCut = combineCuts(antibtagCuts)
print antibtagComboCut

notagCuts = copy.deepcopy(btagCuts)
notagCuts.pop("btag")
notagComboCut = combineCuts(notagCuts)
print notagComboCut

dataFile = TFile(dataFileName)
higgsTree = dataFile.Get("higgs")
drawInNewCanvas(higgsTree, "phJetInvMass_pruned_higgs", notagComboCut,    "notag")
drawInNewCanvas(higgsTree, "phJetInvMass_pruned_higgs", antibtagComboCut, "antibtag")
drawInNewCanvas(higgsTree, "phJetInvMass_pruned_higgs", btagComboCut,     "btag")

