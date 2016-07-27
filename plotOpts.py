from math import sqrt
from ROOT import *
from testpy import getRangesDict, getHiggsRangesDict

def whichVarAmI(inFileName):
  for key in getRangesDict().keys():
    if key in inFileName:
      iAm = key
  return iAm

def getSoverRootB(bkg, sig, start, goUpOrDown, withBtag):
  bb=0.
  ss=0.
  if goUpOrDown in "up":
    for iBin in range(bkg.FindBin(start), bkg.GetNbinsX()):
      bb+=bkg.GetBinContent(iBin)
      ss+=sig.GetBinContent(iBin)
  elif goUpOrDown in "down":
    for iBin in range(0, bkg.FindBin(start)):
      bb+=bkg.GetBinContent(iBin)
      ss+=sig.GetBinContent(iBin)
  if bb != 0:
    return ss/sqrt(bb)
  else:
    return "b=0"

def makeOpt(inFileName, upDown, withBtag):
  inFile     = TFile(inFileName)

  for key in inFile.GetListOfKeys():
    #print key.GetName()
    if "c1" in key.GetName():
      canName = key.GetName()
  #print "canName: %s" % canName 
  can = inFile.Get(canName)
  can.Draw()
  for prim in can.GetListOfPrimitives():
    if "stack" in prim.GetName():
      padName = prim.GetName()
    if "ratio" in prim.GetName():
      bottomPadName = prim.GetName()

  pad = can.GetPrimitive(padName)

  for subprim in pad.GetListOfPrimitives():
    if "m750" in subprim.GetName():
      name750 = subprim.GetName()
    if "THStack" in subprim.IsA().GetName():
      subprim.SetName("theStack")
  stack = pad.GetPrimitive("theStack")
  #print stack

  m750 = pad.GetPrimitive(name750)
  total = stack.GetStack().Last()
  if not m750.GetNbinsX() == total.GetNbinsX():
    print "nonmatching histograms!"
    quit()

  graphPoints = []
  nSteps = total.GetNbinsX()
  lowerBound = getRangesDict()[whichVarAmI(inFileName)][0]
  upperBound = getRangesDict()[whichVarAmI(inFileName)][1]
  stepSize = (upperBound-lowerBound)/nSteps
  for i in range(0, total.GetNbinsX()):
    slideValue = lowerBound+i*stepSize
    sOverRootB= getSoverRootB(total, m750, slideValue, upDown, withBtag)
    if type(sOverRootB) is float : 
      graphPoints.append([slideValue, sOverRootB])

  print graphPoints

  graph = TGraph()
  for graphPoint in graphPoints:
    graph.SetPoint(graph.GetN(), graphPoint[0], graphPoint[1])

  bottomPad = can.GetPrimitive(bottomPadName)
  bottomPad.cd()
  bottomPad.Clear()
  graph.Draw()
  graph.GetXaxis().SetLimits(lowerBound, upperBound)
  bottomPad.SetBottomMargin(0.18)
  bottomPad.SetBorderSize(0)
  bottomPad.Draw()
  pad.SetBottomMargin(0.15)
  can.cd()
  #pad.SetBBoxY1(-2)
  #pad.SetBBoxY2(105)
  pad.Draw()

  graph.GetYaxis().SetTitle("S/#sqrt{B} (a.u.)")
  graph.GetYaxis().SetLabelSize(0)
  graph.GetXaxis().SetLabelSize(0.1)
  graph.GetYaxis().SetTitleSize(0.12)
  graph.GetYaxis().SetTitleOffset(.3)
  graph.GetXaxis().SetTitle("cut value")
  graph.GetXaxis().SetTitleSize(0.12)
  graph.GetXaxis().SetTitleOffset(0.65)
  bottomPad.Draw()
  pad.SetBorderSize(0)

  
  if withBtag:
    outFileName="optplots_nMinus1_withBtag/%s"%inFileName.split("/")[1]
  else:
  
    outFileName="optplots_nMinus1_noBtag/%s"%inFileName.split("/")[1]
  outFile = TFile(outFileName, "RECREATE")
  outFile.cd()
  can.Write()
  can.Print("%s_%r.pdf"%(outFileName.split(".")[0], upDown))
  outFile.Close()

for direction in ["up", "down"]:
  for key in getHiggsRangesDict().keys():
    varName = "stackplots_nMinus1_withBtag/nMinus1_stack_%s.root"%key
    makeOpt(varName, direction, True)
for direction in ["up", "down"]:
  for key in getHiggsRangesDict().keys():
    varName = "stackplots_nMinus1_noBtag/nMinus1_stack_%s.root"%key
    makeOpt(varName, direction, False)
