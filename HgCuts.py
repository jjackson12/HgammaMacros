import copy
from ROOT import TCut
# functions to define the selection cuts for H(bb)Gamma 
# John Hakala 7/13/16

def getCutValues():
  cutValues = {}
  cutValues["minInvMass"]  = 600.0
  cutValues["phEta"]       = 1.4442
  cutValues["jetEta"]      = 2.2
  cutValues["deltaR"]      = 1.1
  cutValues["ptOverM"]     = 0.35
  cutValues["Hbb"]         = 0.9
  # WARNING WARNING TODO this is just for s+g
  #cutValues["higgsWindow"] = [110.0, 140.0]
  cutValues["higgsWindow"] = [50.0, 9999999999.9]
  return cutValues


def combineCuts(cutDict):
  combinedCut = TCut()
  for cut in cutDict.keys():
    combinedCut += cutDict[cut]
  return combinedCut

def getVarKeys():
  varKeys = {}
  varKeys["higgsJett2t1"]              = "t2t1"
  varKeys["higgsJet_HbbTag"]           = "btagHolder"
  varKeys["cosThetaStar"]              = "cosThetaStar"
  varKeys["phPtOverMgammaj"]           = "ptOverM"
  varKeys["leadingPhEta"]              = "phEta"
  varKeys["leadingPhPhi"]              = "phPhi"
  varKeys["leadingPhPt"]               = "phPt"
  varKeys["leadingPhAbsEta"]           = "phEta"
  varKeys["phJetInvMass_pruned_higgs"] = "turnon"
  varKeys["phJetDeltaR_higgs"]         = "deltaR"
  varKeys["higgsJet_pruned_abseta"]    = "jetEta"
  varKeys["higgsPrunedJetCorrMass"]    = "higgsWindow"
  return varKeys

def makeHiggsWindow():
    cutValues = getCutValues()
    cuts = {}
    cuts["higgsWindowLow"] = TCut( "higgsPrunedJetCorrMass>%f"   % cutValues["higgsWindow"][0] )
    cuts["higgsWindowHi"]  = TCut( "higgsPrunedJetCorrMass<%f"   % cutValues["higgsWindow"][1] )
    return combineCuts(cuts)

def getDefaultCuts(region):
    cutValues = getCutValues()

    cuts = {} 
    cuts["phEta"]           = TCut( "leadingPhAbsEta<%f"           % cutValues["phEta"]  )
    cuts["ptOverM"]         = TCut( "phPtOverMgammaj>%f"           % cutValues["ptOverM"]    )
    cuts ["phPhi"]          = TCut()
    cuts ["t2t1"]           = TCut()
    cuts ["btagHolder"]     = TCut()
    cuts ["cosThetaStar"]   = TCut()
    cuts ["phPt"]           = TCut()
    if region is "higgs":
      cuts["turnon"]   = TCut( "phJetInvMass_pruned_higgs>%f"      % cutValues["minInvMass"]     )
      cuts["deltaR"]   = TCut( "phJetDeltaR_higgs>%f"              % cutValues["deltaR"]         )
      cuts["jetEta"]   = TCut( "higgsJet_pruned_abseta<%f"         % cutValues["jetEta"]         )
      cuts["btag"]     = TCut( "higgsJet_HbbTag>%f"                % cutValues["Hbb"]            )
      cuts["antibtag"] = TCut( "higgsJet_HbbTag<%f"                % cutValues["Hbb"]            )
      #cuts["higgsWindowLow"] = TCut( "higgsPrunedJetCorrMass>%f"   % cutValues["higgsWindow"][0] )
      #cuts["higgsWindowHi"]  = TCut( "higgsPrunedJetCorrMass<%f"   % cutValues["higgsWindow"][1] )
      cuts["higgsWindow"]   = makeHiggsWindow()
    elif region is "side5070" or region is "side100110":
      if region is "side5070":
        index = "Three"
      else:
        index = "Four"
      cuts["turnon"]   = TCut( "phJetInvMass_pruned_sideLow%s>%f" % (index, cutValues["minInvMass"] ))
      cuts["deltaR"]   = TCut( "phJetDeltaR_sideLow%s>%f"         % (index, cutValues["deltaR"]     ))
      cuts["jetEta"]   = TCut( "sideLow%sJet_pruned_abseta<%f"    % (index, cutValues["jetEta"]     ))
      cuts["btag"]     = TCut( "sideLow%sJet_HbbTag>%f"           % (index, cutValues["Hbb"]        ))
      cuts["antibtag"] = TCut( "sideLow%sJet_HbbTag<%f"           % (index, cutValues["Hbb"]        ))
    else:
      print "Invalid region!!!"
      quit()
    return cuts
    
def getBtagComboCut(region):
    btagCuts = copy.deepcopy(getDefaultCuts(region))
    btagCuts.pop("antibtag")
    return combineCuts(btagCuts)

def getBtagComboCut(region):
    btagCuts = copy.deepcopy(getDefaultCuts(region))
    btagCuts.pop("antibtag")
    return combineCuts(btagCuts)
    
def getAntiBtagComboCut(region):
    antibtagCuts = copy.deepcopy(getDefaultCuts(region))
    antibtagCuts.pop("btag")
    return combineCuts(antibtagCuts)

def getNoBtagComboCut(region):
    nobtagCuts = copy.deepcopy(getDefaultCuts(region))
    nobtagCuts.pop("btag")
    nobtagCuts.pop("antibtag")
    return combineCuts(nobtagCuts)

def getOnlyWindowComboCut(region):
    nobtagCuts = copy.deepcopy(getDefaultCuts(region))
    for cut in nobtagCuts.keys():
      if not cut == "higgsWindow":
        nobtagCuts.pop(cut)
    return combineCuts(nobtagCuts)

def getNminus1ComboCut(region, popVar, withBtag):
    nobtagCuts = copy.deepcopy(getDefaultCuts(region))
    nobtagCuts.pop("antibtag")
    if not withBtag:
      nobtagCuts.pop("btag")
    nobtagCuts.pop(getVarKeys()[popVar])
    return combineCuts(nobtagCuts)

