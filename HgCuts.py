# functions to define the selection cuts for 
import copy
from ROOT import TCut

def getCutValues():
  cutValues = {}
  cutValues["minInvMass"] = 600
  cutValues["photonEta"]  = 1.4442
  cutValues["jetEta"]     = 2.2
  cutValues["deltaR"]     = 1.1
  cutValues["ptOverM"]    = 0.35
  cutValues["Hbb"]        = 0.9
  return cutValues


def combineCuts(cutDict):
  combinedCut = TCut()
  for cut in cutDict.keys():
    combinedCut += cutDict[cut]
  return combinedCut

def getDefaultCuts():
    cutValues = getCutValues()

    cuts = {} 
    cuts["turnon"]   = TCut( "phJetInvMass_pruned_higgs>%f" % cutValues["minInvMass"] )
    cuts["phEta"]    = TCut( "leadingPhAbsEta<%f"           % cutValues["photonEta"]  )
    cuts["jetEta"]   = TCut( "higgsJet_pruned_abseta<%f"    % cutValues["jetEta"]     )
    cuts["deltaR"]   = TCut( "phJetDeltaR_higgs>%f"         % cutValues["deltaR"]     )
    cuts["ptOverM"]  = TCut( "phPtOverMgammaj>%f"           % cutValues["ptOverM"]    )
    cuts["btag"]     = TCut( "higgsJet_HbbTag>%f"           % cutValues["Hbb"]        )
    cuts["antibtag"] = TCut( "higgsJet_HbbTag<%f"           % cutValues["Hbb"]        )
    return cuts
    
def getBtagComboCut():
    btagCuts = copy.deepcopy(getDefaultCuts())
    btagCuts.pop("antibtag")
    return combineCuts(btagCuts)
    
def getAntiBtagComboCut():
    antibtagCuts = copy.deepcopy(getDefaultCuts())
    antibtagCuts.pop("btag")
    return combineCuts(antibtagCuts)

