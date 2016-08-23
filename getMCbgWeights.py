from ROOT import *

# janky methods for mapping the samples cross sections, the sample's small3 tree, and the sample's treeChecker tree
# John Hakala 5/11/2016

def getFilePrefix():
  return "ddTree_"

def getMCbgSampleXsects():
  sampleXsects = {}
  #sampleXsects["GJets_HT-100To200.root"    ] = 9238*1.8
  sampleXsects["GJets_HT-100To200.root"    ] = 9238*1.8*0.8
  # sampleXsects["GJets_HT-200To400.root"    ] = 2305*1.8
  sampleXsects["GJets_HT-200To400.root"    ] = 2305*1.8*0.8
  # sampleXsects["GJets_HT-400To600.root"    ] = 274.4*1.4
  sampleXsects["GJets_HT-400To600.root"    ] = 274.4*1.4*0.8
  sampleXsects["GJets_HT-600ToInf.root"    ] = 93.46*0.8
  sampleXsects["QCD_HT100to200.root"       ] = 27990000*0.8
  sampleXsects["QCD_HT200to300.root"       ] = 1712000*0.8
  sampleXsects["QCD_HT300to500.root"       ] = 347700*0.8
  sampleXsects["QCD_HT500to700.root"       ] = 32100*0.8
  sampleXsects["QCD_HT700to1000.root"      ] = 6831*0.8
  sampleXsects["QCD_HT1000to1500.root"     ] = 1207*0.8
  sampleXsects["QCD_HT1500to2000.root"     ] = 119.9*0.8
  sampleXsects["QCD_HT2000toInf.root"      ] = 25.24*0.8
  sampleXsects["DYJetsToQQ_HT180.root"     ] = 1187*1.23*0.8
  sampleXsects["WJetsToQQ_HT-600ToInf.root"] = 95.14*1.21*0.8
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
  return [  "Hgamma_m650.root",
            "Hgamma_m750.root",
            "Hgamma_m1000.root",
            "Hgamma_m1250.root",
            "Hgamma_m1500.root",
            "Hgamma_m1750.root",
            "Hgamma_m2000.root",
            "Hgamma_m2500.root",
            "Hgamma_m3000.root",
            "Hgamma_m3500.root",
            "Hgamma_m4000.root"
          ]

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
  sampleWeights["Hgamma_m650.root"] = .8
  sampleWeights["Hgamma_m750.root"] = .8
  sampleWeights["Hgamma_m1000.root"] = .8
  sampleWeights["Hgamma_m1250.root"] = .8
  sampleWeights["Hgamma_m1500.root"] = .8
  sampleWeights["Hgamma_m1750.root"] = .8
  sampleWeights["Hgamma_m2000.root"] = .8
  sampleWeights["Hgamma_m2500.root"] = .8
  sampleWeights["Hgamma_m3000.root"] = .8
  sampleWeights["Hgamma_m3500.root"] = .8
  sampleWeights["Hgamma_m4000.root"] = .8
  return sampleWeights

def getMCbgWeightsDict(small3Dir):
 weights = getWeightsDict(small3Dir) 
 nonMCbgs = getSignalsToInclude()
 nonMCbgs.append("SilverJson.root")
 for nonMCbg in nonMCbgs:
   weights.pop(nonMCbg)
 return weights

def getMCbgOrderedList():
  return [ 
    "WJetsToQQ_HT-600ToInf.root",
    "DYJetsToQQ_HT180.root"     ,
    "QCD_HT2000toInf.root"      ,
    "QCD_HT1500to2000.root"     ,
    "QCD_HT1000to1500.root"     ,
    "QCD_HT700to1000.root"      ,
    "QCD_HT500to700.root"       ,
    "QCD_HT300to500.root"       ,
    "QCD_HT200to300.root"       ,
    "QCD_HT100to200.root"       ,
    "GJets_HT-600ToInf.root"    ,
    "GJets_HT-400To600.root"    ,
    "GJets_HT-200To400.root"    ,
    "GJets_HT-100To200.root"    
  ]

