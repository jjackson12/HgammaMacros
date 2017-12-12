from ROOT import *
from math import sqrt
from tcanvasTDR import TDRify


tfile=[]
tfile.append(TFile("/Users/johakala/dec11/forErrs/rebinnedPdfs_antibtag.root"))
tfile.append(TFile("/Users/johakala/dec11/forErrs/rebinnedPdfs_btag.root"))
anti = tfile[0].Get("masterCan_antibtag")
antiFit = anti.GetPrimitive("dataFit_antibtag")
antiHist = antiFit.GetPrimitive("rebinned_fit")
antiHist.SetTitle("antibtag category") 
antiCurve = antiFit.GetPrimitive("bkg_dijetsimple2_Norm[x]")
antiCurve.SetTitle("dijet2 fit")
btag = tfile[1].Get("masterCan_btag")
btagFit = btag.GetPrimitive("dataFit_btag")
btagHist = btagFit.GetPrimitive("rebinned_fit")
btagHist.SetTitle("btag category") 
btagCurve = btagFit.GetPrimitive("bkg_dijetsimple2_Norm[x]")
btagCurve.SetTitle("dijet2 fit")

antiErrFile = TFile("fitRes_antibtag.root")
btagErrFile = TFile("fitRes_btag.root")

btagErrCan = btagErrFile.Get("c1")
btagErrorCurves = []
for prim in btagErrCan.GetListOfPrimitives():
  print prim.GetName()
  if "errorband" in prim.GetName():
    btagErrorCurves.append(prim)

for btagErrorCurve in btagErrorCurves:
  for i in range(0, btagErrorCurve.GetN()):
    btagErrorCurve.GetY()[i] *= 50 # the rebin factor

btagCan = TCanvas()
btagCan.cd()
btag.Draw()
btagFit.cd()
btagErrorCurves[0].SetFillColor(kOrange)
btagErrorCurves[0].Draw("f")
btagErrorCurves[1].SetFillColor(kGreen+2)
btagErrorCurves[1].Draw("f")

TDRify(btagFit, False, "btagFit")
btagRatio = btag.GetPrimitive("ratioPad_btag")
btagRatio.cd()
TDRify(btagRatio, True, "btagRatio")

antiErrCan = antiErrFile.Get("c1")
antiErrorCurves = []
for prim in antiErrCan.GetListOfPrimitives():
  if "errorband" in prim.GetName():
    antiErrorCurves.append(prim)

for antiErrorCurve in antiErrorCurves:
  for i in range(0, antiErrorCurve.GetN()):
    antiErrorCurve.GetY()[i] *= 50 # the rebin factor

antiCan = TCanvas()
antiCan.cd()
anti.Draw()
antiFit.cd()
antiErrorCurves[0].SetFillColor(kOrange)
antiErrorCurves[0].Draw("f")
antiErrorCurves[1].SetFillColor(kGreen+2)
antiErrorCurves[1].Draw("f")


TDRify(antiFit, False, "antiFit")
antiRatio = anti.GetPrimitive("ratioPad_antibtag")
antiRatio.cd()
TDRify(antiRatio, True, "antiRatio")

antiFit.cd()
antiFit.GetPrimitive("bkg_dijetsimple2_Norm[x]").Draw("SAME")
antiFit.GetPrimitive("rebinned_fit").Draw("SAME PE")
for prim in antiFit.GetListOfPrimitives():
  print prim.GetName()
  print prim.IsA().GetName()
  print "-------"
btagFit.cd()
btagFit.GetPrimitive("bkg_dijetsimple2_Norm[x]").Draw("SAME")
btagFit.GetPrimitive("rebinned_fit").Draw("SAME PE")
for prim in btagFit.GetListOfPrimitives():
  print prim.GetName()
  print prim.IsA().GetName()
  print "-------"
