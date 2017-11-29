from ROOT import *
from math import sqrt
from tcanvasTDR import TDRify
from fitResultHelpers import getVarsAndCorrMatrix

def makeErrBandFunc(category):
  formula = "[0]*TMath::Power(x,[1]+[2]*log(x))"

  formulaVar  = "TMath::Max(TMath::Max([8]*TMath::Power(x,[0]+[1]*log(x)), [9]*TMath::Power(x,[2]+[3]*log(x))), TMath::Max([10]*TMath::Power(x,[4]+[5]*log(x)), [11]*TMath::Power(x,[6]+[7]*log(x))))"
  formulaNom = "[12]*TMath::Power(x,[13]+[14]*log(x))"
  formulaMax ="TMath::Max(%s,  %s)" % (formulaVar, formulaNom)
  formulaVar2  = "TMath::Min(TMath::Min([8]*TMath::Power(x,[0]+[1]*log(x)), [9]*TMath::Power(x,[2]+[3]*log(x))), TMath::Min([10]*TMath::Power(x,[4]+[5]*log(x)), [11]*TMath::Power(x,[6]+[7]*log(x))))"
  formulaMin = "TMath::Min(%s, %s)" % (formulaVar2, formulaNom)
  if "antibtag" in category:
    #par1nom = 18.111653339379174
    #par1err = .150063
    #par2nom = -1.693887532216388
    #par2err = .0127796

    par1, par2, correlationMatrix = getVarsAndCorrMatrix("fitRes_antibtag.root")
    #par1nom = par1["val"]
    par1nom = 18.111653339379174
    par1errHi = par1["errHi"]
    par1errLo = par1["errLo"]
    #par1errHi = (par1["errHi"] - par1["errLo"])/float(2)
    #par1errLo = -(par1["errHi"] - par1["errLo"])/float(2)
    #par2nom = par2["val"]
    par2nom = -1.693887532216388
    par2errHi = par2["errHi"]
    par2errLo = par2["errLo"]
    #par2errHi = (par2["errHi"] - par2["errLo"])/ float(2)
    #par2errLo = -(par2["errHi"] - par2["errLo"])/ float(2)
    normNom = 4578.193317770958
    normErr = 67.6623480482
    normHiNom = normNom+normErr
    normLoNom = normNom-normErr
    rebin=50    
  else:
    #par1nom = 30.772208177849887
    #par1err = 0.0181290*par1nom
    #par2nom = -2.5224772757037215
    #par2err = 0.018*par2nom
    par1, par2, correlationMatrix = getVarsAndCorrMatrix("fitRes_btag.root")
    #par1nom = par1["val"]
    par1nom = 30.772208177849887
    par1errHi = par1["errHi"]
    par1errLo = par1["errLo"]
    #par1errHi = (par1["errHi"] - par1["errLo"])/float(2)
    #par1errLo = -(par1["errHi"] - par1["errLo"])/float(2)
    #par2nom = par2["val"]
    par2nom = -2.5224772757037215
    par2errHi = par2["errHi"]
    par2errLo = par2["errLo"]
    #par2errHi = (par2["errHi"] - par2["errLo"])/ float(2)
    #par2errLo = -(par2["errHi"] - par2["errLo"])/ float(2)
    normNom = 79.35249078273773
    normErr = 8.90800153006
    normHiNom = normNom+normErr
    normLoNom = normNom-normErr
    rebin=50

  fitNom = TF1("nom", formula, 700, 4700)
  fitNom.SetParameters(1, par1nom, par2nom)
  fitInt = fitNom.Integral(700, 4700)
  fitTmp = TF1("nom", formula, 700, 4700)

  # upper error band
  fitMax = TF1("max", formulaMax, 700, 4700)
  # first piece: p1 goes up by 1
  fitMax.SetParameter(0, par1nom+par1errHi)
  fitMax.SetParameter(1, par2nom+par2errHi*correlationMatrix[0][1] if correlationMatrix[0][1] > 0 else par2nom-par2errLo*correlationMatrix[0][1] )
  # second piece: p1 goes down by 1
  fitMax.SetParameter(2, par1nom+par1errLo)
  fitMax.SetParameter(3, par2nom+par2errLo*correlationMatrix[0][1] if correlationMatrix[0][1] > 0 else par2nom-par2errHi*correlationMatrix[0][1])
  # third piece: p2 goes up by 1
  fitMax.SetParameter(4, par1nom+par1errHi*correlationMatrix[1][0] if correlationMatrix[1][0] > 0 else par1nom-par1errLo*correlationMatrix[1][0])
  fitMax.SetParameter(5, par2nom+par2errHi)
  # fourth piece: p2 goes down by 1
  fitMax.SetParameter(6, par1nom+par1errLo*correlationMatrix[1][0] if correlationMatrix[1][0] > 0 else par1nom-par1errHi*correlationMatrix[1][0])
  fitMax.SetParameter(7, par2nom+par2errLo)
  
  fitTmp.SetParameters(1, par1nom+par1errHi, par2nom+par2errHi*correlationMatrix[0][1] if correlationMatrix[0][1] > 0 else par2nom-par2errLo*correlationMatrix[0][1])
  piece1norm = (rebin*normHiNom)/fitTmp.Integral(700, 4700)
  fitMax.SetParameter(8, piece1norm)
  
  fitTmp.SetParameters(1, par1nom+par1errLo, par2nom+par2errLo*correlationMatrix[0][1] if correlationMatrix[0][1] > 0 else par2nom-par2errHi*correlationMatrix[0][1])
  piece2norm = (rebin*normHiNom)/fitTmp.Integral(700, 4700)
  fitMax.SetParameter(9, piece2norm )
  
  
  fitTmp.SetParameters(1, par1nom+par1errHi*correlationMatrix[1][0] if correlationMatrix[1][0] > 0 else par1nom-par1errLo*correlationMatrix[1][0], par2nom+par2errHi)
  piece3norm = (rebin*normHiNom)/fitTmp.Integral(700, 4700)
  fitMax.SetParameter(10, piece3norm)
  
  fitTmp.SetParameters(1, par1nom+par1errLo*correlationMatrix[1][0] if correlationMatrix[1][0] > 0 else par1nom-par1errHi*correlationMatrix[1][0], par2nom+par2errLo)
  piece4norm = (rebin*normHiNom)/fitTmp.Integral(700, 4700)
  fitMax.SetParameter(11, piece4norm )
  
  fitMax.SetParameter(12, (rebin*normHiNom)/fitInt)
  fitMax.SetParameter(13, par1nom)
  fitMax.SetParameter(14, par2nom)
  
  fitMax.SetLineColor(kGreen)
  
  # lower error band
  fitMin = TF1("min", formulaMin, 700, 4700)
  # first piece: p1 goes up by 1
  fitMin.SetParameter(0, par1nom+par1errHi)
  fitMin.SetParameter(1, par2nom+par2errHi*correlationMatrix[0][1] if correlationMatrix[0][1] > 0 else par2nom-par2errLo*correlationMatrix[0][1] )
  # second piece: p1 goes down by 1
  fitMin.SetParameter(2, par1nom+par1errLo)
  fitMin.SetParameter(3, par2nom+par2errLo*correlationMatrix[0][1] if correlationMatrix[0][1] > 0 else par2nom-par2errHi*correlationMatrix[0][1])
  # third piece: p2 goes up by 1
  fitMin.SetParameter(4, par1nom+par1errHi*correlationMatrix[1][0] if correlationMatrix[1][0] > 0 else par1nom-par1errLo*correlationMatrix[1][0])
  fitMin.SetParameter(5, par2nom+par2errHi)
  # fourth piece: p2 goes down by 1
  fitMin.SetParameter(6, par1nom+par1errLo*correlationMatrix[1][0] if correlationMatrix[1][0] > 0 else par1nom-par1errHi*correlationMatrix[1][0])
  fitMin.SetParameter(7, par2nom+par2errLo)
  
  fitTmp.SetParameters(1, par1nom+par1errHi, par2nom+par2errHi*correlationMatrix[0][1] if correlationMatrix[0][1] > 0 else par2nom-par2errLo*correlationMatrix[0][1])
  piece1norm = (rebin*normLoNom)/fitTmp.Integral(700, 4700)
  fitMin.SetParameter(8, piece1norm)
  
  fitTmp.SetParameters(1, par1nom+par1errLo, par2nom+par2errLo*correlationMatrix[0][1] if correlationMatrix[0][1] > 0 else par2nom-par2errHi*correlationMatrix[0][1])
  piece2norm = (rebin*normLoNom)/fitTmp.Integral(700, 4700)
  fitMin.SetParameter(9, piece2norm )
  
  
  fitTmp.SetParameters(1, par1nom+par1errHi*correlationMatrix[1][0] if correlationMatrix[1][0] > 0 else par1nom-par1errLo*correlationMatrix[1][0], par2nom+par2errHi)
  piece3norm = (rebin*normLoNom)/fitTmp.Integral(700, 4700)
  fitMin.SetParameter(10, piece3norm)
  
  fitTmp.SetParameters(1, par1nom+par1errLo*correlationMatrix[1][0] if correlationMatrix[1][0] > 0 else par1nom-par1errHi*correlationMatrix[1][0], par2nom+par2errLo)
  piece4norm = (rebin*normLoNom)/fitTmp.Integral(700, 4700)
  fitMin.SetParameter(11, piece4norm )
  
  fitMin.SetParameter(12, (rebin*normLoNom)/fitInt)
  fitMin.SetParameter(13, par1nom)
  fitMin.SetParameter(14, par2nom)
  
  fitMin.SetLineColor(kRed)

  return {"min" : fitMin, "max" : fitMax}
  #return {"max" : fitMax}

