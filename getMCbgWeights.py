from ROOT import *

def getWeightsDict():
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
    mcBGfile = TFile("inputs/small3_%s"%key)
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
