from math import sqrt
from ROOT import *
from pyrootTools import instance
from getMCbgWeights import getWeightsDict, getSmall3ddTreeDict

dataOrMCbg = "MC"
small3sDir = "~/physics/small3s"
ddDir = "~/physics/may5_btagging"
inSampleFile = "~/physics/may5_btagging/small3_SilverJson_may5.root"

def calcSoverRootB(sampleFile, mass, masswindow, cutValue, compileOrLoad):

  sigWindowTreeName = "higgs"  # just keep the name from TTree::MakeClass(), don't give it a special name
  instance(sigWindowTreeName, compileOrLoad)
  
  bgFileName = sampleFile
  bgFile = TFile(bgFileName)
  sigWindowBgTree = bgFile.Get(sigWindowTreeName)
  #print sigWindowBgTree
  sigWindowBg = higgs(sigWindowBgTree)
  
  lowerMassBound = masswindow[0]
  upperMassBound = masswindow[1]
  #print "    For Hbb working point %f:" % cutValue
  nSignalWindowEventsInBkg = sigWindowBg.Loop(cutValue, lowerMassBound, upperMassBound)
  #print "      Number of signal window events in background is: %i" % nSignalWindowEventsInBkg
  
  mcSigFileName = "~/physics/may5_Hgamma_btagging/Hgamma_m%s_may5.root"%mass
  mcSigFile = TFile(mcSigFileName)
  sigWindowMCsigTree = mcSigFile.Get(sigWindowTreeName)
  sigWindowMCsig = higgs(sigWindowMCsigTree)
  nSignalWindowEventsInMCsig = sigWindowMCsig.Loop(cutValue, lowerMassBound, upperMassBound)
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

def fillGraph(graph, dataOrMCbg, mass, masswindow, compileOrLoad):
  normalizations = {}
  normalizations["750"] = 1
  normalizations["1000"] = .8
  normalizations["2000"] = .1
  normalizations["3000"] = .1
  if not (dataOrMCbg == "data" or dataOrMCbg == "MC"):
    exit("Please pick either 'data' or 'MC' for the background")
  for i in range(-10, 110):
    cutValue = i/float(100)
    if dataOrMCbg == "data":
      sOverRootB = calcSoverRootB(inSampleFile, mass, masswindow, cutValue, compileOrLoad)["SoverRootB"]
      #print "      S/sqrt(B) is %s" % str(sOverRootB)
      if (isinstance(sOverRootB, float)):
        graph.SetPoint(graph.GetN(), cutValue, sOverRootB)
      compileOrLoad = "load"
    elif dataOrMCbg == "MC":
      weightsDict = getWeightsDict(small3sDir)
      #print "the weights dictionary is:"
      #print weightsDict
      small3ddDict = getSmall3ddTreeDict(ddDir)
      sTotal = 0
      bTotal = 0
      for mcBgFile in weightsDict.keys():
        unweightedSoverRootBinfo = calcSoverRootB(small3ddDict[mcBgFile], mass, masswindow, cutValue, compileOrLoad)
        #print "S for %s is: %s" % (mcBgFile, str(unweightedSoverRootBinfo["S"]))
        sTotal = unweightedSoverRootBinfo["S"]
        #print "unweighted B for %s is: %s" % (mcBgFile, str(unweightedSoverRootBinfo["B"]))
        #print "weight is %s" % str(weightsDict[mcBgFile])
        bTotal += float(unweightedSoverRootBinfo["B"]) * weightsDict[mcBgFile]
        compileOrLoad="load"
      #print "total B is: %f" % bTotal
      if not bTotal == 0:
        sOverRootB = sTotal / sqrt(bTotal)
        graph.SetPoint(graph.GetN(), cutValue, normalizations[mass]*sOverRootB)
      



graphs = []
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
  graphs.append(TGraph())
  #print "Signal mass %f" % mass
  fillGraph(graphs[-1], dataOrMCbg, str(mass), masswindow, compileOrLoad)
  compileOrLoad = "load"

canvas = TCanvas()
canvas.cd()
option = ""
x=0
for graph in graphs:
  graph.Draw(option)
  graph.SetLineColor(kRed+x)
  x += 1
  option = "SAME"


