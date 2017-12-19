from os import path, makedirs
from pprint import pprint
from sympy.solvers import solve
from sympy import Symbol, erf
from ROOT import *
from HgCuts import *


can = TCanvas()
can.cd()

graph = TGraph()

useWeightFactors=True
outDir = "turnOns_functions_"
if useWeightFactors:
  outDir += "_withWeightFactors"
else:
  outDir += "_noWeightFactors"
if not path.exists(outDir):
  makedirs(outDir)
  

inFile = TFile("organize_DDs_btag-nom/data/ddTree_data2016SinglePhoton.root")
#inFile = TFile("organize_DDs_btag-nom/backgrounds/ddTree_gJets400To600.root")
tree = inFile.Get("higgs")
hist = TH1F("hist", "m_{j#gamma}", 500, 0, 5000)
hist.GetXaxis().SetRangeUser(400, 1400)
jetMassWindows = []
turnOns=[]

x = Symbol("x")

for i in range(0,16):
  jetMassWindows.append([30.0+10*i, 40.0+10*i])
jetMassWindows.append([110.0,140.0])
for jetMassWindow in jetMassWindows:
  hist.SetTitle("m_{j#gamma}, %i GeV < m_{j} < %i GeV" % (int(jetMassWindow[0]), int(jetMassWindow[1])))
  if useWeightFactors:
    cut ="weightFactor*(%s)" % getNoBtagComboCut("higgs", True, True, jetMassWindow)
  else:
    cut = getNoBtagComboCut("higgs", True, True, jetMassWindow)
  #print cut
  tree.Draw("phJetInvMass_puppi_softdrop_higgs >>hist", cut)
  
  fit = TF1("fit", "[0]*TMath::Exp([1]*x-[2])*(0.5+0.5*TMath::Erf((x-[3])/[4]))", 0, 13000)
  fit.SetParameters(1.8, -3.3e-3, -8.7, 600, 100)
  for i in range(0, 10):
    result = hist.Fit(fit, "SMLQ", "", 500, 2500)
  print "result of fit:", result.IsValid()
  if not result.IsValid():
    fit.SetParameters(3.4, -6.1e-3, -8.9, 515, 59)
    result = hist.Fit(fit, "SLQ", "", 500, 2500)
    print "result of fit, second try:", result.IsValid()
   

  erfComponent = TF1("erf", "[0]*(0.5+0.5*TMath::Erf((x-[1])/[2]))", 0, 13000)
  erfComponent.SetParameters(fit.GetMaximum(), fit.GetParameter(3), fit.GetParameter(4))
  erfComponent.SetLineColor(kGray)
  erfComponent.SetLineStyle(7)
  expComponent = TF1("exp", "[0]*TMath::Exp([1]*x-[2])", 0, 13000)
  expComponent.SetParameters(fit.GetParameter(0), fit.GetParameter(1), fit.GetParameter(2))
  expComponent.SetLineColor(kGray+2)
  expComponent.SetLineStyle(7)
  erfComponent.Draw("SAME")
  expComponent.Draw("SAME")
  gStyle.SetOptFit(0)
  gStyle.SetOptStat(0)
  #for prim in can.GetListOfPrimitives():
  #  if hasattr(prim, 'GetName'):
  #    print prim.GetName()
  print "solution for mass window", jetMassWindow, ":"
  solution = solve(-0.99 + 0.5 + 0.5*(erf((x-fit.GetParameter(3))/fit.GetParameter(4))), x)
  print solution
  if len(solution) == 1:
    if jetMassWindow[1]-jetMassWindow[0] == 10:
      graph.SetPoint(graph.GetN(), (jetMassWindow[0]+jetMassWindow[1])/float(2), solution[0])
  else:
    print "... did not get exactly one solution for this mass window"
  turnOns.append(([jetMassWindow[0],jetMassWindow[1]], solution[0]))
  line = TLine(solution[0], 0, solution[0], can.GetFrame().GetY2())
  line.SetLineColor(kBlack)
  line.Draw("SAME")
  text = TPaveText(solution[0]+can.GetFrame().GetX2()/16., can.GetFrame().GetY2()/12., solution[0]+can.GetFrame().GetX2()/16. , can.GetFrame().GetY2()/12.)
  text.AddText("m_{j\gamma}=%01d GeV" % solution[0])
  text.SetTextSize(0.03)
  text.Draw("SAME")
  can.Print(path.join(outDir, "turnOn_%i-%i.pdf" % (int(jetMassWindow[0]), int(jetMassWindow[1]))))
  

can2=TCanvas()
can2.cd()
graph.Draw()
can2.Print(path.join(outDir, "turnOnGraph.pdf"))

pprint(turnOns)
