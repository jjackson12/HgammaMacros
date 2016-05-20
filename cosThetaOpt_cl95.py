from ROOT import *
from recheckOptimization import MCbgGetSoverRootB
from HgParameters import getMassWindows, getSamplesDirs
from calcCL95limits import getExpectedLimit

massWindows = getMassWindows()
samplesDirs = getSamplesDirs()
useCosTheta=False
usePtOverM = True

def scanCuts(mass, graph, compileOrLoad):
  for i in range(0, 70):
    cutValue = 0.3 + (i/float(100))
  #for i in range(0, 2):
  #  cutValue = 0.3 + (i/float(100))
    #bgMCsOverRootBinfo = MCbgGetSoverRootB(samplesDirs["small3sDir"], samplesDirs["ddDir", mass, massWindows[mass], -100.0, cosThetaCutValue, compileOrLoad)
    #ss = bgMCsOverRootBinfo["S"]
    #bb = bgMCsOverRootBinfo["B"]
    expectedLimitInfo = getExpectedLimit(samplesDirs["small3sDir"], samplesDirs["ddDir"], mass, massWindows[mass], -100.0, cutValue, 0, compileOrLoad)
    graph.SetPoint(graph.GetN(), cutValue, expectedLimitInfo["expectedLimit"])
    compileOrLoad = "load"
    outfile = TFile("noBtagCut_m%i.root"%mass, "RECREATE")
    outfile.cd()
    graph.Write()
    outfile.Close()
  return compileOrLoad

    
def scanCuts_ptOverM(mass, graph, compileOrLoad):
  for i in range(0, 60):
    pToverMcutValue = i/float(100)
    #bgMCsOverRootBinfo = MCbgGetSoverRootB(samplesDirs["small3sDir"], samplesDirs["ddDir", mass, massWindows[mass], -100.0, cosThetaCutValue, compileOrLoad)
    #ss = bgMCsOverRootBinfo["S"]
    #bb = bgMCsOverRootBinfo["B"]
    expectedLimitInfo = getExpectedLimit(samplesDirs["small3sDir"], samplesDirs["ddDir"], mass, massWindows[mass], -100.0, 2, pToverMcutValue, compileOrLoad)
    graph.SetPoint(graph.GetN(), pToverMcutValue, expectedLimitInfo["expectedLimit"])
    compileOrLoad = "load"
    outfile = TFile("noBtag_pToverM_m%i.root"%mass, "RECREATE")
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
massWindows.pop(750)
massWindows.pop(1000)
for mass in massWindows.keys():
  graphs.append(TGraph())
  graphs[-1].SetNameTitle("M=%i GeV" % mass, "M=%i GeV" % mass)
  graphs[-1].SetLineColor(kRed+iColor)
  iColor +=1
  if useCosTheta:
    compileOrLoad = scanCuts(mass, graphs[-1], compileOrLoad)
  elif usePtOverM:
    compileOrLoad = scanCuts_ptOverM(mass, graphs[-1], compileOrLoad)
  if first:
    graphs[-1].Draw()
    first = False
  else:
    graphs[-1].Draw("SAME")
  
canvas.Draw()
canvas.SaveAs("testcanvas.pdf")
