from ROOT import *

# janky methods for mapping the samples cross sections, the sample's small3 tree, and the sample's treeChecker tree
# John Hakala 5/11/2016

def getDDPrefix():
  return "ddTree_"

def getSmallPrefix():
  return "smallified_"

def getMCbgSampleXsects():
  sampleXsects = {}
  sampleXsects[   "gJets100To200.root"   ]   = 9238*1.8*0.8   
  sampleXsects[   "gJets200To400.root"   ]   = 2305*1.8*0.8   
  sampleXsects[   "gJets400To600.root"   ]   = 274.4*1.4*0.8  
  sampleXsects[   "gJets600ToInf.root"   ]   = 93.46*0.8      
  sampleXsects[   "qcd200to300.root"     ]   = 1712000*0.8    
  sampleXsects[   "qcd300to500.root"     ]   = 347700*0.8     
  sampleXsects[   "qcd500to700.root"     ]   = 32100*0.8      
  sampleXsects[   "qcd700to1000.root"    ]    = 6831*0.8       
  sampleXsects[   "qcd1000to1500.root"   ]    = 1207*0.8       
  sampleXsects[   "qcd1500to2000.root"   ]    = 119.9*0.8      
  sampleXsects[   "qcd2000toInf.root"    ]    = 25.24*0.8      
  sampleXsects[   "DYJetsToQQ180.root"  ]    = 1187*1.23*0.8  
  sampleXsects[   "WJetsToQQ180.root"   ]    = 95.14*1.21*0.8 
  return sampleXsects

def getMCbgSampleEvents(small3Dir):
  sampleXsects=getMCbgSampleXsects()
  sampleEvents = {}
  for key in sampleXsects:
    mcBGfileName = "%s/%s%s" % (small3Dir, getSmallPrefix(), key)
    print "the small3 input filename is: %s" % mcBGfileName
    mcBGfile = TFile( mcBGfileName )
    #print mcBGfile
    hCounter = mcBGfile.Get("ntuplizer/hCounter")
    nEvents = hCounter.GetBinContent(1)
    sampleEvents[key]=nEvents;
  return sampleEvents

def getSignalsToInclude():
  return [  "sig_m750.root",
            "sig_m850.root",
            "sig_m1000.root",
            "sig_m1150.root",
            "sig_m1300.root",
            "sig_m1450.root",
            "sig_m1600.root",
            "sig_m1750.root",
            "sig_m1900.root",
            "sig_m2050.root",
            "sig_m2450.root",
            "sig_m2850.root",
            "sig_m3250.root",
          ]

def getWeightsDict(small3Dir):
  sampleXsects = getMCbgSampleXsects() 
  sampleEvents = getMCbgSampleEvents(small3Dir)

  lumi = 36420

  sampleWeights = {}
  for key in sampleXsects:
    expectedEvents = lumi*sampleXsects[key]
    weight = expectedEvents/sampleEvents[key]
    sampleWeights[key] = weight
  signalWeight = .5
  #for signalToInclude in getSignalsToInclude():
  #  sampleWeights[signalToInclude] = signalWeight
  sampleWeights["SilverJson.root"] = 1
#  sampleWeights[ "sig_m650.root"   ] = .8*10
  sampleWeights[ "sig_m750.root"   ] = .8*10
  sampleWeights[ "sig_m850.root"   ] = .8*10
  sampleWeights[ "sig_m1000.root"  ] = .7*10
  sampleWeights[ "sig_m1150.root"  ] = .7*10
  sampleWeights[ "sig_m1300.root"  ] = .7*10
  sampleWeights[ "sig_m1450.root"  ] = .6*10
  sampleWeights[ "sig_m1600.root"  ] = .6*10
  sampleWeights[ "sig_m1750.root"  ] = .6*10
  sampleWeights[ "sig_m1900.root"  ] = .5*10
  sampleWeights[ "sig_m2050.root"  ] = .5*10
  sampleWeights[ "sig_m2450.root"  ] = .5*10
  sampleWeights[ "sig_m2850.root"  ] = .4*10
  sampleWeights[ "sig_m3250.root"  ] = .4*10
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
    "DYJetsToQQ180.root"   ,
    "WJetsToQQ180.root"    ,
    "qcd2000toInf.root"     ,
    "qcd1500to2000.root"    ,
    "qcd1000to1500.root"    ,
    "qcd700to1000.root"     ,
    "qcd500to700.root"      ,
    "qcd300to500.root"      ,
    "qcd200to300.root"      ,
    "gJets600ToInf.root"    ,
    "gJets400To600.root"    ,
    "gJets200To400.root"    ,
    "gJets100To200.root"   
  ]