btagErrs = makeErrBandFunc("btag")
antiErrs = makeErrBandFunc("antibtag")

btagCan = TCanvas()
btagCan.cd()
btagErrs['max'].Draw()
btagErrs['min'].Draw("SAME")

antiCan = TCanvas()
antiCan.cd()
antiErrs['max'].Draw()
antiErrs['min'].Draw("SAME")


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
antiErr2Up = TGraph()
antiErrUpArr = []
antiErr2UpArr = []
antiErrLo = TGraph()
antiErr2Lo = TGraph()
antiErrLoArr = []
antiErr2LoArr = []
btagErrUp = TGraph()
btagErr2Up = TGraph()
btagErrUpArr = []
btagErr2UpArr = []
btagErrLo = TGraph()
btagErr2Lo = TGraph()
btagErrLoArr = []
btagErr2LoArr = []
x = Double()
y = Double()
for iPoint in range(0, antiCurve.GetN()+5):
  antiCurve.GetPoint(iPoint, x, y)
  antiErrUpArr.append((float(x), antiErrs['max'].Eval(float(x))))
  antiErrUp.SetPoint(antiErrUp.GetN(), x, antiErrs['max'].Eval(float(x)))
  antiErrLoArr.append((float(x), antiErrs['min'].Eval(float(x))))
  antiErrLo.SetPoint(antiErrLo.GetN(), x, antiErrs['min'].Eval(float(x)))
