from ROOT import *

inFiles = { "up":   TFile("btag-up_efficienciesGraphs_masswindow_110-140.root"),
            "down": TFile("btag-down_efficienciesGraphs_masswindow_110-140.root") }

inGraphs = {}
for key in inFiles:
  inGraphs[key] = inFiles[key].Get("SigEff_btag")

print inGraphs


xx = Double()
yy = Double()
upX = Double()
upY = Double()
diffGraph = TGraph()

for iPoint in range(0, inGraphs["up"].GetN()):
  inGraphs["up"].GetPoint(iPoint, xx, yy)
  upX = Double(xx)
  upY = Double(yy)
  inGraphs["down"].GetPoint(iPoint, xx, yy)
  if not xx == upX:
    print "something's wrong!"
    exit(1)
  else:
    if not xx == 650:
      print "setting point (x, y) = (%f, %f)" % (upX, upY-yy)
      diffGraph.SetPoint(diffGraph.GetN(), upX, (upY-yy)/((upY+yy)/2))

outCan = TCanvas()
outCan.cd()
diffGraph.SetMarkerStyle(20)
diffGraph.SetTitle("double-b tagger systematic evaluation")
diffGraph.GetXaxis().SetTitle("m_{X} (GeV)")
diffGraph.GetYaxis().SetTitle("(#varepsilon_{up}-#varepsilon_{down})/#varepsilon_{nom}")
diffGraph.GetYaxis().SetTitleOffset(0.8)
diffGraph.GetYaxis().SetTitleSize(0.06)
diffGraph.GetYaxis().SetLabelSize(0.025)
diffGraph.Draw("AP")
