from math import sqrt
from ROOT import *
from pyrootTools import instance, getSortedDictKeys
from getMCbgWeights import getWeightsDict, getMCbgWeightsDict, getSmall3ddTreeDict
from HgParameters import getNormalizations, getMassWindows, getSamplesDirs
from HgCuts import getCutValues

# Methods for finding optimal cuts - here focusing on the Hbb tagger - using the treeChecker trees.
# The bottom methods focus on S/root(B) as the figure of merit.
# There are other scripts that use some of the top methods here but focus on an expected CL95 limit as the figure of merit.
# John Hakala, 5/11/2016

dataOrMCbg = "MC"
samplesDirs = getSamplesDirs()
small3sDir = samplesDirs["small3sDir"]
ddDir = samplesDirs["ddDir"]
inSampleFile = samplesDirs["dataDir"]
doOptGraphs = True
doComparisonGraphs = False

def calcSoverRootB(sampleFile, mass, higgswindow, masswindow, category, HbbCutValue, pToverMcutValue, deltaRcutValue, jetEtaCutValue, phoEtaCutValue, compileOrLoad):

  sigWindowTreeName = "higgs"  # just keep the name from TTree::MakeClass(), don't give it a special name
  instance(sigWindowTreeName, compileOrLoad)
  
  bgFileName = sampleFile
  bgFile = TFile(bgFileName)
  #print "bgFilename: %s" % bgFileName
  sigWindowBgTree = bgFile.Get(sigWindowTreeName)
  #print sigWindowBgTree
  sigWindowBg = higgs(sigWindowBgTree)
  
  lowerMassBound = masswindow[0]
  upperMassBound = masswindow[1]
  jetMassLowerBound = higgswindow[0]
  jetMassUpperBound = higgswindow[1]
  #print "    For Hbb working point %f:" % HbbCutValue
  # new higgs class Loop method:
  # int higgs::Loop(std::string category, float HbbCutValue,  float pToverMcutValue, float deltaRcutValue, float jetEtaCutValue, float phoEtaCutValue, float jetMassLowerBound, float jetMassUpperBound, float lowerMassBound, float upperMassBound)

  nSignalWindowEventsInBkg = sigWindowBg.Loop(category, HbbCutValue, pToverMcutValue, deltaRcutValue, jetEtaCutValue, phoEtaCutValue, jetMassLowerBound, jetMassUpperBound, lowerMassBound, upperMassBound)
  #print "      Number of signal window events in background is: %i" % nSignalWindowEventsInBkg
  
  mcSigFileName = "%s/ddTree_Hgamma_m%s.root" % (samplesDirs["ddDir"], mass)
  mcSigFile = TFile(mcSigFileName)
  sigWindowMCsigTree = mcSigFile.Get(sigWindowTreeName)
  sigWindowMCsig = higgs(sigWindowMCsigTree)
  nSignalWindowEventsInMCsig = sigWindowMCsig.Loop(category, HbbCutValue, pToverMcutValue, deltaRcutValue, jetEtaCutValue, phoEtaCutValue, jetMassLowerBound, jetMassUpperBound, lowerMassBound, upperMassBound)
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

def MCbgGetSoverRootB(small3sDir, ddDir, mass, higgswindow, masswindow, category, HbbCutValue, pToverMcutValue, deltaRcutValue, jetEtaCutValue, phoEtaCutValue, compileOrLoad):
  weightsDict = getMCbgWeightsDict(small3sDir)
  #print "the weights dictionary is:"
  #print weightsDict
  small3ddDict = getSmall3ddTreeDict(ddDir)
  sTotal = 0
  bTotal = 0
  for mcBgFile in weightsDict.keys():
    unweightedSoverRootBinfo = calcSoverRootB(small3ddDict[mcBgFile], mass, higgswindow, masswindow, category, HbbCutValue, pToverMcutValue, deltaRcutValue, jetEtaCutValue, phoEtaCutValue, compileOrLoad)
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

