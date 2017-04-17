from math import sqrt
from ROOT import *
from testpy import getRangesDict, getHiggsRangesDict
from getMCbgWeights import getMCbgLabels

# John Hakala, 12/1/2016
# Makes optimization plots by sliding cuts over N-1 stackplots from makeStacks.py

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
    if "m1000" in subprim.GetName():
      name1000 = subprim.GetName()
    if "m2050" in subprim.GetName():
      name2050 = subprim.GetName()
    if "m3250" in subprim.GetName():
      name3250 = subprim.GetName()
    #if "m4000" in subprim.GetName():
    #  name4000 = subprim.GetName()
    if "THStack" in subprim.IsA().GetName():
      subprim.SetName("theStack")
  stack = pad.GetPrimitive("theStack")
  #print stack

  m750 = pad.GetPrimitive(name750)
  m750.SetLineColor(kTeal)
  m750.SetLineStyle(2)
  m750.SetLineWidth(3)
  m1000 = pad.GetPrimitive(name1000)
  m1000.SetLineColor(kOrange-3)
  m1000.SetLineStyle(2)
  m1000.SetLineWidth(3)
  m2050 = pad.GetPrimitive(name2050)
  m2050.SetLineColor(kPink-3)
  m2050.SetLineStyle(2)
  m2050.SetLineWidth(3)
  m3250 = pad.GetPrimitive(name3250)
  m3250.SetLineColor(kRed+2)
  m3250.SetLineStyle(2)
  m3250.SetLineWidth(3)

  #m4000 = pad.GetPrimitive(name4000)
  total = stack.GetStack().Last()
  if not m750.GetNbinsX() == total.GetNbinsX():
    print "nonmatching histograms!"
    quit()

  graphPoints750 = []
  graphPoints1000 = []
  graphPoints2050 = []
  graphPoints3250 = []
  #graphPoints4000 = []
  nSteps = total.GetNbinsX()
  lowerBound = getRangesDict()[whichVarAmI(inFileName)][0]
  upperBound = getRangesDict()[whichVarAmI(inFileName)][1]
  stepSize = (upperBound-lowerBound)/nSteps
  for i in range(0, total.GetNbinsX()):
    slideValue = lowerBound+i*stepSize
    sOverRootB750= getSoverRootB(total, m750, slideValue, upDown, withBtag)
    sOverRootB1000= getSoverRootB(total, m1000, slideValue, upDown, withBtag)
    sOverRootB2050= getSoverRootB(total, m2050, slideValue, upDown, withBtag)
    sOverRootB3250= getSoverRootB(total, m3250, slideValue, upDown, withBtag)
    if type(sOverRootB750) is float : 
      graphPoints750.append([slideValue, sOverRootB750])
      #print "filled point %f %f into graphPoints750" % ( slideValue, sOverRootB750)
    if type(sOverRootB1000) is float : 
      graphPoints1000.append([slideValue, sOverRootB1000])
      #print "filled point %f %f into graphPoints1000" % ( slideValue, sOverRootB1000)
    if type(sOverRootB2050) is float : 
      graphPoints2050.append([slideValue, sOverRootB2050])
      #print "filled point %f %f into graphPoints2050" % ( slideValue, sOverRootB2050)
    if type(sOverRootB3250) is float : 
      graphPoints3250.append([slideValue, sOverRootB3250])
    #if type(sOverRootB4000) is float : 
    #  graphPoints4000.append([slideValue, sOverRootB2050])

