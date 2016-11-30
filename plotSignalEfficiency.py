from ROOT import TFile, TGraph, TCanvas
from HgParameters import getNormalizations
from checkSignalEfficiency import getSignalEfficiencies

massWindowToCheck = [110, 140]
#massWindowToCheck = [90, 150]

#signalEfficiencies = getSignalEfficiencies(massWindowToCheck)
#print signalEfficiencies
signalEfficiencies={}
with open("btagEffs.tx") as bf:
  lines = bf.readlines()
  for line in lines:
    lineparts = line.split(", ")
    signalEfficiencies["btag_%s"%str(lineparts[0])] = float(lineparts[1])
with open("antibtagEffs.tx") as af:
  lines = af.readlines()
  for line in lines:
    lineparts = line.split(", ")
    signalEfficiencies["antibtag_%s"%str(lineparts[0])] = float(lineparts[1])
print signalEfficiencies

##"plotting signal efficiencies for masswindow (%r, %r)" % (massWindowToCheck[0], massWindowToCheck[1])
outfile = TFile("efficienciesGraphs_masswindow_%r-%r.root"%(massWindowToCheck[0], massWindowToCheck[1]), "RECREATE")
outfile.cd()

canvases = []
graphs   = []



for category in ['btag', 'antibtag']:
  canvases.append(TCanvas())
  graphs.append(TGraph())
  graphs[-1].SetNameTitle("SigEff_%s" % category, "Signal efficiency, %s category" % category)
  graphs[-1].Draw()
  masses = getNormalizations()  
  print masses
  for mass in masses.keys():
    print "%r: %f" % (float(mass), signalEfficiencies["%s_%s"%(category, str(mass))])
    #graphs[-1].SetPoint(graphs[-1].GetN(), float(mass), signalEfficiencies[str(mass)][category])
    graphs[-1].SetPoint(graphs[-1].GetN(), float(mass), signalEfficiencies["%s_%s"%(category, str(mass))])
  graphs[-1].GetXaxis().SetTitle("Signal mass (GeV)")
  graphs[-1].GetYaxis().SetTitle("#varepsilon")
  graphs[-1].SetMarkerStyle(2)
  graphs[-1].Write() 
outfile.Close()