def fillGraph(graph, dataOrMCbg, mass, higgswindow, masswindow, category, pToverMcutValue, deltaRcutValue, jetEtaCutValue, phoEtaCutValue, compileOrLoad):
  normalizations = getNormalizations()
  if not (dataOrMCbg == "data" or dataOrMCbg == "MC"):
    exit("Please pick either 'data' or 'MC' for the background")
  for i in range(-10, 100):
    HbbCutValue = i/float(100)
  #for i in range(-1, 11):
  #  HbbCutValue = i/float(10)
    if dataOrMCbg == "data":
      sOverRootB = calcSoverRootB(inSampleFile, mass, higgswindow, masswindow, category, HbbCutValue, pToverMcutValue, deltaRcutValue, jetEtaCutValue, phoEtaCutValue, compileOrLoad)["SoverRootB"]
      #print "      S/sqrt(B) is %s" % str(sOverRootB)
      if (isinstance(sOverRootB, float)):
        graph.SetPoint(graph.GetN(), HbbCutValue, sOverRootB)
      compileOrLoad = "load"
    elif dataOrMCbg == "MC":
      bgMCsOverRootBinfo = MCbgGetSoverRootB(small3sDir, ddDir, mass, higgswindow, masswindow, category, HbbCutValue, pToverMcutValue, deltaRcutValue, jetEtaCutValue, phoEtaCutValue, compileOrLoad)
      compileOrLoad=bgMCsOverRootBinfo["compileOrLoad"]
      sTotal = bgMCsOverRootBinfo["S"]
      bTotal = bgMCsOverRootBinfo["B"]
      #print "total B is: %f" % bTotal
      if not bTotal == 0:
        sOverRootB = sTotal / sqrt(bTotal)
        graph.SetPoint(graph.GetN(), HbbCutValue, normalizations[mass]*sOverRootB)

def fillGraph_pToverM(graph, dataOrMCbg, mass, higgswindow, masswindow, HbbCutValue, deltaRcutValue, jetEtaCutValue, phoEtaCutValue, compileOrLoad):
  cosThetaCutValue = 2
  normalizations = getNormalizations()
  if not (dataOrMCbg == "data" or dataOrMCbg == "MC"):
    exit("Please pick either 'data' or 'MC' for the background")
  for i in range(0, 100):
    pToverMcutValue=i/float(100)
    if dataOrMCbg == "data":
      sOverRootB = calcSoverRootB(inSampleFile, mass, higgswindow, masswindow, category, HbbCutValue, pToverMcutValue, deltaRcutValue, jetEtaCutValue, phoEtaCutValue, compileOrLoad)["SoverRootB"]
      #print "      S/sqrt(B) is %s" % str(sOverRootB)
      if (isinstance(sOverRootB, float)):
        graph.SetPoint(graph.GetN(), HbbCutValue, sOverRootB)
      compileOrLoad = "load"
    elif dataOrMCbg == "MC":
      bgMCsOverRootBinfo = MCbgGetSoverRootB(small3sDir, ddDir, mass, higgswindow, masswindow, HbbCutValue, pToverMcutValue, deltaRcutValue, jetEtaCutValue, phoEtaCutValue, compileOrLoad)
      compileOrLoad=bgMCsOverRootBinfo["compileOrLoad"]
      sTotal = bgMCsOverRootBinfo["S"]
      bTotal = bgMCsOverRootBinfo["B"]
      #print "total B is: %f" % bTotal
      if not bTotal == 0:
        sOverRootB = sTotal / sqrt(bTotal)
        graph.SetPoint(graph.GetN(), pToverMcutValue, normalizations[mass]*sOverRootB)
        print "filling pToverM graph with point (%f, %f)" % (pToverMcutValue, normalizations[mass]*sOverRootB)

#def fillGraph_cosTheta(graph, dataOrMCbg, mass, masswindow, HbbCutValue, compileOrLoad):
#  pToverMcutValue = 0
#  normalizations = getNormalizations()
#  if not (dataOrMCbg == "data" or dataOrMCbg == "MC"):
#    exit("Please pick either 'data' or 'MC' for the background")
#  for i in range(0, 100):
#    cosThetaCutValue=i/float(100)
#    if dataOrMCbg == "data":
#      sOverRootB = calcSoverRootB(inSampleFile, mass, higgswindow, masswindow, category, HbbCutValue, pToverMcutValue, deltaRcutValue, jetEtaCutValue, phoEtaCutValue, compileOrLoad)["SoverRootB"]
#      #print "      S/sqrt(B) is %s" % str(sOverRootB)
#      if (isinstance(sOverRootB, float)):
#        graph.SetPoint(graph.GetN(), HbbCutValue, sOverRootB)
#      compileOrLoad = "load"
#    elif dataOrMCbg == "MC":
#      bgMCsOverRootBinfo = MCbgGetSoverRootB(small3sDir, ddDir, mass, masswindow, HbbCutValue, cosThetaCutValue, pToverMcutValue, compileOrLoad)
#      compileOrLoad=bgMCsOverRootBinfo["compileOrLoad"]
#      sTotal = bgMCsOverRootBinfo["S"]
#      bTotal = bgMCsOverRootBinfo["B"]
#      #print "total B is: %f" % bTotal
#      if not bTotal == 0:
#        sOverRootB = sTotal / sqrt(bTotal)
#        graph.SetPoint(graph.GetN(), cosThetaCutValue, normalizations[mass]*sOverRootB)
#        print "filling cosTheta graph with point (%f, %f)" % (cosThetaCutValue, normalizations[mass]*sOverRootB)