#  print graphPoints
  #graph4000 = TGraph()
  #for graphPoint4000 in graphPoints4000:
  #  graph4000.SetPoint(graph4000.GetN(), graphPoint4000[0], graphPoint4000[1])
  #  #print "set point in graph4000"

  graph3250 = TGraph()
  graph3250.SetName("optGraph_%s"%name3250)
  for graphPoint3250 in graphPoints3250:
    graph3250.SetPoint(graph3250.GetN(), graphPoint3250[0], graphPoint3250[1])
    #print "set point in graph3250"

  graph2050 = TGraph()
  graph2050.SetName("optGraph_%s"%name2050)
  for graphPoint2050 in graphPoints2050:
    graph2050.SetPoint(graph2050.GetN(), graphPoint2050[0], graphPoint2050[1])
    #print "set point in graph2050"

  graph1000 = TGraph()
  graph1000.SetName("optGraph_%s"%name1000)
  for graphPoint1000 in graphPoints1000:
    graph1000.SetPoint(graph1000.GetN(), graphPoint1000[0], graphPoint1000[1])
    #print "set point in graph1000"

  graph750 = TGraph()
  graph750.SetName("optGraph_%s"%name750)
  for graphPoint750 in graphPoints750:
    graph750.SetPoint(graph750.GetN(), graphPoint750[0], graphPoint750[1])
    #print "set point in graph750"

  bottomPad = can.GetPrimitive(bottomPadName)
  bottomPad.cd()
  bottomPad.Clear()
  graph1000.Draw()
  graph1000.GetXaxis().SetLimits(lowerBound, upperBound)
  #graph1000.Draw()
  #graph1000.GetXaxis().SetLimits(lowerBound, upperBound)
  bottomPad.SetBottomMargin(0.18)
  bottomPad.SetBorderSize(0)
  bottomPad.Draw()
  pad.SetBottomMargin(0.15)
  can.cd()
  #pad.SetBBoxY1(-2)
  #pad.SetBBoxY2(105)
  pad.Draw()

  bottomPad.cd()
  graph1000.GetYaxis().SetTitle("S/#sqrt{B} (a.u.)")
  graph1000.GetYaxis().SetLabelSize(0)
  graph1000.GetXaxis().SetLabelSize(0.1)
  graph1000.GetYaxis().SetTitleSize(0.12)
  graph1000.GetYaxis().SetTitleOffset(.3)
  graph1000.GetXaxis().SetTitle("cut value")
  graph1000.GetXaxis().SetTitleSize(0.12)
  graph1000.GetXaxis().SetTitleOffset(0.65)
  graph1000.SetLineStyle(2)
  graph1000.SetLineWidth(2)
  graph1000.SetLineColor(kRed+2)
  graph1000.SetFillColor(kWhite)
  graph1000.SetMarkerStyle(20)
  graph1000.SetMarkerSize(0)
  #graph3250.GetYaxis().SetTitle("S/#sqrt{B} (a.u.)")
  #graph3250.GetYaxis().SetLabelSize(0)
  #graph3250.GetXaxis().SetLabelSize(0.1)
  #graph3250.GetYaxis().SetTitleSize(0.12)
  #graph3250.GetYaxis().SetTitleOffset(.3)
  #graph3250.GetXaxis().SetTitle("cut value")
  #graph3250.GetXaxis().SetTitleSize(0.12)
  #graph3250.GetXaxis().SetTitleOffset(0.65)
  #graph3250.SetLineStyle(2)
  #graph3250.SetLineWidth(2)
  #graph3250.SetLineColor(kPink-3)
  #graph3250.SetMarkerStyle(20)
  #graph3250.SetMarkerSize(0)
  graph2050.Draw("SAME")
  graph2050.SetLineStyle(2)
  graph2050.SetLineWidth(2)
  graph2050.SetLineColor(kPink-3)
  graph2050.SetFillColor(kWhite)
  graph3250.Draw("SAME")
  graph3250.SetLineStyle(2)
  graph3250.SetLineWidth(2)
  graph3250.SetLineColor(kOrange-3)
  graph3250.SetFillColor(kWhite)
  graph750.Draw("SAME")
  graph750.SetLineStyle(2)
  graph750.SetLineWidth(2)
  graph750.SetLineColor(kTeal)
  graph750.SetFillColor(kWhite)
  bottomPad.BuildLegend()
  legendLabels = getMCbgLabels()
  for prim in bottomPad.GetListOfPrimitives():
    if "TLegend" in prim.IsA().GetName():
      prim.SetX1NDC(0.753)
      prim.SetY1NDC(0.703)
      prim.SetX2NDC(0.946)
      prim.SetY2NDC(0.911)
      for subprim in prim.GetListOfPrimitives():
        for mass in ["750", "1000", "2050", "3250"]:
          if mass in subprim.GetLabel():
            subprim.SetLabel("H#gamma(%r TeV)"%(float(mass)/float(1000)))
            subprim.SetOption("lf")
  can.cd()
  bottomPad.Draw()
  pad.SetBorderSize(0)

  
  if withBtag:
    outFileName="optplots_nMinus1_withBtag/%s"%inFileName.split("/")[1]
  else:
    outFileName="optplots_nMinus1_noBtag/%s"%inFileName.split("/")[1]
  outFileName=outFileName.split(".")[0]
  outFile = TFile("%s_%r.root"%(outFileName, upDown), "RECREATE")
  outFile.cd()
  can.Write()
  can.Print("%s_%r.pdf"%(outFileName, upDown))
  outFile.Close()

for direction in ["up", "down"]:
  for key in getHiggsRangesDict().keys():
    varName = "stackplots_nMinus1_withBtag/nMinus1_stack_%s.root"%key
    makeOpt(varName, direction, True)
for direction in ["up", "down"]:
  for key in getHiggsRangesDict().keys():
    varName = "stackplots_nMinus1_noBtag/nMinus1_stack_%s.root"%key
    makeOpt(varName, direction, False)
