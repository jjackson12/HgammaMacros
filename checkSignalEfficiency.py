from ROOT import *
from HgParameters import *
from HgCuts import *
from pyrootTools import *
# macro for rechecking signal efficiencies for H(bb)gamma
# John Hakala, 7/13/16

samplesDirs = getSamplesDirs()
cutValues = getCutValues()
cutsDict = getDefaultCuts("higgs")
for cut in cutsDict.keys():
  print "cut: ", 
  print cut,
  print " value: ", 
  print cutsDict[cut]

instance("higgs", "compile")

efficiencies110140 = {}

sigDDs = {}
higgsTrees = {}

# create a dict of dd trees by masses
for mass in getNormalizations().keys():
  sigDDs[mass] = TFile("%s/newerDD_Hgamma_m%s.root" % (samplesDirs["ddDir"], mass))
  higgsTrees[mass] = sigDDs[mass].Get("higgs")

# loop over all the masses
for key in higgsTrees.keys():
  higgsCounter = higgs(higgsTrees[key])
  # check with no masswindow applied
  print "No higgs mass window cut:"
  nEntriesWithBtag = higgsCounter.Loop("btag", cutValues["Hbb"], cutValues["ptOverM"], cutValues["deltaR"], cutValues["jetEta"], cutValues["phEta"])
  print "   sample mass %s has number of entries with btagging %i" % (key, nEntriesWithBtag)
  nEntriesNoBtag = higgsCounter.Loop("nobtag", 0.9, 0.35, 1.1, 2.4, 1.4442)
  print "   sample mass %s has number of events with no btagging: %i" % (key, nEntriesNoBtag)
  btagEfficiency = nEntriesWithBtag/float(nEntriesNoBtag)
  print "   N-1 btagging efficiency is: %f" % btagEfficiency
  totalEfficiency = nEntriesWithBtag/float(getSigNevents()[str(mass)])
  print "   total signal efficiency is: %f" % totalEfficiency

  # check with masswindows
  for masswindow in [[110, 140], [90, 150], [95,145], [100,140]]:
    # higgsCounter: higgs::Loop(float HbbCutValue, float pToverMcutValue, float deltaRcutValue, float jetEtaCutValue, float phoEtaCutValue, float lowerMassBound, float upperMassBound)
    print "With higgs mass window cut [%f, %f]:"%(masswindow[0], masswindow[1])
    nEntriesWithBtag = higgsCounter.Loop("btag", cutValues["Hbb"], cutValues["ptOverM"], cutValues["deltaR"], cutValues["jetEta"], cutValues["phEta"], masswindow[0], masswindow[1])
    print "   sample mass %s has number of entries with btagging %i" % (key, nEntriesWithBtag)
    nEntriesWithAntiBtag = higgsCounter.Loop("antibtag", cutValues["Hbb"], cutValues["ptOverM"], cutValues["deltaR"], cutValues["jetEta"], cutValues["phEta"], masswindow[0], masswindow[1])
    print "   sample mass %s has number of entries with antibtagging %i" % (key, nEntriesWithAntiBtag)
    nEntriesNoBtag = higgsCounter.Loop("nobtag", cutValues["Hbb"], cutValues["ptOverM"], cutValues["deltaR"], cutValues["jetEta"], cutValues["phEta"], masswindow[0], masswindow[1])
    print "   sample mass %s has number of events with no btagging: %i" % (key, nEntriesNoBtag)
    btagEfficiency = nEntriesWithBtag/float(nEntriesNoBtag)
    print "   N-1 btagging efficiency is: %f" % btagEfficiency
    antiBtagEfficiency = nEntriesWithAntiBtag/float(nEntriesNoBtag)
    print "   N-1 antibtagging efficiency is: %f" % antiBtagEfficiency
    totalBtagEfficiency = nEntriesWithBtag/float(getSigNevents()[str(mass)])
    print "   total btagged category signal efficiency is: %f" % totalBtagEfficiency
    totalAntiBtagEfficiency = nEntriesWithAntiBtag/float(getSigNevents()[str(mass)])
    print "   total anti-btagged category signal efficiency is: %f" % totalAntiBtagEfficiency
    
    
