from math import sqrt
from ROOT import *
from testpy import getRangesDict, getWRangesDict
from getMCbgWeights import getMCbgLabels
from os import path, makedirs

# John Hakala, 12/1/2016
# Makes optimization plots by sliding cuts over N-1 stackplots from makeStacks.py

gROOT.SetBatch()

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


# 6/22/18: Butchering this to what I need!!!
def makeOpt(inFileName_Wwindow, upDown, srCans, srPads, sbCans, sbPads, stacks, i, windowEdges):
  
  debug=True
  inFile_Wwindow     = TFile(inFileName_Wwindow)
  if debug:
    print "inFile_Wwindow is: %s" % inFile_Wwindow.GetName()
  
  for key in inFile_Wwindow.GetListOfKeys():
    if debug:
      print "Wwindow File has key ",key.GetName()
    if "c1" in key.GetName():
      can_Wwindow = inFile_Wwindow.Get(key.GetName()).DrawClone()
      can_Wwindow.SetName("%i_%s_c1_Wwindow" % (i, inFileName_Wwindow))
      print "can_Wwindow: ",
      print can_Wwindow
      SetOwnership(can_Wwindow, False)
      srCans.append(can_Wwindow)
      #canName_Wwindow = "c1_Wwindow"
        
  for key in inFile_Wwindow.GetListOfKeys():
    if debug:
      print "inFile_Wwindow is: %s" % inFile_Wwindow.GetName()
      print "inFile_Wwindow has key: ", 
      print key.GetName()
  #print "canName_Wwindow: %s" % canName_Wwindow 
  if debug:
    print can_Wwindow
  for prim in can_Wwindow.GetListOfPrimitives():
    if debug:
      print "can_Wwindow has primitive: %s" % prim.GetName()
    prim.SetName("%i_%s_Wwindow" % (i, prim.GetName()))
    #print "can_Wwindow has renamed primitive: %s" % prim.GetName()
    if "stack" in prim.GetName():
      pad_Wwindow = prim
      for primitive in pad_Wwindow.GetListOfPrimitives():
        if not ("TLine" in primitive.IsA().GetName() or "TFrame" in primitive.IsA().GetName()):
          primitive.SetName("%s_%s_Wwindow" % (inFileName_Wwindow, primitive.GetName()))
      #print "pad_Wwindow: ",
      #print  pad_Wwindow
      SetOwnership(pad_Wwindow, False)
      srPads.append(pad_Wwindow)
      #print "using Wwindow stack: %s" % padName_Wwindow
    if debug:
      print "prim.GetName()", prim.GetName()
    if "ratio" in prim.GetName():
      bottomPad_Wwindow = prim
      for primitive in bottomPad_Wwindow.GetListOfPrimitives():
        if not ("TLine" in primitive.IsA().GetName() or "TFrame" in primitive.IsA().GetName()):
          primitive.SetName("%s_%s_Wwindow" % (inFileName_Wwindow, primitive.GetName()))
      SetOwnership(bottomPad_Wwindow, False)
      srPads.append(bottomPad_Wwindow)
      bottomPad_ratio=srPads[-1]
      
  for subprim in pad_Wwindow.GetListOfPrimitives():
    print "pad_Wwindow has primitive: %s" % subprim.GetName()
    if "m600" in subprim.GetName():
      name600 = subprim.GetName()
    if "m800" in subprim.GetName():
      name800 = subprim.GetName()
    if "m1000" in subprim.GetName():
      name1000 = subprim.GetName()
    if "m2000" in subprim.GetName():
      name2000 = subprim.GetName()
    if "m3500" in subprim.GetName():
      name3500 = subprim.GetName()
    if "THStack" in subprim.IsA().GetName():

      print "found THStack at ",subprim.GetName()
      subprim.SetName("%i_theStack_%s" % ( i, inFileName_Wwindow))

      stack = subprim
      SetOwnership(stack, False)
      stacks.append(stack)
    if "SilverJson" in subprim.GetName():
      subprim.SetName("garbage_%i_%s_%s" % (i, inFileName_Wwindow, subprim.GetName()))
      subprim.Delete()
  print "DEBUGGING STACK"
  print stack
  print stack.GetStack()
  can = TCanvas("stackDebug","stackDebug",800,800)
  can.cd()
  stack.GetStack().Last().Draw()
  outFile = TFile("stackDebug.root","RECREATE")
  outFile.cd()
  can.Write()
  outFile.Close() 
 
  sbNorm = stack.GetStack().Last().GetSumOfWeights()/float(sideband.GetSumOfWeights())
  print "number of entries in stack is   : %i" % stack.GetStack().Last().GetSumOfWeights()
  print "number of entries in sideband is: %i" % sideband.GetSumOfWeights()
  print "                       sbNorm is: %f" % sbNorm 
  for sbBin in range (1, sideband.GetXaxis().GetNbins()+1):
    sideband.SetBinContent(sbBin, sideband.GetBinContent(sbBin)*sbNorm)
  #stack = stacks[-1]
  #theSideband = sidebands[-1]
  #print stack

  ## HERE?  can_Wwindow.Draw()
  m600 = pad_Wwindow.GetPrimitive(name600)
  color600 = kTeal
  m600.SetLineColor(color600)
  m600.SetLineStyle(2)
  m600.SetLineWidth(3)
  m800 = pad_Wwindow.GetPrimitive(name800)
  color800  = kOrange-3
  m800.SetLineColor(color800)
  m800.SetLineStyle(2)
  m800.SetLineWidth(3)
  m1000 = pad_Wwindow.GetPrimitive(name1000)
  color1000 = kPink-3
  m1000.SetLineColor(color1000)
  m1000.SetLineStyle(2)
  m1000.SetLineWidth(3)
  m2000 = pad_Wwindow.GetPrimitive(name2000)
  color2000 = kRed+2
  m2000.SetLineColor(color2000)
  m2000.SetLineStyle(2)
  m2000.SetLineWidth(3)
  m3500 = pad.GetPrimitive(name3500)
  color3500 = kRed-3
  m3500.SetLineColor(color2000)
  m3500.SetLineStyle(2)
  m3500.SetLineWidth(3)

  total = sideband
  if not m600.GetNbinsX() == total.GetNbinsX():
    print "nonmatching histograms!"
    quit()

  graphPoints600 = []
  graphPoints800 = []
  graphPoints1000 = []
  graphPoints2000 = []
  graphPoints3500 = []
  nSteps = total.GetNbinsX()
  # HACK HACK
  lowerBound = getRangesDict()[whichVarAmI(inFileName_Wwindow)][0][0]
  upperBound = getRangesDict()[whichVarAmI(inFileName_Wwindow)][0][1]
  # END HACK HACK
  stepSize = (upperBound-lowerBound)/nSteps
  for i in range(0, total.GetNbinsX()):
    slideValue = lowerBound+i*stepSize
    sOverRootB600= getSoverRootB(total, m600, slideValue, upDown, withBtag)
    sOverRootB800= getSoverRootB(total, m800, slideValue, upDown, withBtag)
    sOverRootB1000= getSoverRootB(total, m1000, slideValue, upDown, withBtag)
    sOverRootB2000= getSoverRootB(total, m2000, slideValue, upDown, withBtag)
    if type(sOverRootB600) is float : 
      graphPoints600.append([slideValue, sOverRootB600])
      #print "filled point %f %f into graphPoints600" % ( slideValue, sOverRootB600)
    if type(sOverRootB800) is float : 
      graphPoints800.append([slideValue, sOverRootB800])
      #print "filled point %f %f into graphPoints800" % ( slideValue, sOverRootB800)
    if type(sOverRootB1000) is float : 
      graphPoints1000.append([slideValue, sOverRootB1000])
      #print "filled point %f %f into graphPoints1000" % ( slideValue, sOverRootB1000)
    if type(sOverRootB2000) is float : 
      graphPoints2000.append([slideValue, sOverRootB2000])
    #if type(sOverRootB3500) is float : 
    #  graphPoints3500.append([slideValue, sOverRootB1000])

  #  print graphPoints
  #graph3500 = TGraph()
  #for graphPoint3500 in graphPoints3500:
  #  graph3500.SetPoint(graph3500.GetN(), graphPoint3500[0], graphPoint3500[1])
  #  #print "set point in graph3500"

  graph2000 = TGraph()
  graph2000.SetName("optGraph_%s"%name2000)
  for graphPoint2000 in graphPoints2000:
    graph2000.SetPoint(graph2000.GetN(), graphPoint2000[0], graphPoint2000[1])
    #print "set point in graph2000"

  graph1000 = TGraph()
  graph1000.SetName("optGraph_%s"%name1000)
  for graphPoint1000 in graphPoints1000:
    graph1000.SetPoint(graph1000.GetN(), graphPoint1000[0], graphPoint1000[1])
    #print "set point in graph1000"

  graph800 = TGraph()
  graph800.SetName("optGraph_%s"%name800)
  for graphPoint800 in graphPoints800:
    graph800.SetPoint(graph800.GetN(), graphPoint800[0], graphPoint800[1])
    #print "set point in graph800"

  graph600 = TGraph()
  graph600.SetName("optGraph_%s"%name600)
  for graphPoint600 in graphPoints600:
    graph600.SetPoint(graph600.GetN(), graphPoint600[0], graphPoint600[1])
    #print "set point in graph600"

  #bottomPad_Wwindow.cd()
  #bottomPad_Wwindow.Clear()
  bottomPad_ratio.cd()
  bottomPad_ratio.Clear()
  graph800.Draw()
  graph800.GetXaxis().SetLimits(lowerBound, upperBound)
  #graph800.Draw()
  #graph800.GetXaxis().SetLimits(lowerBound, upperBound)
  #bottomPad_Wwindow.SetBottomMargin(0.18)
  #bottomPad_Wwindow.SetBorderSize(0)
  #bottomPad_Wwindow.Draw()
  bottomPad_ratio.SetBottomMargin(0.18)
  bottomPad_ratio.SetBorderSize(0)
  bottomPad_ratio.Draw()
  pad_Wwindow.SetBottomMargin(0.15)
  can_Wwindow.cd()
  #pad.SetBBoxY1(-2)
  #pad.SetBBoxY2(105)
  pad_Wwindow.Draw()
  pad_Wwindow.cd()
  sideband.SetMarkerStyle(20)
  sideband.SetMarkerColor(kBlack)
  sideband.SetLineColor(kBlack)
  sideband.Draw("SAME PE")
  for prim in pad_Wwindow.GetListOfPrimitives():
    if "TLegend" in prim.IsA().GetName():
      prim.InsertEntry(sideband.GetName(), "Sideband %i GeV < m_{j} < %i GeV" % (windowEdges[0], windowEdges[1]))

  #bottomPad_Wwindow.cd()
  bottomPad_ratio.cd()
  graph800.GetYaxis().SetTitle("S/#sqrt{B} (a.u.)")
  graph800.GetYaxis().SetLabelSize(0)
  graph800.GetXaxis().SetLabelSize(0.1)
  graph800.GetYaxis().SetTitleSize(0.12)
  graph800.GetYaxis().SetTitleOffset(.3)
  graph800.GetXaxis().SetTitle("cut value")
  graph800.GetXaxis().SetTitleSize(0.12)
  graph800.GetXaxis().SetTitleOffset(0.65)
  graph800.SetLineStyle(2)
  graph800.SetLineWidth(2)
  graph800.SetLineColor(color800)
  graph800.SetFillColor(kWhite)
  graph800.SetMarkerStyle(20)
  graph800.SetMarkerSize(0)
  graph1000.Draw("SAME")
  graph1000.SetLineStyle(2)
  graph1000.SetLineWidth(2)
  graph1000.SetLineColor(color1000)
  graph1000.SetFillColor(kWhite)
  graph2000.Draw("SAME")
  graph2000.SetLineStyle(2)
  graph2000.SetLineWidth(2)
  graph2000.SetLineColor(color2000)
  graph2000.SetFillColor(kWhite)
  graph600.Draw("SAME")
  graph600.SetLineStyle(2)
  graph600.SetLineWidth(2)
  graph600.SetLineColor(color600)
  graph600.SetFillColor(kWhite)
  #bottomPad_Wwindow.BuildLegend()
  bottomPad_ratio.BuildLegend()
  legendLabels = getMCbgLabels()
  #for prim in bottomPad_Wwindow.GetListOfPrimitives():
  for prim in bottomPad_ratio.GetListOfPrimitives():
    if "TLegend" in prim.IsA().GetName():
      prim.SetX1NDC(0.753)
      prim.SetY1NDC(0.703)
      prim.SetX2NDC(0.946)
      prim.SetY2NDC(0.911)
      for subprim in prim.GetListOfPrimitives():
        for mass in ["600", "800", "1000", "2000"]:
          if mass in subprim.GetLabel():
            subprim.SetLabel("H#gamma(%r TeV)"%(float(mass)/float(800)))
            subprim.SetOption("lf")
  can_Wwindow.cd()
  #bottomPad_Wwindow.Draw()
  bottomPad_ratio.Draw()
  pad_Wwindow.SetBorderSize(0)

  
  outDirName =  "optplots_nMinus1_noBtag_dd_sb%i%i" % (windowEdges[0], windowEdges[1])
  outFileName="%s/%s"%(outDirName, inFileName_Wwindow.split("/")[1])
  if not path.exists(outDirName):
    makedirs(outDirName)
  outFileName=outFileName.split(".")[0]
  outFile = TFile("%s_%r.root"%(outFileName, upDown), "RECREATE")
  outFile.cd()
  can_Wwindow.Write()
  can_Wwindow.Print("%s_%r.pdf"%(outFileName, upDown))
  outFile.Close()


