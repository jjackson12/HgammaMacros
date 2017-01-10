from ROOT import *
from pyrootTools import drawInNewCanvas


def normalizeGraphTo(tgraph, var, refVal):
  x = Double()
  y = Double()
  if var == "cosThetaStar":
    tgraph.GetPoint(tgraph.GetN()-1, x, y)
  elif var == "pToverM":
    tgraph.GetPoint(0, x, y)
  print "graph value with no cut applied is %f at cutValue = %f" % (y, x)
  normFactor = Double(refVal/y)
  print "normfactor is %f" % normFactor
  for iPoint in range(0, tgraph.GetN()):
    tgraph.GetPoint(iPoint, x, y)
    print "original value is %f" % y
    tgraph.SetPoint(iPoint, x, y*normFactor)
    tgraph.GetPoint(iPoint, x, y)
    print "normalized value is %f" % y

costhFile = TFile("optplots_nMinus1_withBtag_dd/nMinus1_stack_cosThetaStar_'down'.root")
#print "costhFile:",
#print costhFile
iKey = 0
for key in costhFile.GetListOfKeys():
  key.SetName("%i"%iKey)
  iKey+=1
  if "TCanvas" in costhFile.Get(key.GetName()).IsA().GetName():
    costhCan = costhFile.Get(key.GetName())
costhGraphs = []
for prim in costhCan.GetListOfPrimitives():
  print "costhCan prim:"
  print prim.GetName()
  if "ratio" in prim.GetName():
    costhPadName = prim.GetName()
costhPad = costhCan.GetPrimitive(costhPadName)
costhGraphNames=[]
for padprim in costhPad.GetListOfPrimitives():
  print "costhPad prim:"
  print padprim.GetName()
  if "TGraph" in padprim.IsA().GetName():
    print "this one is a TGraph"
    print padprim.GetName()
    costhGraphs.append(padprim)
    normalizeGraphTo(costhGraphs[-1], "cosThetaStar", 100)
    costhGraphNames.append(padprim.GetName())

#costhGraph=costhPad.GetPrimitive(costhGraphNames[-1])
#drawInNewCanvas(costhGraph)


ptmgjFile = TFile("optplots_nMinus1_withBtag_dd/nMinus1_stack_phPtOverMgammaj_'up'.root")
#ptmgjCan = ptmgjFile.Get("c1_n21")
print "ptmgjFile:",
print ptmgjFile
iKey=0
for key in ptmgjFile.GetListOfKeys():
  key.SetName("%i"%iKey)
  iKey+=1
  if "TCanvas" in ptmgjFile.Get(key.GetName()).IsA().GetName():
    ptmgjCan = ptmgjFile.Get(key.GetName())
ptmgjGraphs = []
for prim in ptmgjCan.GetListOfPrimitives():
  print prim.GetName()
  if "ratio" in prim.GetName():
    ptmgjPadName = prim.GetName()
ptmgjPad = ptmgjCan.GetPrimitive(ptmgjPadName)
ptmgjGraphNames = []
for padprim in ptmgjPad.GetListOfPrimitives():
  print padprim
  if "TGraph" in padprim.IsA().GetName():
    print "this one is a TGraph"
    print padprim.GetName()
    ptmgjGraphs.append(padprim)
    normalizeGraphTo(ptmgjGraphs[-1], "pToverM", 100)
    ptmgjGraphNames.append(padprim.GetName())

#ptmgjGraph=ptmgjPad.GetPrimitive(ptmgjGraphNames[-1])
#drawInNewCanvas(ptmgjGraph)


canvas = TCanvas("comparison", "cos(#theta*) vs. p_{T}^{#gamma}/m_#gammaj cut optimization")
canvas.cd()
print ptmgjGraphs
print costhGraphs
ptmgjGraphs[2].Draw()
ptmgjGraphs[2].GetXaxis().SetLimits(0, 1.05)
#ptmgjGraphs[2].Draw("SAME")
ptmgjGraphs[3].Draw("SAME")
costhGraphs[2].Draw("SAME")
costhGraphs[3].Draw("SAME")
##ptmgjGraphs[0].SetLineColor(kGreen+3)
##ptmgjGraphs[0].SetFillColor(kWhite)
##ptmgjGraphs[0].GetXaxis().SetTitleSize(0.04)
##ptmgjGraphs[0].GetXaxis().SetTitleOffset(1.2)
##ptmgjGraphs[0].GetYaxis().SetTitleSize(0.04)
##ptmgjGraphs[0].GetYaxis().SetLabelSize(0.04)
##ptmgjGraphs[0].GetXaxis().SetLabelSize(0.04)
##ptmgjGraphs[0].GetYaxis().SetTitleOffset(1.2)
##ptmgjGraphs[1].SetTitle("p_{T}^{#gamma}/m_{#gammaj} cut, M750")
##ptmgjGraphs[1].SetLineColor(kSpring-8)
##ptmgjGraphs[1].SetFillColor(kWhite)
##ptmgjGraphs[0].SetTitle("p_{T}^{#gamma}/m_{#gammaj} cut, M1000")
##
##costhGraphs[0].SetLineColor(kRed+3)
##costhGraphs[1].SetTitle("cos(#theta*) cut, M750")
##costhGraphs[0].SetFillColor(kWhite)
##costhGraphs[1].SetLineColor(kRed-4)
##costhGraphs[0].SetTitle("cos(#theta*) cut, M1000")
##costhGraphs[1].SetFillColor(kWhite)
ptmgjGraphs[2].SetLineColor(kGreen+3)
ptmgjGraphs[2].SetFillColor(kWhite)
ptmgjGraphs[2].GetXaxis().SetTitleSize(0.04)
ptmgjGraphs[2].GetXaxis().SetTitleOffset(1.2)
ptmgjGraphs[2].GetYaxis().SetTitleSize(0.04)
ptmgjGraphs[2].GetYaxis().SetLabelSize(0.04)
ptmgjGraphs[2].GetXaxis().SetLabelSize(0.04)
ptmgjGraphs[2].GetYaxis().SetTitleOffset(1.2)
ptmgjGraphs[3].SetTitle("p_{T}^{#gamma}/m_{#gammaj} cut, M750")
ptmgjGraphs[3].SetLineColor(kSpring-8)
ptmgjGraphs[3].SetFillColor(kWhite)
ptmgjGraphs[2].SetTitle("p_{T}^{#gamma}/m_{#gammaj} cut, M1000")

costhGraphs[2].SetLineColor(kRed+3)
costhGraphs[3].SetTitle("cos(#theta*) cut, M750")
costhGraphs[2].SetFillColor(kWhite)
costhGraphs[3].SetLineColor(kRed-4)
costhGraphs[2].SetTitle("cos(#theta*) cut, M1000")
costhGraphs[3].SetFillColor(kWhite)
canvas.BuildLegend()