def makeOptGraphs(category, higgswindow, compileOrLoad):
  #cosThetaCutValue = 0.7
  print "making optgraphs for category %s, window (%i-%i)"%(category, higgswindow[0], higgswindow[1])

  graphs = []
  massWindows = getMassWindows()
  massWindows.pop(2000)
  massWindows.pop(3000)
  cutValues = getCutValues()
  pToverMcutValue = cutValues["ptOverM"]
  deltaRcutValue = cutValues["deltaR"]
  jetEtaCutValue = cutValues["jetEta"]
  phoEtaCutValue = cutValues["phEta"]

  for mass in getSortedDictKeys(massWindows):
    print "making S/rootB optGraph for mass %s" % mass
    masswindow = massWindows[mass]
    graphs.append(TGraph())
    graphs[-1].SetNameTitle("HbbOpt", "S/#sqrt{B}, M=%s, higgs window %s-%s"%(str(mass), str(higgswindow[0]), str(higgswindow[1])))
    #print "Signal mass %f" % mass
     # just keep the name from TTree::MakeClass(), don't give it a special name
    samplesDirs = getSamplesDirs()
    fillGraph(graphs[-1], dataOrMCbg, str(mass), higgswindow, masswindow, category, pToverMcutValue, deltaRcutValue, jetEtaCutValue, phoEtaCutValue, compileOrLoad)
    compileOrLoad = "load"
  
  canvas = TCanvas()
  canvas.cd()
  option = ""
  iGraph = 0
  for graph in graphs:
    graph.Draw(option)
    x = TColor()
    graph.SetLineColor(x.GetColor(0, 0.9-iGraph*0.15, iGraph*0.15))
    graph.SetFillColor(kWhite)
    iGraph+=1
    option = "SAME"
  outfile = TFile("HbbOpt_SoverRootB_higgsWindow_%i-%i.root" % (higgswindow[0], higgswindow[1]), "RECREATE")
  outfile.cd()
  canvas.BuildLegend()
  canvas.Draw()
  legend = canvas.GetPrimitive("TPave")
  legend.SetHeader("%s category"%category)
  for prim in canvas.GetListOfPrimitives():
    if "HbbOpt" in prim:
      prim.SetTitle("H(b#bar{b})#gamma optimization: S/#sqrt{B}")
      prim.GetXaxis().SetRangeUser(0, 2500)
  canvas.Write()
  outfile.Close()

def makeCosThetaPtOverMcomparisonGraphs(compileOrLoad):
  HbbCutValue = 0.9
  pToverMgraphs = []
  cosThetagraphs = []
  compileOrLoad = "compile"
  massWindows = getMassWindows()
  massWindows.pop(2000)
  massWindows.pop(3000)
  for mass in getSortedDictKeys(massWindows):
    pToverMgraphs.append(TGraph())
    pToverMgraphs[-1].SetNameTitle("M=%i_pToverM"%mass, "M=%i GeV, p_{T}/M_{j#gamma} cuts"%mass)
    fillGraph_pToverM(pToverMgraphs[-1], dataOrMCbg, str(mass), massWindows[mass], 0.9, compileOrLoad)
    compileOrLoad = "load"
    cosThetagraphs.append(TGraph())
    cosThetagraphs[-1].SetNameTitle("M=%i_cosTheta"%mass, "M=%i GeV, cos(#theta*) cuts"%mass)
    fillGraph_cosTheta(cosThetagraphs[-1], dataOrMCbg, str(mass), massWindows[mass], 0.9, compileOrLoad)
    compileOrLoad = "load"
  outfile = TFile("cosTheta_pToverM_lowMasses_HbbCut0.9.root", "RECREATE")
  outfile.cd()
  for graph in pToverMgraphs:
    graph.Write()
  for graph in cosThetagraphs:
    graph.Write()
  outfile.Close()


if doOptGraphs:
  #instance("higgs", "compile")
  #testFile = TFile("/Users/johakala/WZgammaMacros/newerDDs/newerDD_Hgamma_m650.root")
  #print "testFile: ",
  #print testFile
  #higgsInstance = higgs(testFile.Get("higgs"))
  makeOptGraphs("btag", [110, 140], "compile")
  makeOptGraphs("btag", [100, 140],    "load")
  makeOptGraphs("btag", [95, 145],     "load")
  makeOptGraphs("btag", [90, 150] ,    "load")
if doComparisonGraphs:
  makeCosThetaPtOverMcomparisonGraphs()
