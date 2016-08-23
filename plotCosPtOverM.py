from ROOT import *
from pyrootTools import drawInNewCanvas



costhFile = TFile("optplots_nMinus1_withBtag/nMinus1_stack_cosThetaStar_'down'.root")
costhCan = costhFile.Get("c1_n9")
costhGraphs = []
for prim in costhCan.GetListOfPrimitives():
  print prim.GetName()
  if "ratio" in prim.GetName():
    costhPadName = prim.GetName()
costhPad = costhCan.GetPrimitive(costhPadName)
costhGraphNames=[]
for padprim in costhPad.GetListOfPrimitives():
  print padprim
  if "TGraph" in padprim.IsA().GetName():
    print padprim.GetName()
    costhGraphs.append(padprim)

#costhGraph=costhPad.GetPrimitive(costhGraphName)
#drawInNewCanvas(costhGraph)


ptmgjFile = TFile("optplots_nMinus1_withBtag/nMinus1_stack_phPtOverMgammaj_'up'.root")
ptmgjCan = ptmgjFile.Get("c1_n21")
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
    print padprim.GetName()
    ptmgjGraphs.append(padprim)

#ptmgjGraph=ptmgjPad.GetPrimitive(ptmgjGraphName)
#drawInNewCanvas(ptmgjGraph)


canvas = TCanvas("comparison", "cos(#theta*) vs. p_{T}^{#gamma}/m_#gammaj cut optimization")
canvas.cd()
print ptmgjGraphs
print costhGraphs
ptmgjGraphs[0].Draw()
ptmgjGraphs[0].GetXaxis().SetLimits(0, 1.05)
ptmgjGraphs[1].Draw("SAME")
costhGraphs[0].Draw("SAME")
costhGraphs[1].Draw("SAME")
ptmgjGraphs[0].SetLineColor(kGreen+3)
ptmgjGraphs[0].SetFillColor(kWhite)
ptmgjGraphs[0].GetXaxis().SetTitleSize(0.04)
ptmgjGraphs[0].GetXaxis().SetTitleOffset(1.2)
ptmgjGraphs[0].GetYaxis().SetTitleSize(0.04)
ptmgjGraphs[0].GetYaxis().SetLabelSize(0.04)
ptmgjGraphs[0].GetXaxis().SetLabelSize(0.04)
ptmgjGraphs[0].GetYaxis().SetTitleOffset(1.2)
ptmgjGraphs[1].SetTitle("cos(#theta*) cut, M750")
ptmgjGraphs[1].SetLineColor(kSpring-8)
ptmgjGraphs[1].SetFillColor(kWhite)
ptmgjGraphs[0].SetTitle("cos(#theta*) cut, M1000")

costhGraphs[0].SetLineColor(kRed+3)
costhGraphs[1].SetTitle("p_{T}^{#gamma}/m_{#gammaj} cut, M750")
costhGraphs[0].SetFillColor(kWhite)
costhGraphs[1].SetLineColor(kRed-4)
costhGraphs[0].SetTitle("p_{T}^{#gamma}/m_{#gammaj} cut, M1000")
costhGraphs[1].SetFillColor(kWhite)
canvas.BuildLegend()
