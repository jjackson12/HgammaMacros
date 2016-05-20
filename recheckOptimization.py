from math import sqrt
from ROOT import *
from pyrootTools import instance
from getMCbgWeights import getWeightsDict, getSmall3ddTreeDict
from HgParameters import getNormalizations, getMassWindows, getSamplesDirs

# Methods for finding optimal cuts - here focusing on the Hbb tagger - using the treeChecker trees.
# The bottom methods focus on S/root(B) as the figure of merit.
# There are other scripts that use some of the top methods here but focus on an expected CL95 limit as the figure of merit.
# John Hakala, 5/11/2016

dataOrMCbg = "MC"
samplesDirs = getSamplesDirs()
small3sDir = samplesDirs["small3sDir"]
ddDir = samplesDirs["ddDir"]
inSampleFile = samplesDirs["dataDir"]

def calcSoverRootB(sampleFile, mass, masswindow, HbbCutValue, cosThetaCutValue, pToverMcutValue, compileOrLoad):

  sigWindowTreeName = "higgs"  # just keep the name from TTree::MakeClass(), don't give it a special name
  instance(sigWindowTreeName, compileOrLoad)
  
  bgFileName = sampleFile
  bgFile = TFile(bgFileName)
  sigWindowBgTree = bgFile.Get(sigWindowTreeName)
  #print sigWindowBgTree
  sigWindowBg = higgs(sigWindowBgTree)
  
  lowerMassBound = masswindow[0]
  upperMassBound = masswindow[1]
  #print "    For Hbb working point %f:" % HbbCutValue
  nSignalWindowEventsInBkg = sigWindowBg.Loop(HbbCutValue, cosThetaCutValue, pToverMcutValue, lowerMassBound, upperMassBound)
  #print "      Number of signal window events in background is: %i" % nSignalWindowEventsInBkg
  
  mcSigFileName = "~/physics/may5_Hgamma_btagging/Hgamma_m%s_may5.root"%mass
  mcSigFile = TFile(mcSigFileName)
  sigWindowMCsigTree = mcSigFile.Get(sigWindowTreeName)
  sigWindowMCsig = higgs(sigWindowMCsigTree)
  nSignalWindowEventsInMCsig = sigWindowMCsig.Loop(HbbCutValue, cosThetaCutValue, pToverMcutValue, lowerMassBound, upperMassBound)
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

def MCbgGetSoverRootB(small3sDir, ddDir, mass, masswindow, HbbCutValue, cosThetaCutValue, pToverMcutValue, compileOrLoad):
  weightsDict = getWeightsDict(small3sDir)
  #print "the weights dictionary is:"
  #print weightsDict
  small3ddDict = getSmall3ddTreeDict(ddDir)
  sTotal = 0
  bTotal = 0
  for mcBgFile in weightsDict.keys():
    unweightedSoverRootBinfo = calcSoverRootB(small3ddDict[mcBgFile], mass, masswindow, HbbCutValue, cosThetaCutValue, pToverMcutValue, compileOrLoad)
    #print "S for %s is: %s" % (mcBgFile, str(unweightedSoverRootBinfo["S"]))
    sTotal = unweightedSoverRootBinfo["S"]
    #print "unweighted B for %s is: %s" % (mcBgFile, str(unweightedSoverRootBinfo["B"]))
    #print "weight is %s" % str(weightsDict[mcBgFile])
    bTotal += float(unweightedSoverRootBinfo["B"]) * weightsDict[mcBgFile]
    compileOrLoad = "load"
  response = {}
  response["S"]=sTotal
  response["B"]=bTotal
  response["compileOrLoad"] = "load"
  return response

def fillGraph(graph, dataOrMCbg, mass, masswindow, cosThetaCutValue, pToverMcutValue, compileOrLoad):
  normalizations = getNormalizations()
  if not (dataOrMCbg == "data" or dataOrMCbg == "MC"):
    exit("Please pick either 'data' or 'MC' for the background")
  for i in range(-10, 110):
    HbbCutValue = i/float(100)
  #for i in range(-1, 11):
  #  HbbCutValue = i/float(10)
    if dataOrMCbg == "data":
      sOverRootB = calcSoverRootB(inSampleFile, mass, masswindow, HbbCutValue, cosThetaCutValue, pToverMcutValue, compileOrLoad)["SoverRootB"]
      #print "      S/sqrt(B) is %s" % str(sOverRootB)
      if (isinstance(sOverRootB, float)):
        graph.SetPoint(graph.GetN(), HbbCutValue, sOverRootB)
      compileOrLoad = "load"
    elif dataOrMCbg == "MC":
      bgMCsOverRootBinfo = MCbgGetSoverRootB(small3sDir, ddDir, mass, masswindow, HbbCutValue, cosThetaCutValue, pToverMcutValue, compileOrLoad)
      compileOrLoad=bgMCsOverRootBinfo["compileOrLoad"]
      sTotal = bgMCsOverRootBinfo["S"]
      bTotal = bgMCsOverRootBinfo["B"]
      #print "total B is: %f" % bTotal
      if not bTotal == 0:
        sOverRootB = sTotal / sqrt(bTotal)
        graph.SetPoint(graph.GetN(), HbbCutValue, normalizations[mass]*sOverRootB)

def makeOptGraphs():
  cosThetaCutValue = 0.7
  graphs = []
  compileOrLoad = "compile" # just compile the first time
  massWindows = getMassWindows()
  for mass in massWindows.keys():
    masswindow = massWindows[mass]
    graphs.append(TGraph())
    #print "Signal mass %f" % mass
    fillGraph(graphs[-1], dataOrMCbg, str(mass), masswindow, cosThetaCutValue, pToverMcutValue, compileOrLoad)
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
  outfile = TFile("HbbOpt_SoverRootB.root", "RECREATE")
  outfile.cd()
  canvas.Write()
  outfile.Close()
