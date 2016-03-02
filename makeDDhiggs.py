from sys import argv
from os import path, makedirs
import subprocess
from math import sqrt
from ROOT import *

dataFile = TFile("ddTreeHiggs_silver_Feb26.root")

data          = dataFile.Get("higgs"     )
print "using sideband %s"%argv[3]
if (argv[3]=="100to110"):
    sidebandName = "side100110"
    sidebandIndex = "Four"
elif (argv[3]=="50to70"):
    sidebandName = "side5070"
    sidebandIndex = "Three"
else:
    exit("please pick the sideband range: either 100to110 or 50to70.")
sideLow = dataFile.Get(sidebandName)

phoEtaMax   = 1.4442
jetEtaMax   = 2.0
deltaRmin   = 1.1
cosThetaMax = 0.6

massWindowLo = 600
massWindowHi = 700

phoEtaCut           = TCut("leadingPhAbsEta<%s"               % str(phoEtaMax  ) )
cosThetaCut         = TCut("cosThetaStar<%s"                  % str(cosThetaMax) )
deltaRdataCut       = TCut("phJetDeltaR_higgs>%s"             % str(deltaRmin  ) )
deltaRsidebandCut   = TCut("phJetDeltaR_sideLow%s>%s"         % (sidebandIndex, str(deltaRmin)) )
jetEtaDataCut       = TCut("higgsJet_pruned_abseta<%s"        % str(jetEtaMax  ) )
jetEtaSidebandCut   = TCut("sideLow%sJet_pruned_abseta<%s"  % (sidebandIndex, str(jetEtaMax)) )

dataMassCuts         = TCut("(phJetInvMass_pruned_higgs>%s)&&(phJetInvMass_pruned_higgs<%s)"               % ( str(massWindowLo), str(massWindowHi) )    )
sidebandMassCuts     = TCut("(phJetInvMass_pruned_sideLow%s>%s)&&(phJetInvMass_pruned_sideLow%s<%s)" % (sidebandIndex, str(massWindowLo), sidebandIndex, str(massWindowHi) )    )

dataCuts     = TCut()
sidebandCuts = TCut()

dataCuts     += phoEtaCut + cosThetaCut + deltaRdataCut     + jetEtaDataCut     + dataMassCuts
sidebandCuts += phoEtaCut + cosThetaCut + deltaRsidebandCut + jetEtaSidebandCut + sidebandMassCuts


print "the cut string for the signal region is %s" % dataCuts
print "the cut string for the sideband region is %s" % sidebandCuts


c = TCanvas()
c.SetLogy()
data.Draw(argv[1], dataCuts)
for primitive in c.GetListOfPrimitives():
    primitive.SetName("data")
    primitive.SetLineColor(kBlack)
dataEntries = c.GetPrimitive("data").GetEntries()
print "data has %i entries" % dataEntries
sideLow.Draw(argv[2], sidebandCuts, "SAME")
for primitive in c.GetListOfPrimitives():
    if not primitive.GetName()=="data":
        primitive.SetName("sideband")
        primitive.SetBinErrorOption(TH1.kPoisson)
sidebandEntries = c.GetPrimitive("sideband").GetEntries()
print "sideband has %i entries" % sidebandEntries
sidebandNormalization = dataEntries/sidebandEntries
print "sideband normalization factor is %f" % sidebandNormalization
for sidebandBin in range (0, c.GetPrimitive("sideband").GetNbinsX()):
    c.GetPrimitive("sideband").SetBinContent(sidebandBin, c.GetPrimitive("sideband").GetBinContent(sidebandBin)*sidebandNormalization)
c.GetPrimitive("sideband").SetLineColor(kGreen)
c.Update()
c.Draw()
primitives = []
for primitive in c.GetListOfPrimitives():
    primitives.append(primitive.GetName())
#sig.Draw("higgsJet_pruned_abseta", dataCuts, "SAME")
#for primitive in c.GetListOfPrimitives():
#    print primitive
#    if not primitive.GetName() in primitives:
#        print "found new primitive with name %s" % primitive.GetName()
#        primitive.SetName("signal")
#        print "found updated primitive with name %s" % primitive.GetName()

ymax=0
for primitive in c.GetListOfPrimitives():
    if primitive.GetName() in ["sideband", "signal", "data"]:
        primitive.Rebin(5)
        if primitive.GetName()=="signal":
            for sigBin in range(0, c.GetPrimitive("signal").GetNbinsX()):
                c.GetPrimitive("signal").SetBinContent(sigBin, c.GetPrimitive("signal").GetBinContent(sigBin)*0.1)
        if primitive.GetMaximum()>ymax:
            ymax = primitive.GetMaximum()

for primitive in c.GetListOfPrimitives():
    if primitive.GetName() in ["sideband", "signal", "data"]:
        primitive.GetYaxis().SetRangeUser(1, ymax*3)

c.Draw()
c.Update()
c2 = TCanvas()
c2.cd()
c2.SetLogy()
c.GetPrimitive("sideband").SetLineColor(kOrange+2)
c.GetPrimitive("sideband").SetFillColor(kOrange)
c.GetPrimitive("sideband").Draw()
clone = c.GetPrimitive("sideband").Clone()
for sidebandBin in range (0, c.GetPrimitive("sideband").GetNbinsX()):
    clone.SetBinError(sidebandBin, c.GetPrimitive("sideband").GetBinError(sidebandBin)*sidebandNormalization)
clone.SetFillColor(kOrange-6)
clone.SetFillStyle(3017)
clone.Draw("ZE2 SAME")
c.GetPrimitive("data").SetMarkerStyle(20)
c.GetPrimitive("data").Draw("apE0 SAME")
#c.GetPrimitive("signal").SetLineWidth(3)
#c.GetPrimitive("signal").SetLineStyle(6)
#c.GetPrimitive("signal").Draw("SAME")
c2.Draw()

outputDirName="output_higgs_sideband%s_masswindow%i-%i"%(sidebandName, massWindowLo, massWindowHi)
if not path.exists(outputDirName):
      makedirs(outputDirName)
outfile = TFile("%s/%s_canvas.root"%(outputDirName, argv[1]),"RECREATE")
outfile.cd()
c2.Write()
outfile.Close()

print "\nOutput tcanvas is:\n%s"%outfile.GetName()
subprocess.call(["python", "tcanvasTDR.py", outfile.GetName(), "-b"])
exit()
