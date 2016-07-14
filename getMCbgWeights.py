from ROOT import *

# janky methods for mapping the samples cross sections, the sample's small3 tree, and the sample's treeChecker tree
# John Hakala 5/11/2016

def getFilePrefix():
  return "newerDD_"

def getMCbgSampleXsects():
  sampleXsects = {}
  sampleXsects["GJets_HT-100To200.root"    ] = 9238*1.8
  sampleXsects["GJets_HT-200To400.root"    ] = 2305*1.8
  sampleXsects["GJets_HT-400To600.root"    ] = 274.4*1.4
  sampleXsects["GJets_HT-600ToInf.root"    ] = 93.46
  sampleXsects["QCD_HT100to200.root"       ] = 27990000
  sampleXsects["QCD_HT200to300.root"       ] = 1712000
  sampleXsects["QCD_HT300to500.root"       ] = 347700
  sampleXsects["QCD_HT500to700.root"       ] = 32100
  sampleXsects["QCD_HT700to1000.root"      ] = 6831
  sampleXsects["QCD_HT1000to1500.root"     ] = 1207
  sampleXsects["QCD_HT1500to2000.root"     ] = 119.9
  sampleXsects["QCD_HT2000toInf.root"      ] = 25.24
  sampleXsects["DYJetsToQQ_HT180.root"     ] = 1187*1.23
  sampleXsects["WJetsToQQ_HT-600ToInf.root"] = 95.14*1.21
  return sampleXsects

def getMCbgSampleEvents(small3Dir):
  sampleXsects=getMCbgSampleXsects()
  sampleEvents = {}
  for key in sampleXsects:
    mcBGfileName = "%s/small3_%s" % (small3Dir, key)
    #print "the small3 input filename is: %s" % mcBGfileName
    mcBGfile = TFile( "%s/small3_%s" % (small3Dir, key) )
    #print mcBGfile
    hCounter = mcBGfile.Get("ntuplizer/hCounter")
    nEvents = hCounter.GetEntries()
    sampleEvents[key]=nEvents;
  return sampleEvents

def getSignalsToInclude():
  return ["Hgamma_m750.root", "Hgamma_m1000.root", "Hgamma_m2000.root", "Hgamma_m3000.root"]

def getWeightsDict(small3Dir):
  sampleXsects = getMCbgSampleXsects() 
  sampleEvents = getMCbgSampleEvents(small3Dir)

  lumi = 2700

  sampleWeights = {}
  for key in sampleXsects:
    expectedEvents = lumi*sampleXsects[key]
    weight = expectedEvents/sampleEvents[key]
    sampleWeights[key] = weight
  signalWeight = .5
  for signalToInclude in getSignalsToInclude():
    sampleWeights[signalToInclude] = signalWeight
  sampleWeights["SilverJson.root"] = 1

  return sampleWeights

def getMCbgWeightsDict(small3Dir):
 weights = getWeightsDict(small3Dir) 
 nonMCbgs = getSignalsToInclude()
 nonMCbgs.append("SilverJson.root")
 for nonMCbg in nonMCbgs:
   weights.pop(nonMCbg)
 return weights


def getSmall3ddTreeDict(ddDir):
  s3dd = {}
  
  s3dd["GJets_HT-100To200.root"    ] = "%s/newerDD_GJets_HT-100To200.root"%ddDir
  s3dd["GJets_HT-200To400.root"    ] = "%s/newerDD_GJets_HT-200To400.root"%ddDir
  s3dd["GJets_HT-400To600.root"    ] = "%s/newerDD_GJets_HT-400To600.root"%ddDir
  s3dd["GJets_HT-600ToInf.root"    ] = "%s/newerDD_GJets_HT-600ToInf.root"%ddDir
  s3dd["QCD_HT100to200.root"       ] = "%s/newerDD_QCD_HT100to200.root"%ddDir
  s3dd["QCD_HT200to300.root"       ] = "%s/newerDD_QCD_HT200to300.root"%ddDir
  s3dd["QCD_HT300to500.root"       ] = "%s/newerDD_QCD_HT300to500.root"%ddDir
  s3dd["QCD_HT500to700.root"       ] = "%s/newerDD_QCD_HT500to700.root"%ddDir
  s3dd["QCD_HT700to1000.root"      ] = "%s/newerDD_QCD_HT700to1000.root"%ddDir
  s3dd["QCD_HT1000to1500.root"     ] = "%s/newerDD_QCD_HT1000to1500.root"%ddDir
  s3dd["QCD_HT1500to2000.root"     ] = "%s/newerDD_QCD_HT1500to2000.root"%ddDir
  s3dd["QCD_HT2000toInf.root"      ] = "%s/newerDD_QCD_HT2000toInf.root"%ddDir
  s3dd["DYJetsToQQ_HT180.root"     ] = "%s/newerDD_DYJetsToQQ_HT180.root"%ddDir
  s3dd["WJetsToQQ_HT-600ToInf.root"] = "%s/newerDD_WJetsToQQ_HT-600ToInf.root"%ddDir

  return s3dd
