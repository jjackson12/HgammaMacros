from math import sqrt
from ROOT import *
from pyrootTools import instance
from getMCbgWeights import getWeightsDict

def calcSoverRootB(mass, masswindow, cutValue, compileOrLoad):

  sigWindowTreeName = "higgs"  # just keep the name from TTree::MakeClass(), don't give it a special name
  instance(sigWindowTreeName, compileOrLoad)
  
  dataFileName = "may5_tagging/allMCbgs.root"
  dataFile = TFile(dataFileName)
  sigWindowDataTree = dataFile.Get(sigWindowTreeName)
  sigWindowData = higgs(sigWindowDataTree)
  
  lowerMassBound = masswindow[0]
  upperMassBound = masswindow[1]
  print "    For Hbb working point %f:" % cutValue
  nSignalWindowEventsInData = sigWindowData.Loop(cutValue, lowerMassBound, upperMassBound)
  print "      Number of signal window events in background MC is: %i" % nSignalWindowEventsInData
  
  mcSigFileName = "may5_Hgamma_tagging/Hgamma_m%s_may5.root"%mass
  mcSigFile = TFile(mcSigFileName)
  sigWindowMCTree = mcSigFile.Get(sigWindowTreeName)
  sigWindowMCsig = higgs(sigWindowMCTree)
  nSignalWindowEventsInMCsig = sigWindowMCsig.Loop(cutValue, lowerMassBound, upperMassBound)
  print "      Number of signal window events in signal MC is: %i" % nSignalWindowEventsInMCsig

  if not nSignalWindowEventsInData==0:
    return nSignalWindowEventsInMCsig/sqrt(nSignalWindowEventsInData)
  elif nSignalWindowEventsInData==0:
    return "%i / sqrt(0)" % nSignalWindowEventsInMCsig
  else:
    print "something's screwy!"
    exit(1)

def fillGraph(graph, mass, masswindow, compileOrLoad):
  for i in range(-1, 11):
    cutValue = i/float(10)
    sOverRootB = calcSoverRootB(mass, masswindow, cutValue, compileOrLoad)
    print "      S/sqrt(B) is %s" % str(sOverRootB)
    if (isinstance(sOverRootB, float)):
      graph.SetPoint(graph.GetN(), cutValue, sOverRootB)
    compileOrLoad = "load"

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
  print "Signal mass %f" % mass
  fillGraph(graphs[-1], str(mass), masswindow, compileOrLoad)
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


