from ROOT import *
from math import sqrt
from sys import argv

dataFile = TFile("ddTreeHiggs_silver_Feb26.root")
sigFile = TFile("ddTreeHiggs_%s_Feb26.root"%argv[1])

sideband = "side5070"

sig            = sigFile.Get( "sig"     )
sig2           = sigFile.Get( "sig"     )
data           = dataFile.Get("sig"     )
data2          = dataFile.Get("sig"     )
sideLowThree   = dataFile.Get(sideband)
sideLowThree2  = dataFile.Get(sideband)
print sideLowThree
for branch in sideLowThree.GetListOfBranches():
    print branch
g = TGraph()
g2 = TGraph()

phoEtaMax   = 1.4442
jetEtaMax   = 2.0
deltaRmin   = 1.1

if argv[1]=="750":
    massWindowLo = 700
    massWindowHi = 800

elif argv[1]=="1000":
    massWindowLo = 950
    massWindowHi = 1050

elif argv[1]=="2000":
    massWindowLo = 1900
    massWindowHi = 2100

elif argv[1]=="3000":
    massWindowLo = 2200
    massWindowHi = 3800

else:
    exit("pick the signal mass")


phoEtaCut           = TCut("leadingPhAbsEta<%s"               % str(phoEtaMax  ) )
deltaRdataCut       = TCut("phJetDeltaR_sig>%s"             % str(deltaRmin  ) )
deltaRsidebandCut   = TCut("phJetDeltaR_sideLowThree>%s"         % ( str(deltaRmin)) )
jetEtaDataCut       = TCut("matchedJet_pruned_abseta<%s"        % str(jetEtaMax  ) )
jetEtaSidebandCut   = TCut("sideLowThreeJet_pruned_abseta<%s"% str(jetEtaMax) )

dataMassCuts         = TCut("(phJetInvMass_pruned_sig>%s)&&(phJetInvMass_pruned_sig<%s)"               % ( str(massWindowLo), str(massWindowHi) )    )
sidebandMassCuts     = TCut("(phJetInvMass_pruned_sideLowThree>%s)&&(phJetInvMass_pruned_sideLowThree<%s)" % ( str(massWindowLo), str(massWindowHi) )    )