def getMCbgColors():
  color = TColor()
  sampleColors = {}
  #sampleColors["QCD_HT100to200.root"       ] = color.GetColor(.1, 0.3, 0.25)
  sampleColors["gJets100To200.root" ] = color.GetColor(.475*1.1, .6*1.2, 1.0)
  sampleColors["gJets200To400.root" ] = color.GetColor(.475, .6, 1.0)
  sampleColors["gJets400To600.root" ] = color.GetColor(.35, .5, 0.85)
  sampleColors["gJets600ToInf.root" ] = color.GetColor(.225, .3, 0.7) 
  sampleColors["qcd200to300.root"   ] = color.GetColor(.31*1.2, 1.0, 0.425*1.2)
  sampleColors["qcd300to500.root"   ] = color.GetColor(.31, .95, 0.425)
  sampleColors["qcd500to700.root"   ] = color.GetColor(.28, .9, 0.4)
  sampleColors["qcd700to1000.root"  ] = color.GetColor(.25, .8, 0.375)
  sampleColors["qcd1000to1500.root" ] = color.GetColor(.22, .7, 0.35)
  sampleColors["qcd1500to2000.root" ] = color.GetColor(.19, .6, 0.325)
  sampleColors["qcd2000toInf.root"  ] = color.GetColor(.16, .5, 0.3)
  sampleColors["DYJetsToQQ180.root"] = color.GetColor(.6, .2, .2)
  sampleColors["WJetsToQQ180.root" ] = color.GetColor(.85, .85, 0.3)
  return sampleColors

def getMCbgLabels():
  color = TColor()
  legendLabels = {}
  legendLabels["gJets100To200" ] = "#gamma#plusjets[100,200]"
  legendLabels["gJets200To400" ] = "#gamma#plusjets[200,400]"
  legendLabels["gJets400To600" ] = "#gamma#plusjets[400,600]"
  legendLabels["gJets600ToInf" ] = "#gamma#plusjets[600,#infty]"
  legendLabels["qcd200to300"   ] = "QCD[200,300]"
  legendLabels["qcd300to500"   ] = "QCD[300,500]"
  legendLabels["qcd500to700"   ] = "QCD[500,700]"
  legendLabels["qcd700to1000"  ] = "QCD[700,1000]"
  legendLabels["qcd1000to1500" ] = "QCD[1000,1500]"
  legendLabels["qcd1500to2000" ] = "QCD[1500,2000]"
  legendLabels["qcd2000toInf"  ] = "QCD[2000,#infty]"
  legendLabels["DYJetsToQQ180"] = "DY#plusjets[180,#infty]"
  legendLabels["WJetsToQQ180" ] = "W#plusjets[600,#infty]"
  #legendLabels["QCD_HT100to200"       ] = "QCD[100,200]"
  return legendLabels

def getSmall3ddTreeDict(ddDir):
  s3dd = {}
  
  #s3dd["QCD_HT100to200.root"       ] = "%s/ddTree_QCD_HT100to200.root"%ddDir
  s3dd["gJets100To200" ] = "%s/ddTree_GJets100-200"  % ddDir
  s3dd["gJets200To400" ] = "%s/ddTree_gJets200To400"  % ddDir
  s3dd["gJets400To600" ] = "%s/ddTree_gJets400To600"  % ddDir
  s3dd["gJets600ToInf" ] = "%s/ddTree_gJets600ToInf"  % ddDir
  s3dd["qcd200to300"   ] = "%s/ddTree_qcd200to300"    % ddDir
  s3dd["qcd300to500"   ] = "%s/ddTree_qcd300to500"    % ddDir
  s3dd["qcd500to700"   ] = "%s/ddTree_qcd500to700"    % ddDir
  s3dd["qcd700to1000"  ] = "%s/ddTree_qcd700to1000"   % ddDir
  s3dd["qcd1000to1500" ] = "%s/ddTree_qcd1000to1500"  % ddDir
  s3dd["qcd1500to2000" ] = "%s/ddTree_qcd1500to2000"  % ddDir
  s3dd["qcd2000toInf"  ] = "%s/ddTree_qcd2000toInf"   % ddDir
  s3dd["DYJetsToQQ180"] = "%s/ddTree_DYJetsToQQ180" % ddDir
  s3dd["WJetsToQQ180" ] = "%s/ddTree_WJetsToQQ180"  % ddDir

  return s3dd
