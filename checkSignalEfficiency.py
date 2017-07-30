from ROOT import *
from HgParameters import *
from HgCuts import *
from pyrootTools import *
import copy
# macro for rechecking signal efficiencies for H(bb)gamma
# John Hakala, 7/13/16

def getSignalEfficiencies(massWindowToCheck):
  debugFlag = False

  samplesDirs = getSamplesDirs()
  cutValues = getCutValues()
  cutsDict = getDefaultCuts("higgs", False, False, [0.,0.])

  instance("higgs", "compile")

  efficiencies = {}

  sigDDs = {}
  higgsTrees = {}

  # create a dict of dd trees by masses
  masses = getNormalizations().keys()
  print "calculating efficiencies for masses:", masses
  for mass in masses:
    sigDDs[mass] = TFile("%s/ddTree_sig_m%s.root" % (samplesDirs["sigDDdir"], mass))
    higgsTrees[mass] = sigDDs[mass].Get("higgs")
    print "higgsTrees:"
    print higgsTrees

  # loop over all the masses
  for key in higgsTrees.keys():
    higgsCounter = higgs(higgsTrees[key])
    # check with no masswindow applied
    nEntriesWithBtag = higgsCounter.Loop("btag", cutValues["Hbb"], cutValues["ptOverM"], cutValues["deltaR"], cutValues["jetAbsEta"], cutValues["phEta"])
    nEntriesNoBtag = higgsCounter.Loop("nobtag", cutValues["Hbb"], cutValues["ptOverM"], cutValues["deltaR"], cutValues["jetAbsEta"], cutValues["phEta"])
    btagEfficiency = nEntriesWithBtag/float(nEntriesNoBtag)
    totalEfficiency = nEntriesWithBtag/float(getSigNevents()[str(mass)])
    thisMassEff     = {}
    if debugFlag:
      print "No higgs mass window cut:"
      print "   sample mass %s has number of entries with btagging %i" % (key, nEntriesWithBtag)
      print "   sample mass %s has number of events with no btagging: %i" % (key, nEntriesNoBtag)
      print "   N-1 btagging efficiency is: %f" % btagEfficiency
      print "   total signal efficiency is: %f" % totalEfficiency

    # check with masswindows
    for masswindow in [[110, 140], [90, 150], [95,145], [100,140]]:
      # higgsCounter: higgs::Loop(float HbbCutValue, float pToverMcutValue, float deltaRcutValue, float jetEtaCutValue, float phoEtaCutValue, float lowerMassBound, float upperMassBound)
      nEntriesWithBtag = higgsCounter.Loop("btag", cutValues["Hbb"], cutValues["ptOverM"], cutValues["deltaR"], cutValues["jetAbsEta"], cutValues["phEta"], masswindow[0], masswindow[1])
      nEntriesWithAntiBtag = higgsCounter.Loop("antibtag", cutValues["Hbb"], cutValues["ptOverM"], cutValues["deltaR"], cutValues["jetAbsEta"], cutValues["phEta"], masswindow[0], masswindow[1])
      nEntriesNoBtag = higgsCounter.Loop("nobtag", cutValues["Hbb"], cutValues["ptOverM"], cutValues["deltaR"], cutValues["jetAbsEta"], cutValues["phEta"], masswindow[0], masswindow[1])
      btagEfficiency = nEntriesWithBtag/float(nEntriesNoBtag)
      antiBtagEfficiency = nEntriesWithAntiBtag/float(nEntriesNoBtag)

      print "nEntriesNoBtag:", nEntriesNoBtag, "getSigNevents()[str(%s)]"%mass, getSigNevents()[str(mass)]
      noBtagEfficiency = nEntriesNoBtag/float(getSigNevents()[str(mass)])
      thisMassEff["nobtag"] = noBtagEfficiency

      totalBtagEfficiency = nEntriesWithBtag/float(getSigNevents()[str(mass)])
      thisMassEff["btag"] = totalBtagEfficiency

      totalAntiBtagEfficiency = nEntriesWithAntiBtag/float(getSigNevents()[str(mass)])
      thisMassEff["antibtag"] = totalAntiBtagEfficiency
      
      if masswindow[0]==massWindowToCheck[0] and masswindow[1]==massWindowToCheck[1]:
        print "writing efficiencies for massWindowToCheck = (%f, %f)" % ( massWindowToCheck[0], massWindowToCheck[1])
        efficiencies[key]=copy.deepcopy(thisMassEff)
      
      if debugFlag:
        print "With higgs mass window cut [%f, %f]:"%(masswindow[0], masswindow[1])
        print "   sample mass %s has number of entries with btagging %i" % (key, nEntriesWithBtag)
        print "   sample mass %s has number of entries with antibtagging %i" % (key, nEntriesWithAntiBtag)
        print "   sample mass %s has number of events with no btagging: %i" % (key, nEntriesNoBtag)
        print "   N-1 btagging efficiency is: %f" % btagEfficiency
        print "   N-1 antibtagging efficiency is: %f" % antiBtagEfficiency
        print "" 
        print "   efficiency with no btagging is: %f" % noBtagEfficiency
        print "   total btagged category signal efficiency is: %f" % totalBtagEfficiency
        print "   total anti-btagged category signal efficiency is: %f" % totalAntiBtagEfficiency
  print efficiencies
  return efficiencies
      