for iPoint in range(0, btagCurve.GetN()+5):
  btagCurve.GetPoint(iPoint, x, y)
  btagErrUpArr.append((float(x), btagErrs['max'].Eval(float(x))))
  btagErrUp.SetPoint(btagErrUp.GetN(), x, btagErrs['max'].Eval(float(x)))
  btagErrLoArr.append((float(x), btagErrs['min'].Eval(float(x))))
  btagErrLo.SetPoint(btagErrLo.GetN(), x, btagErrs['min'].Eval(float(x)))
for iPoint in range(0, antiCurve.GetN()+5):
  antiCurve.GetPoint(iPoint, x, y)
  antiErr2UpArr.append((float(x), y+2*(antiErrs['max'].Eval(float(x))-y)))
  antiErr2Up.SetPoint(antiErr2Up.GetN(), x, y+2*(antiErrs['max'].Eval(float(x))-y))
  antiErr2LoArr.append((float(x), y-2*(y-antiErrs['min'].Eval(float(x)))))
  antiErr2Lo.SetPoint(antiErr2Lo.GetN(), x, y-2*(y-antiErrs['min'].Eval(float(x))))
for iPoint in range(0, btagCurve.GetN()+5):
  btagCurve.GetPoint(iPoint, x, y)
  btagErr2UpArr.append((float(x), y+2*(btagErrs['max'].Eval(float(x))-y)))
  btagErr2Up.SetPoint(btagErr2Up.GetN(), x, y+2*(btagErrs['max'].Eval(float(x))-y))
  btagErr2LoArr.append((float(x), y-2*(y-btagErrs['min'].Eval(float(x)))))
  btagErr2Lo.SetPoint(btagErr2Lo.GetN(), x, y-2*(y-btagErrs['min'].Eval(float(x))))

antiCan = TCanvas()
antiCan.cd()
anti.Draw()
antiFit.cd()
antiErrUp.Draw("P")
antiErrLo.Draw("P")
n=antiErrUp.GetN()
antiErrShade = TGraph(2*n)
antiErr2Shade = TGraph(2*n)
for i in range (0, antiErrUp.GetN()):
  antiErrShade.SetPoint(i,antiErrUpArr[i][0],antiErrUpArr[i][1]);
  antiErrShade.SetPoint(n+i,antiErrLoArr[n-i-1][0],antiErrLoArr[n-i-1][1]);
for i in range (0, antiErr2Up.GetN()):
  antiErr2Shade.SetPoint(i,antiErr2UpArr[i][0],antiErr2UpArr[i][1]);
  antiErr2Shade.SetPoint(n+i,antiErr2LoArr[n-i-1][0],antiErr2LoArr[n-i-1][1]);
antiErr2Shade.Draw("f")
antiErr2Shade.SetFillColor(kOrange)
antiErrShade.Draw("f")
antiErrShade.SetFillColor(kGreen+2)
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
btagErr2Shade = TGraph(2*n)
for i in range (0, btagErrUp.GetN()):
  btagErrShade.SetPoint(i,btagErrUpArr[i][0],btagErrUpArr[i][1]);
  btagErrShade.SetPoint(n+i,btagErrLoArr[n-i-1][0],btagErrLoArr[n-i-1][1]);
for i in range (0, btagErr2Up.GetN()):
  btagErr2Shade.SetPoint(i,btagErr2UpArr[i][0],btagErr2UpArr[i][1]);
  btagErr2Shade.SetPoint(n+i,btagErr2LoArr[n-i-1][0],btagErr2LoArr[n-i-1][1]);
btagErr2Shade.Draw("f")
btagErr2Shade.SetFillColor(kOrange)
btagErrShade.Draw("f")
btagErrShade.SetFillColor(kGreen+2)
TDRify(btagFit, False, "btagFit")
btagRatio = btag.GetPrimitive("ratioPad_btag")
btagRatio.cd()
TDRify(btagRatio, True, "btagRatio")

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
