from ROOT import *
from math import sqrt
from tcanvasTDR import TDRify
tfile=[]
tfile.append(TFile("~/oct31/rebinnedPdfs_antibtag.root"))
tfile.append(TFile("~/oct31/rebinnedPdfs_btag.root"))
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
antiErrUp = TGraph()
antiErrUpArr = []
antiErrLo = TGraph()
antiErrLoArr = []
btagErrUp = TGraph()
btagErrUpArr = []
btagErrLo = TGraph()
btagErrLoArr = []
x = Double()
y = Double()
for iPoint in range(0, antiCurve.GetN()+5):
  antiCurve.GetPoint(iPoint, x, y)
  antiErrUpArr.append((float(x), float(y)+sqrt(float(y))))
  antiErrUp.SetPoint(antiErrUp.GetN(), x, float(y)+sqrt(float(y)))
  antiErrLoArr.append((float(x), float(y)-sqrt(float(y))))
  antiErrLo.SetPoint(antiErrLo.GetN(), x, float(y)-sqrt(float(y)))
for iPoint in range(0, btagCurve.GetN()+5):
  btagCurve.GetPoint(iPoint, x, y)
  btagErrUpArr.append((float(x), float(y)+sqrt(float(y))))
  btagErrUp.SetPoint(btagErrUp.GetN(), x, float(y)+sqrt(float(y)))
  btagErrLoArr.append((float(x), float(y)-sqrt(float(y))))
  btagErrLo.SetPoint(btagErrLo.GetN(), x, float(y)-sqrt(float(y)))

antiCan = TCanvas()
antiCan.cd()
anti.Draw()
antiFit.cd()
antiErrUp.Draw("P")
antiErrLo.Draw("P")
n=antiErrUp.GetN()
antiErrShade = TGraph(2*n)
for i in range (0, antiErrUp.GetN()):
  antiErrShade.SetPoint(i,antiErrUpArr[i][0],antiErrUpArr[i][1]);
  antiErrShade.SetPoint(n+i,antiErrLoArr[n-i-1][0],antiErrLoArr[n-i-1][1]);
antiErrShade.Draw("f")
antiErrShade.SetFillColorAlpha(kBlack,0.2)
TDRify(antiFit, False, "antiFit")
antiRatio = anti.GetPrimitive("ratioPad_antibtag")
antiRatio.cd()
TDRify(antiRatio, True, "antiRatio")


btagCan = TCanvas()
btagCan.cd()
btag.Draw()
btagFit.cd()
btagErrUp.Draw("P")
btagErrLo.Draw("P")
n=btagErrUp.GetN()
btagErrShade = TGraph(2*n)
for i in range (0, btagErrUp.GetN()):
  btagErrShade.SetPoint(i,btagErrUpArr[i][0],btagErrUpArr[i][1]);
  btagErrShade.SetPoint(n+i,btagErrLoArr[n-i-1][0],btagErrLoArr[n-i-1][1]);
btagErrShade.Draw("f")
btagErrShade.SetFillColorAlpha(kBlack,0.2)
TDRify(btagFit, False, "btagFit")
btagRatio = btag.GetPrimitive("ratioPad_btag")
btagRatio.cd()
TDRify(btagRatio, True, "btagRatio")