def getMCbgColors():
  color = TColor()
  sampleColors = {}
  sampleColors["GJets_HT-100To200.root"    ] = color.GetColor(.1, .1, 0.55) 
  sampleColors["GJets_HT-200To400.root"    ] = color.GetColor(.225, .3, 0.7)
  sampleColors["GJets_HT-400To600.root"    ] = color.GetColor(.35, .5, 0.85)
  sampleColors["GJets_HT-600ToInf.root"    ] = color.GetColor(.475, .6, 1.0)
  sampleColors["QCD_HT100to200.root"       ] = color.GetColor(.1, 0.3, 0.25)
  sampleColors["QCD_HT200to300.root"       ] = color.GetColor(.13, .4, 0.275)
  sampleColors["QCD_HT300to500.root"       ] = color.GetColor(.16, .5, 0.3)
  sampleColors["QCD_HT500to700.root"       ] = color.GetColor(.19, .6, 0.325)
  sampleColors["QCD_HT700to1000.root"      ] = color.GetColor(.22, .7, 0.35)
  sampleColors["QCD_HT1000to1500.root"     ] = color.GetColor(.25, .8, 0.375)
  sampleColors["QCD_HT1500to2000.root"     ] = color.GetColor(.28, .9, 0.4)
  sampleColors["QCD_HT2000toInf.root"      ] = color.GetColor(.31, .95, 0.425)
  sampleColors["DYJetsToQQ_HT180.root"     ] = color.GetColor(.6, .2, .2)
  sampleColors["WJetsToQQ_HT-600ToInf.root"] = color.GetColor(.85, .85, 0.3)
  return sampleColors

def getMCbgLabels():
  color = TColor()
  legendLabels = {}
  legendLabels["GJets_HT-100To200"    ] = "#gamma#plusjets[100,200]"
  legendLabels["GJets_HT-200To400"    ] = "#gamma#plusjets[200,400]"
  legendLabels["GJets_HT-400To600"    ] = "#gamma#plusjets[400,600]"
  legendLabels["GJets_HT-600ToInf"    ] = "#gamma#plusjets[600,#infty]"
  legendLabels["QCD_HT100to200"       ] = "QCD[100,200]"
  legendLabels["QCD_HT200to300"       ] = "QCD[200,300]"
  legendLabels["QCD_HT300to500"       ] = "QCD[300,500]"
  legendLabels["QCD_HT500to700"       ] = "QCD[500,700]"
  legendLabels["QCD_HT700to1000"      ] = "QCD[700,1000]"
  legendLabels["QCD_HT1000to1500"     ] = "QCD[1000,1500]"
  legendLabels["QCD_HT1500to2000"     ] = "QCD[1500,2000]"
  legendLabels["QCD_HT2000toInf"      ] = "QCD[2000,#infty]"
  legendLabels["DYJetsToQQ_HT180"     ] = "DY#plusjets[180,#infty]"
  legendLabels["WJetsToQQ_HT-600ToInf"] = "W#plusjets[600,#infty]"
  return legendLabels

def getSmall3ddTreeDict(ddDir):
  s3dd = {}
  
  s3dd["GJets_HT-100To200.root"    ] = "%s/ddTree_GJets_HT-100To200.root"%ddDir
  s3dd["GJets_HT-200To400.root"    ] = "%s/ddTree_GJets_HT-200To400.root"%ddDir
  s3dd["GJets_HT-400To600.root"    ] = "%s/ddTree_GJets_HT-400To600.root"%ddDir
  s3dd["GJets_HT-600ToInf.root"    ] = "%s/ddTree_GJets_HT-600ToInf.root"%ddDir
  s3dd["QCD_HT100to200.root"       ] = "%s/ddTree_QCD_HT100to200.root"%ddDir
  s3dd["QCD_HT200to300.root"       ] = "%s/ddTree_QCD_HT200to300.root"%ddDir
  s3dd["QCD_HT300to500.root"       ] = "%s/ddTree_QCD_HT300to500.root"%ddDir
  s3dd["QCD_HT500to700.root"       ] = "%s/ddTree_QCD_HT500to700.root"%ddDir
  s3dd["QCD_HT700to1000.root"      ] = "%s/ddTree_QCD_HT700to1000.root"%ddDir
  s3dd["QCD_HT1000to1500.root"     ] = "%s/ddTree_QCD_HT1000to1500.root"%ddDir
  s3dd["QCD_HT1500to2000.root"     ] = "%s/ddTree_QCD_HT1500to2000.root"%ddDir
  s3dd["QCD_HT2000toInf.root"      ] = "%s/ddTree_QCD_HT2000toInf.root"%ddDir
  s3dd["DYJetsToQQ_HT180.root"     ] = "%s/ddTree_DYJetsToQQ_HT180.root"%ddDir
  s3dd["WJetsToQQ_HT-600ToInf.root"] = "%s/ddTree_WJetsToQQ_HT-600ToInf.root"%ddDir

  return s3dd
