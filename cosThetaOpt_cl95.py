from ROOT import *
from recheckOptimization import MCbgGetSoverRootB
from HgParameters import getMassWindows, getSamplesDirs
from calcCL95limits import getExpectedLimit

massWindows = getMassWindows()
samplesDirs = getSamplesDirs()

def scanCuts(mass, graph, compileOrLoad):
  for i in range(0, 160):
    cutValue = 0.2 + (i/float(200))
    #bgMCsOverRootBinfo = MCbgGetSoverRootB(samplesDirs["small3sDir"], samplesDirs["ddDir", mass, massWindows[mass], 0.9, cosThetaCutValue, compileOrLoad)
    #ss = bgMCsOverRootBinfo["S"]
    #bb = bgMCsOverRootBinfo["B"]
    expectedLimitInfo = getExpectedLimit(samplesDirs["small3sDir"], samplesDirs["ddDir"], mass, massWindows[mass], 0.9, cutValue, compileOrLoad)
    graph.SetPoint(graph.GetN(), cutValue, expectedLimitInfo["expectedLimit"])
    compileOrLoad = "load"
    outfile = TFile("graph_m%i.root"%mass, "RECREATE")
    outfile.cd()
    graph.Write()
    outfile.Close()
  return compileOrLoad

    

graphs = []
compileOrLoad = "compile"
first = True
gStyle.SetPalette(kRainBow)
canvas = TCanvas()
canvas.cd()
iColor = 0
for mass in massWindows.keys():
  graphs.append(TGraph())
  graphs[-1].SetNameTitle("M=%i GeV" % mass, "M=%i GeV" % mass)
  graphs[-1].SetLineColor(kRed+iColor)
  iColor +=1
  compileOrLoad = scanCuts(mass, graphs[-1], compileOrLoad)
  if first:
    graphs[-1].Draw()
    first = False
  else:
    graphs[-1].Draw("SAME")
  
canvas.Draw()
canvas.SaveAs("testcanvas.pdf")
