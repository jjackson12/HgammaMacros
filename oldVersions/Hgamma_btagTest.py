from ROOT import *
from math import sqrt
from sys import argv

sigMass = "750"
category = "EBEE"

dataFile = TFile("../physics/may5_btagging/small3_SilverJson_may5.root")
sigFile = TFile("../physics/may5_Hgamma_btagging/Hgamma_m%s_may5.root"%sigMass)
print "Signal mass is %s" % sigMass

sig          = sigFile.Get("higgs"     )
data          = dataFile.Get("higgs"     )
#if sideband == "100to110":
#    sideLow   = dataFile.Get("side100110")
#    sidebandIndex = "Four"
#elif sideband == "50to70":
#    sideLow   = dataFile.Get("side5070")
#    sidebandIndex = "Three"

sideLow   = dataFile.Get("side100110")
sidebandIndex = "Four"

#g = TGraph()

if sigMass=="750":
    massWindowLo = 700
    massWindowHi = 800

elif sigMass=="1000":
    massWindowLo = 950
    massWindowHi = 1050

elif sigMass=="2000":
    massWindowLo = 1900
    massWindowHi = 2100

elif sigMass=="3000":
    massWindowLo = 2200
    massWindowHi = 3800

else:
    exit("pick the signal mass")

phoEtaMaxEB   = 1.4442
phoEtaMaxEE   = 2.2
phoEtaMinEE   = 1.566
jetEtaMax   = 2.2
deltaRmin   = 1.1

btagLeadingWP    = 0.5
btagSubleadingWP = 0.5

dataCuts     = []
sidebandCuts = []

#cuts based on eta -- split into EB/EE/both categories
if category=="EB":
    phoEtaCut       = TCut("leadingPhAbsEta<%s"               % str(phoEtaMaxEB  ) )
if category=="EE":
    phoEtaCut       = TCut("%s<leadingPhAbsEta&&leadingPhAbsEta<%s"               % ( str(phoEtaMinEE),str(phoEtaMaxEE) ) )
if category=="EBEE":
    phoEtaCut       = TCut("leadingPhAbsEta<%s"               %  str(phoEtaMaxEE) )


#b-tagging cuts
btaggingDataCut     = TCut( 
btaggingSidebandCut =

#Other cuts
deltaRdataCut       = TCut("phJetDeltaR_higgs>%s"             % str(deltaRmin  ) )
deltaRsidebandCut   = TCut("phJetDeltaR_sideLow%s>%s"         % ( sidebandIndex, str(deltaRmin)) )
jetEtaDataCut       = TCut("higgsJet_pruned_abseta<%s"        % str(jetEtaMax  ) )
jetEtaSidebandCut   = TCut("sideLow%sJet_pruned_abseta<%s"% (sidebandIndex, str(jetEtaMax)) )
#cosThetadataCut     = TCut("cosThetaStar<0.5+0.25*(phJetInvMass_pruned_higgs-750)/250"                                       )
#cosThetasidebandCut = TCut("cosThetaStar<0.5+0.25*(phJetInvMass_pruned_sideLow%s-750)/250"  % sidebandIndex                  )
cosThetadataCut     = TCut("cosThetaStar<-0.627*TMath::ATan((-0.005938*phJetInvMass_pruned_higgs)+3.427)"                      )
cosThetasidebandCut = TCut("cosThetaStar<-0.627*TMath::ATan((-0.005938*phJetInvMass_pruned_sideLow%s)+3.427)"%sidebandIndex    )

dataMassCuts         = TCut("(phJetInvMass_pruned_higgs>%s)&&(phJetInvMass_pruned_higgs<%s)"               % ( str(massWindowLo), str(massWindowHi) )    )
sidebandMassCuts     = TCut("(phJetInvMass_pruned_sideLow%s>%s)&&(phJetInvMass_pruned_sideLow%s<%s)" % ( sidebandIndex, str(massWindowLo), sidebandIndex, str(massWindowHi) )    )

dataCuts.append(      phoEtaCut   )
sidebandCuts.append(  phoEtaCut   )

dataCuts.append(      deltaRdataCut   )
sidebandCuts.append(  deltaRsidebandCut   )

dataCuts.append(      jetEtaDataCut   )
sidebandCuts.append(  jetEtaSidebandCut   )

dataCuts.append(      cosThetadataCut   )
sidebandCuts.append(  cosThetasidebandCut   )

dataCuts.append(      dataMassCuts   )
sidebandCuts.append(  sidebandMassCuts   )

dataOverallCut = TCut()
sidebandOverallCut = TCut()
for cut in dataCuts:
  dataOverallCut += cut
for cut in sidebandCuts:
  sidebandOverallCut += cut

sigCanvas = TCanvas()
sig.Draw("phJetInvMass_pruned_higgs", dataOverallCut)
for primitive in sigCanvas.GetListOfPrimitives():
  primitive.SetName("sig")