for i in range(20, 90):
    masscutSideband = TCut()
    masscutData     = TCut()

    masscutData      += phoEtaCut + deltaRdataCut     + jetEtaDataCut     + dataMassCuts
    masscutSideband  += phoEtaCut + deltaRsidebandCut + jetEtaSidebandCut + sidebandMassCuts

    othercutSideband = TCut()
    othercutData     = TCut()

    othercutData      += phoEtaCut + deltaRdataCut     + jetEtaDataCut     + dataMassCuts
    othercutSideband  += phoEtaCut + deltaRsidebandCut + jetEtaSidebandCut + sidebandMassCuts

    cutValue = float(i)/float(100)
    thiscut  = TCut("cosThetaStar<%s"                  % str(cutValue) )
    othercut = TCut("phPtOverMgammaj>%s"               % str(cutValue) )
    print "the cut value is %f" % cutValue
    print "the cut string is %s" % thiscut
    masscutSideband+=thiscut
    masscutData+=thiscut
    othercutSideband+=othercut
    othercutData+=othercut
    c = TCanvas()
    primitives2=[]
    data.Draw("cosThetaStar", masscutData)
    for primitive in c.GetListOfPrimitives():
        primitive.SetName("data")
        primitive.SetLineColor(kBlack)
        primitives2.append(primitive.GetName())
    dataEntries = c.GetPrimitive("data").GetEntries()
    print "data has %i entries" % dataEntries
    print "step 0: ",
    print primitives2

    if i < 50:
        data2.Draw("phPtOverMgammaj", othercutData, "SAME")
        print data2
        for primitive in c.GetListOfPrimitives():
            print primitive
            if not primitive.GetName() in primitives2:
                primitive.SetName("data2")
                print "data2 has %i entries" % c.GetPrimitive("data2").GetEntries()
                primitive.SetLineColor(kBlack)
                primitives2.append(primitive.GetName())
        data2Entries = c.GetPrimitive("data2").GetEntries()
        print "data2 has %i entries" % data2Entries
        print "step 1: ",
        print primitives2

    sideLowThree.Draw("cosThetaStar", masscutSideband, "SAME")
    for primitive in c.GetListOfPrimitives():
        print primitive
        if not primitive.GetName() in primitives2:
            primitive.SetName("sideband")
            primitives2.append(primitive.GetName())
    sidebandEntries = c.GetPrimitive("sideband").GetEntries()
    print "sideband has %i entries" % sidebandEntries
    sidebandNormalization = dataEntries/sidebandEntries
    print "sideband normalization factor is %f" % sidebandNormalization
    for sidebandBin in range (0, c.GetPrimitive("sideband").GetNbinsX()):
        c.GetPrimitive("sideband").SetBinContent(sidebandBin, c.GetPrimitive("sideband").GetBinContent(sidebandBin)*sidebandNormalization)
    c.GetPrimitive("sideband").SetLineColor(kGreen)
    print "step 2: ",
    print primitives2

    if i < 50:
        sideLowThree2.Draw("phPtOverMgammaj", othercutSideband, "SAME")
        for primitive in c.GetListOfPrimitives():
            if not primitive.GetName() in primitives2:
                primitive.SetName("sideband2")
                primitives2.append(primitive.GetName())
        sideband2Entries = c.GetPrimitive("sideband2").GetEntries()
        print "sideband2 has %i entries" % sidebandEntries
        sideband2Normalization = data2Entries/sideband2Entries
        print "sideband2 normalization factor is %f" % sideband2Normalization
        for sideband2Bin in range (0, c.GetPrimitive("sideband2").GetNbinsX()):
            c.GetPrimitive("sideband2").SetBinContent(sideband2Bin, c.GetPrimitive("sideband2").GetBinContent(sideband2Bin)*sideband2Normalization)
        c.GetPrimitive("sideband2").SetLineColor(kGreen)
        print "step 3: ",
        print primitives2


    c.Update()
    c.Draw()

    primitives = []
    for primitive in c.GetListOfPrimitives():
        print "adding primitive with name %s" % primitive.GetName()
        primitives.append(primitive.GetName())
    print primitives
    sig.Draw("cosThetaStar", masscutData, "SAME")
    for primitive in c.GetListOfPrimitives():
        print primitive
        if not primitive.GetName() in primitives:
            print "found new primitive with name %s" % primitive.GetName()
            primitive.SetName("signal")
            print "found updated primitive with name %s" % primitive.GetName()
            primitives.append(primitive.GetName())
    if i < 50:
        sig2.Draw("phPtOverMgammaj", othercutData, "SAME")
        for primitive in c.GetListOfPrimitives():
            print primitive
            if not primitive.GetName() in primitives:
                print "found new primitive with name %s" % primitive.GetName()
                primitive.SetName("signal2")
                print "found updated primitive with name %s" % primitive.GetName()
                primitives.append(primitive.GetName())

    ss = c.GetPrimitive("signal").GetEntries()
    print "number of signal events is %i" % ss
    bb = c.GetPrimitive("sideband").GetEntries()
    print "number of background events is %i" % bb
    sOverRootB=ss/sqrt(bb)
    print "s over root b is %f" % sOverRootB
    g.SetPoint(g.GetN(), cutValue, sOverRootB)
    if i < 50:
        ss2 = c.GetPrimitive("signal2").GetEntries()
        print "number of signal2 events is %i" % ss2
        bb2 = c.GetPrimitive("sideband2").GetEntries()
        print "number of background2 events is %i" % bb2
        sOverRootB2=ss2/sqrt(bb2)
        print "s over root b, 2, is %f" % sOverRootB2
        g2.SetPoint(g2.GetN(), cutValue, sOverRootB2)
    c.Clear()

    del masscutSideband
    del masscutData

c2 = TCanvas()
c2.cd()
g.SetTitle("S/#sqrt{B} for #||{cos(#theta*)} and p_{T}/m_{#gammaj} cuts")
g.GetXaxis().SetTitle("cut value")
g.GetYaxis().SetTitle("S/#sqrt{B} (a.u.)")
g.Draw()
g2.SetLineColor(kRed)
g2.Draw("SAME")
c2.Draw()
outfile = TFile("optimization50to70_cosThetaStar_M=%s.root"%argv[1], "RECREATE")
outfile.cd()
g.Write()
g2.Write()

c2.Write()
c2.Print("cosThetaStarOptimization_50-70sideband_M=%s.pdf"%argv[1])
c2.Print("cosThetaStarOptimization_50-70sideband_M=%s.png"%argv[1])