from sys import argv
#if not 3 is len(argv) :
#  print "please supply two arguments, with/without btag and the sideband name." 
#  exit(1)
#if not argv[2] in ["100110", "5070", "80100"]:
#  print 'invalid second argument, either "100110", "5070", or "80100"'
#  exit(1)
#withBtag = argv[1]
#if argv[2] in "100110":
#  windowEdges = [100.0, 110.0]
#elif argv[2] in "5070":
#  windowEdges = [50.0, 70.0]
#elif argv[2] in "80100":
#  windowEdges = [80.0, 100.0]
windowEdges = [70,90]



for direction in ["up", "down"]:
  srCans =  []
  srPads =  []
  sbCans =  []
  sbPads =  []
  stacks = []
  sidebands = []
  i=0
  for key in getWRangesDict().keys():
    # for withBtag / noBtag you need to change the next THREE lines
    #sideband_varName    = "stackplots_puppiSoftdrop_nMinus1_%s_sideband%i%i/nMinus1_stack_%s.root"%( withBtag, windowEdges[0], windowEdges[1], key)
    srcName = "stackplots_puppiSoftdrop_preselection/preselection_stack_%s.root"%key
    #NOTE: Sideband file shouldn't be too different from my preselection file I think... just check the scaling line in makeStacks.py (denoted with "HEREHERE")
    #Wwindow_varName = "stackplots_puppiSoftdrop_nMinus1_%s/nMinus1_stack_%s.root"%(withBtag, key)
    makeOpt(srcName, direction, srCans, srPads, sbCans, sbPads, stacks, i, windowEdges)
    i+=1
  if direction is direction[-1]:
    exit(0)
#for direction in ["up", "down"]:
#  srCans =  []
#  srPads =  []
#  sbCans =  []
#  sbPads =  []
#  stacks = []
#  sidebands = []
#  i=0
#  for key in getHiggsRangesDict().keys():
#    sideband_varName = "stackplots_puppiSoftdrop_nMinus1_noBtag_sideband/nMinus1_stack_%s.root"%key
#    Wwindow_varName = "stackplots_puppiSoftdrop_nMinus1_noBtag/nMinus1_stack_%s.root"%key
#    makeOpt(sideband_varName, Wwindow_varName, direction, False, srCans, srPads, sbCans, sbPads, stacks, sidebands, i)
#    i+=1
#  if direction is direction[-1]:
#    exit(0)
