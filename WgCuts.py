import copy
from ROOT import TCut
# functions to define the selection cuts for H(bb)Gamma 
# John Hakala 7/13/16


#Baseline preselection cut values
def getCutValues():
  cutValues = {}
  cutValues["minInvMass"]     = 600
  #cutValues["minWJetMass"]    = 30
  cutValues["phEta"]          = 1.4442
  #cutValues['phEta']           = 2.2
  cutValues["phPt"]           = 180.0
  cutValues["jetAbsEta"]      = 2.2
  cutValues["jetPt"]          = 220.0
  cutValues["deltaR"]         = 1.1
  #cutValues["phPtOverM"]      = -1	
  #cutValues["WPtOverM"]       = -1
  #cutValues["HT"]             = i
  #cutValues["Tau21"]          = 0.65

  #cutValues["WWindow"]        = [70,90]
  #cutValues["sidebandWindow"] = [100.0, 110.0]
  #cutValues["sideband5070Window"] = [50.0, 70.0]
  #cutValues["sideband80100Window"] = [80.0, 100.0]
  #cutValues["preselectionWindow"] = [30.0, 99999.9]
  return cutValues


#down: Cuts on (keeps) events less than value
#up: Cuts on (keeps) events more than value
#both: cuts within phase space
def getDirections():
  directions = {}
  directions["minInvMass"] = "up"
  directions["Tau21"] = "down"
  directions["cosThetaStar"] = "down"
  directions["phPtOverM"] = "up"
  directions["WPtOverM"] = "down"
  #FOR SIDEBAND: directions["phEta"] = "down"
  directions["phPt"] = "up"
  directions["phEta"] = "down"
  #directions["deltaR"] = "up"
  directions["jetEta"] = "down"
  directions["jetPhi"] = "both"
  directions["jetPt"] = "up"
  return directions

def combineCuts(cutDict):
  combinedCut = TCut()
  for cut in cutDict.keys():
    combinedCut += cutDict[cut]
  return combinedCut

def getVarKeys():
  varKeys = {}
  varKeys["WJetTau21"]              = "Tau21"
  varKeys["cosThetaStar"]              = "cosThetaStar"
  varKeys["phPtOverMgammaj"]           = "phPtOverM"
  varKeys["WJetPtOverMgammaj"]           = "WPtOverM"
  varKeys["leadingPhEta"]              = "phEta"
  varKeys["leadingPhPhi"]              = "phPhi"
  varKeys["leadingPhPt"]               = "phPt"
  varKeys["leadingPhAbsEta"]           = "phEta"
  varKeys["phJetInvMass_puppi_softdrop_W"] = "turnon"
  varKeys["phJetDeltaR_W"]         = "deltaR"
  varKeys["WJet_puppi_abseta"]    = "jetAbsEta"
  varKeys["WJet_puppi_eta"]       = "jetEta"
  varKeys["WJet_puppi_phi"]       = "jetPhi"
  varKeys["WJet_puppi_pt"]        = "jetPt"
  varKeys["WPuppi_softdropJetCorrMass"]    = "WWindow"
  return varKeys

def makeWWindow(sideband=False, windowEdges=[70,90]):
    #print "makeHiggsWindow got sideband =", sideband, "and windowEdges =", windowEdges
    #cutValues = getCutValues()
    cuts = {}
    #window = "WWindow"
    #if sideband:
    #  if windowEdges == [100.0,110.0]:
    #    window = "sidebandWindow"
    #  elif windowEdges == [50.0,70.0]:
    #    window = "sideband5070Window"
    #  elif windowEdges == [80.0,100.0]:
    #    window = "sideband80100Window"
    #  elif windowEdges == [30.0,99999.9]:
    #    window = "preselectionWindow"
    cuts["WWindowLow"] = TCut( "WPuppi_softdropJetCorrMass>%f"   % windowEdges[0] )
    cuts["WWindowHi"]  = TCut( "WPuppi_softdropJetCorrMass<%f"   % windowEdges[1] )
    #print "will return combineCuts(cuts)=", combineCuts(cuts)
    return combineCuts(cuts)

def makeTrigger(which = "OR"):
  cutValues = getCutValues()
  cuts = {}
  if which == "OR":
    cuts["trigger"] = TCut( "triggerFired_175 > 0.5 || triggerFired_165HE10 > 0.5" )
  return combineCuts(cuts)
    

def getDefaultCuts( useTrigger, sideband=False, windowEdges=[70,90]):
    cutValues = getCutValues()
    print "sideband = %s"%sideband
    cuts = {} 
    cuts["phEta"]           = TCut( "leadingPhAbsEta<%f"           % cutValues["phEta"]      )
    #cuts["phPtOverM"]         = TCut( "phPtOverMgammaj>%f"           % cutValues["phPtOverM"]    )
    #cuts["WPtOverM"]         = TCut( "WPtOverMgammaj>%f"           % cutValues["WPtOverM"]    )
    cuts ["phPt"]           = TCut("leadingPhPt>%f"                % cutValues["phPt"]       )
    cuts["deltaR"]   = TCut( "phJetDeltaR_W>%f"              % cutValues["deltaR"]         )
    cuts["jetAbsEta"]       = TCut( "WJet_puppi_abseta<%f"         % cutValues["jetAbsEta"]      )
    cuts ["jetPt"]          = TCut("WJet_puppi_pt>%f"          % cutValues["jetPt"]      )
    cuts ["phPhi"]          = TCut()
    cuts ["Tau21"]           = TCut()
    cuts ["jetPhi"]         = TCut()
    #cuts ["jetEta"]         = TCut()
    cuts ["cosThetaStar"]   = TCut()
    if(not(len(windowEdges)==0)):
      cuts["WWindow"]     = makeWWindow(sideband, windowEdges)
    #else:
      #cuts["minWJetMass"] = TCut("WPuppi_softdropJetCorrMass>%f"  % cutValues["minWJetMass"])
    if useTrigger: 
      cuts["trigger"]         = makeTrigger()
      #cuts["turnon"]   = TCut( "phJetInvMass_puppi_softdrop_W>%f"      % cutValues["minInvMass"]     )

      #cuts["WWindowLow"] = TCut( "WPuppi_softdropJetCorrMass>%f"   % cutValues["WWindow"][0] )
      #cuts["WWindowHi"]  = TCut( "WPuppi_softdropJetCorrMass<%f"   % cutValues["WWindow"][1] )

    return cuts
    
def getPreselectionComboCut(useTrigger=False, sideband=False, windowEdges=[70,90] ):
    preselectionCuts = copy.deepcopy(getDefaultCuts(useTrigger, sideband, windowEdges))
    #         #Included
   # preselectionCuts.pop("phPt")
   # preselectionCuts.pop("phPhi") UNSET
   # preselectionCuts.pop("Tau21") 
   # preselectionCuts.pop("jetPhi") UNSET
   # preselectionCuts.pop("jetEta") UNSET
   # preselectionCuts.pop("cosThetaStar") UNSET
   # preselectionCuts.pop("deltaR")
   # preselectionCuts.pop("jetAbsEta")
   # preselectionCuts.pop("jetPt")
   # preselectionCuts.pop("WWindow")
   # preselectionCuts.pop("phEta")
   # preselectionCuts.pop("phPtOverM")
   # preselectionCuts.pop("WPtOverM")
   # preselectionCuts.pop("turnon")
   # preselectionCuts.pop("jetAbsEta")
    return combineCuts(preselectionCuts)

