from ROOT import *
from HgParameters import *
from HgCuts import *
from pyrootTools import *

samplesDirs = getSamplesDirs()
cutsDict = getDefaultCuts("higgs")
for cut in cutsDict.keys():
  print "cut: ", 
  print cut,
  print " value: ", 
  print cutsDict[cut]

instance("higgs", "compile")

efficiencies = {}

sigDDs = {}
higgsTrees = {}
for mass in getNormalizations().keys():
  sigDDs[mass] = TFile("%s/newerDD_Hgamma_m%s.root" % (samplesDirs["ddDir"], mass))
  higgsTrees[mass] = sigDDs[mass].Get("higgs")

for key in higgsTrees.keys():
  higgsCounter = higgs(higgsTrees[key])
  print "No higgs mass window cut:"
  nEntriesWithBtag = higgsCounter.Loop("btag", 0.9, 0.35, 1.1, 2.4, 1.4442)
  print "   sample mass %s has number of entries with btagging %i" % (key, nEntriesWithBtag)
  nEntriesNoBtag = higgsCounter.Loop("nobtag", 0.9, 0.35, 1.1, 2.4, 1.4442)
  print "   sample mass %s has number of events with no btagging: %i" % (key, nEntriesNoBtag)
  btagEfficiency = nEntriesWithBtag/float(nEntriesNoBtag)
  print "   N-1 btagging efficiency is: %f" % btagEfficiency
  totalEfficiency = nEntriesWithBtag/float(getSigNevents()[str(mass)])
  print "   total signal efficiency is: %f" % totalEfficiency
  for masswindow in [[110, 140], [90, 150], [95,145], [100,140]]:
    # higgsCounter: higgs::Loop(float HbbCutValue, float pToverMcutValue, float deltaRcutValue, float jetEtaCutValue, float phoEtaCutValue, float lowerMassBound, float upperMassBound)
    print "With higgs mass window cut [%f, %f]:"%(masswindow[0], masswindow[1])
    nEntriesWithBtag = higgsCounter.Loop("btag", 0.9, 0.35, 1.1, 2.4, 1.4442, masswindow[0], masswindow[1])
    print "   sample mass %s has number of entries with btagging %i" % (key, nEntriesWithBtag)
    nEntriesNoBtag = higgsCounter.Loop("nobtag", 0.9, 0.35, 1.1, 2.4, 1.4442, masswindow[0], masswindow[1])
    print "   sample mass %s has number of events with no btagging: %i" % (key, nEntriesNoBtag)
    btagEfficiency = nEntriesWithBtag/float(nEntriesNoBtag)
    print "   N-1 btagging efficiency is: %f" % btagEfficiency
    totalEfficiency = nEntriesWithBtag/float(getSigNevents()[str(mass)])
    print "   total signal efficiency is: %f" % totalEfficiency
    
    
