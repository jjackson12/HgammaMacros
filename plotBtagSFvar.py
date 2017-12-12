from ROOT import *

varUpFile = TFile("btag-up_efficienciesGraphs_masswindow_110-140.root")
varDownFile = TFile("btag-down_efficienciesGraphs_masswindow_110-140.root")

upBtagGraph = varUpFile.Get("SigEff_btag")
downBtagGraph = varDownFile.Get("SigEff_btag")

diffGraph = TGraph()

xxUp = Double()
yyUp = Double()
xxDown = Double()
yyDown = Double()
for i in range(0, upBtagGraph.GetN()):
  upBtagGraph.GetPoint(i, xxUp, yyUp)
  downBtagGraph.GetPoint(i, xxDown, yyDown)
  if xxUp != xxDown:
    print "something is funky!"
    exit(1)
  if (xxUp >= 700):
    diffGraph.SetPoint(diffGraph.GetN(), xxUp, (yyUp-yyDown)/((yyUp+yyDown)/2))

can = TCanvas()
diffGraph.Draw()
errFunc = TF1("errFunc", "[0]*TMath::Erf((x-[1])/[2]) + [3]", 700, 3250)
errFunc.SetParameters(0.075, 1000, 500, .02)
for i in range(0, 10):
  diffGraph.Fit("errFunc", "M")
outFile = TFile("sigEff_btagVarDiff.root", "RECREATE")
can.Write()
outFile.Close()
