from ROOT import *

def getWeightsDict(small3Dir):
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


  sampleEvents = {}
  for key in sampleXsects:
    mcBGfileName = "%s/small3_%s" % (small3Dir, key)
    #print "the small3 input filename is: %s" % mcBGfileName
    mcBGfile = TFile( "%s/small3_%s" % (small3Dir, key) )
    #print mcBGfile
    hCounter = mcBGfile.Get("ntuplizer/hCounter")
    nEvents = hCounter.GetEntries()
    sampleEvents[key]=nEvents;

  lumi = 2700

  sampleWeights = {}
  for key in sampleXsects:
    expectedEvents = lumi*sampleXsects[key]
    weight = expectedEvents/sampleEvents[key]
    sampleWeights[key] = weight

  return sampleWeights


def getSmall3ddTreeDict(ddDir):
  s3dd = {}
  
  s3dd["GJets_HT-100To200.root"    ] = "%s/small3_GJets_HT-100To200_may5.root"%ddDir
  s3dd["GJets_HT-200To400.root"    ] = "%s/small3_GJets_HT-200To400_may5.root"%ddDir
  s3dd["GJets_HT-400To600.root"    ] = "%s/small3_GJets_HT-400To600_may5.root"%ddDir
  s3dd["GJets_HT-600ToInf.root"    ] = "%s/small3_GJets_HT-600ToInf_may5.root"%ddDir
  s3dd["QCD_HT100to200.root"       ] = "%s/small3_QCD_HT100to200_may5.root"%ddDir
  s3dd["QCD_HT200to300.root"       ] = "%s/small3_QCD_HT200to300_may5.root"%ddDir
  s3dd["QCD_HT300to500.root"       ] = "%s/small3_QCD_HT300to500_may5.root"%ddDir
  s3dd["QCD_HT500to700.root"       ] = "%s/small3_QCD_HT500to700_may5.root"%ddDir
  s3dd["QCD_HT700to1000.root"      ] = "%s/small3_QCD_HT700to1000_may5.root"%ddDir
  s3dd["QCD_HT1000to1500.root"     ] = "%s/small3_QCD_HT1000to1500_may5.root"%ddDir
  s3dd["QCD_HT1500to2000.root"     ] = "%s/small3_QCD_HT1500to2000_may5.root"%ddDir
  s3dd["QCD_HT2000toInf.root"      ] = "%s/small3_QCD_HT2000toInf_may5.root"%ddDir
  s3dd["DYJetsToQQ_HT180.root"     ] = "%s/small3_DYJetsToQQ_HT180_may5.root"%ddDir
  s3dd["WJetsToQQ_HT-600ToInf.root"] = "%s/small3_WJetsToQQ_HT-600ToInf_may5.root"%ddDir

  return s3dd
