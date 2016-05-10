from math import sqrt
from ROOT import *
from pyrootTools import instance
from getMCbgWeights import getWeightsDict, getSmall3ddTreeDict

dataOrMCbg = "MC"
small3sDir = "~/physics/small3s"
ddDir = "~/physics/may5_btagging"
inSampleFile = "~/physics/may5_btagging/small3_SilverJson_may5.root"

def calcSoverRootB(sampleFile, mass, masswindow, workingPoint, compileOrLoad):

  sigWindowTreeName = "higgs"  # just keep the name from TTree::MakeClass(), don't give it a special name
  instance("%s_csv"%sigWindowTreeName, compileOrLoad)
  
  bgFileName = sampleFile
  bgFile = TFile(bgFileName)
  sigWindowBgTree = bgFile.Get(sigWindowTreeName)
  #print sigWindowBgTree
  sigWindowBg = higgs_csv(sigWindowBgTree)
  
  lowerMassBound = masswindow[0]
  upperMassBound = masswindow[1]
  #print "    For Hbb working point %f:" % cutValue
  nSignalWindowEventsInBkg = sigWindowBg.Loop(workingPoint, lowerMassBound, upperMassBound)
  #print "      Number of signal window events in background is: %i" % nSignalWindowEventsInBkg
  
  mcSigFileName = "~/physics/may5_Hgamma_btagging/Hgamma_m%s_may5.root"%mass
  mcSigFile = TFile(mcSigFileName)
  sigWindowMCsigTree = mcSigFile.Get(sigWindowTreeName)
  sigWindowMCsig = higgs_csv(sigWindowMCsigTree)
  nSignalWindowEventsInMCsig = sigWindowMCsig.Loop(workingPoint, lowerMassBound, upperMassBound)
  #print "      Number of signal window events in signal MC is: %i" % nSignalWindowEventsInMCsig

  if not nSignalWindowEventsInBkg==0:
    sOverRootB = nSignalWindowEventsInMCsig/sqrt(nSignalWindowEventsInBkg)
  elif nSignalWindowEventsInBkg==0:
    sOverRootB = "%i / sqrt(0)" % nSignalWindowEventsInMCsig
  else:
    print "something's screwy!"
    exit(1)
  response = {}
  response["S"] = nSignalWindowEventsInMCsig
  response["B"] = nSignalWindowEventsInBkg
  response["SoverRootB"] = sOverRootB
  return response

def fillHist(hist, dataOrMCbg, mass, masswindow, compileOrLoad):
  normalizations = {}
  normalizations["750"] = 1
  normalizations["1000"] = .8
  normalizations["2000"] = .1
  normalizations["3000"] = .1
  if not (dataOrMCbg == "data" or dataOrMCbg == "MC"):
    exit("Please pick either 'data' or 'MC' for the background")
  binMap = {}
  binMap["looseloose"]=[1,1]
  binMap["mediumloose"]=[2,1]
  binMap["tightloose"]=[3,1]
  binMap["mediummedium"]=[2,2]
  binMap["tightmedium"]=[3,2]
  binMap["tighttight"]=[3,3]
  for workingPoint in binMap.keys() :
    if dataOrMCbg == "data":
      sOverRootB = calcSoverRootB(inSampleFile, mass, masswindow, workingPoint, compileOrLoad)["SoverRootB"]
      #print "      S/sqrt(B) is %s" % str(sOverRootB)
      if (isinstance(sOverRootB, float)):
        hist.SetBinContent(binMap[workingPoint][0], binMap[workingPoint][1], sOverRootB)
      compileOrLoad = "load"
    elif dataOrMCbg == "MC":
      weightsDict = getWeightsDict(small3sDir)
      #print "the weights dictionary is:"
      #print weightsDict
      small3ddDict = getSmall3ddTreeDict(ddDir)
      sTotal = 0
      bTotal = 0
      for mcBgFile in weightsDict.keys():
        unweightedSoverRootBinfo = calcSoverRootB(small3ddDict[mcBgFile], mass, masswindow, workingPoint, compileOrLoad)
        #print "S for %s is: %s" % (mcBgFile, str(unweightedSoverRootBinfo["S"]))
        sTotal = unweightedSoverRootBinfo["S"]
        #print "unweighted B for %s is: %s" % (mcBgFile, str(unweightedSoverRootBinfo["B"]))
        #print "weight is %s" % str(weightsDict[mcBgFile])
        bTotal += float(unweightedSoverRootBinfo["B"]) * weightsDict[mcBgFile]
        compileOrLoad="load"
      #print "total B is: %f" % bTotal
      print "   working point: %s has = %f, b=%f" % (workingPoint, float(sTotal), float(bTotal))
      if not bTotal == 0:
        sOverRootB = sTotal / sqrt(bTotal)
        print "      S/root(B) is: %f" % sOverRootB
        #graph.SetPoint(graph.GetN(), cutValue, normalizations[mass]*sOverRootB)

        hist.SetBinContent(binMap[workingPoint][0], binMap[workingPoint][1], normalizations[mass]*sOverRootB)
      



#graphs = []
hists = []
compileOrLoad = "compile" # just compile the first time
for mass in [750, 1000, 2000, 3000]:
  if mass == 750:
    masswindow = [700, 800]
  elif mass == 1000:
    masswindow = [900, 1100]
  elif mass == 2000:
    masswindow = [1850, 2150]
  elif mass == 3000:
    masswindow = [2200, 4000]
  hists.append(TH2I("M=%i"%mass, "M=%i"%mass, 3, 0, 3, 3, 0, 3))

  #print "Signal mass %f" % mass
  print "For mass %i:" % mass
  fillHist(hists[-1], dataOrMCbg, str(mass), masswindow, compileOrLoad)
  compileOrLoad = "load"

canvases = []
x=0
gStyle.SetPalette(kRainBow)
for hist in hists:
  hist.SetContour(1000)
  canvases.append(TCanvas())
  canvases[-1].cd()
  hist.Draw("COLZ")
