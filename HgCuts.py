# functions to define the selection cuts for 
import copy
from ROOT import TCut

def combineCuts(cutDict):
  combinedCut = TCut()
  for cut in cutDict.keys():
    combinedCut += cutDict[cut]
  return combinedCut

def getDefaultCuts():
    cuts = {} 
    cuts["turnon"]   = TCut("phJetInvMass_pruned_higgs>600")
    cuts["phEta"]    = TCut("leadingPhAbsEta<1.4442")
    cuts["jetEta"]   = TCut("higgsJet_pruned_abseta<2.2")
    cuts["deltaR"]   = TCut("phJetDeltaR_higgs>1.1")
    cuts["ptOverM"]  = TCut("phPtOverMgammaj>0.35")
    cuts["btag"]     = TCut("higgsJet_HbbTag>0.9")
    cuts["antibtag"] = TCut("higgsJet_HbbTag<0.9")
    return cuts
    
def getBtagComboCut():
    btagCuts = copy.deepcopy(getDefaultCuts())
    btagCuts.pop("antibtag")
    return combineCuts(btagCuts)
    
def getAntiBtagComboCut():
    antibtagCuts = copy.deepcopy(getDefaultCuts())
    antibtagCuts.pop("btag")
    return combineCuts(antibtagCuts)

